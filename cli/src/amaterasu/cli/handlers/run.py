"""
Run an Amaterasu pipeline.
You have to have Mesos installed on the same machine where Amaterasu is installed to use this command.
IMPORTANT:
In the future we plan to enable remote execution, hence you will be required to connect to a cluster prior to executing this command

Usage: ama run <repository_url>

Options:
    -h --help       Show this screen
    -e --env        The environment to use for running this job [default: default]
    -r --report     Verbosity, this controls how much of the job's logs is propagated to the CLI [default: none]
    -b --branch     What branch to use when running this job [default: master]
    -j --job-id     Provide a job-id to resume a paused job.
    -n --name       Provider a name for the job.
"""
from distutils.sysconfig import get_python_lib
from .. import common, consts, compat
from .base import MakiMixin, ValidateRepositoryMixin, BaseHandler, HandlerError
from . import config as config_handlers
from string import Template
import netifaces
import abc
import os
import socket
import uuid
import git


__version__ = '0.2.0-incubating'


class BaseRunPipelineHandler(BaseHandler, MakiMixin):

    platform = None

    def __init__(self, **args):
        super(BaseRunPipelineHandler, self).__init__(**args)
        self.base_dir = '/tmp/amaterasu/repos'
        self.dir_path = '{}/{}'.format(self.base_dir, uuid.uuid4())
        self.amaterasu_root = os.path.abspath(
            '{}/amaterasu/process/apache-amaterasu-{}'.format(get_python_lib(),
                                                              __version__))

    def _validate_repository(self):
        super(BaseRunPipelineHandler, self)._validate_repository()
        BaseRunPipelineHandler.load_maki(
            os.path.join(self.dir_path, 'maki.yml'))

    @abc.abstractmethod
    def _get_command_params(self):
        pass

    def handle(self):
        try:
            git.Repo.clone_from(self.args['repository_url'], self.dir_path)
            self._validate_repository()
            command_params = self._get_command_params()
            os.environ.setdefault('AWS_ACCESS_KEY_ID', "0")
            os.environ.setdefault('AWS_SECRET_ACCESS_KEY', "0")
            os.environ.setdefault('AMA_NODE', socket.gethostname())
            compat.run_subprocess(command_params, cwd=self.amaterasu_root)
        except git.GitError as e:
            raise HandlerError(inner_errors=[e])


class RunMesosPipelineHandler(BaseRunPipelineHandler, MakiMixin,  ValidateRepositoryMixin):
    """
    This handler takes care of starting up Amaterasu Scala process.
    First, we validate the inputs we get. The user is expected to pass at least the repository URL.
    We inspect the submitted repository and validate that it exists and fits the structure of a valid Amaterasu job repository
    If all validations are passed, we invoke the Scala runtime.
    """

    platform = 'mesos'

    def _get_command_params(self):
        command_params = [
            'java',
            '-cp',
            '{}/bin/leader-{}-all.jar'.format(self.amaterasu_root, __version__),
            "-Djava.library.path=/usr/lib",
            "org.apache.amaterasu.leader.mesos.JobLauncher",
            "--home",
            self.amaterasu_root,
            "--repo",
            self.args['repository_url'][0],
            "--env",
            self.args.get('env', 'default'),
            "--report",
            self.args.get('report', None),
            "--branch",
            self.args.get('branch', 'master')
        ]
        if self.args.get('job_id'):
            command_params.extend(["--job-id", self.args['job_id']])
        if self.args.get('name'):
            command_params.extend(["--name", self.args['name']])
        return command_params

    def _generate_amaterasu_properties(self):
        ama_template = Template(common.RESOURCES[consts.AMATERASU_PROPERTIES])
        default_gateway = netifaces.gateways()['default']
        if default_gateway:
            netface_name = default_gateway[netifaces.AF_INET][1]
            ip = netifaces.ifaddresses(netface_name)[netifaces.AF_INET][0]['addr']
        else:
            ip = '127.0.0.1'
        rendered = ama_template.substitute(zk=ip, master=ip)
        with open('{}/amaterasu.properties'.format(self.amaterasu_root), 'w') as f:
            f.write(rendered)


class RunYarnPipelineHandler(BaseRunPipelineHandler):

    platform = 'yarn'

    def _get_command_params(self):
        """
        yarn jar ${BASEDIR}/bin/leader-0.2.0-incubating-all.jar org.apache.amaterasu.leader.yarn.Client --home ${BASEDIR}
        :return:
        """
        command_params = [
            'yarn',
            'jar',
            '{}/bin/leader-{}-all.jar'.format(self.amaterasu_root, __version__),
            'org.apache.amaterasu.leader.yarn.Client',
            "--home",
            self.amaterasu_root,
            "--repo",
            self.args['repository'][0],
            "--env",
            self.args['env'],
            "--report",
            self.args['report'],
            "--branch",
            self.args['branch']
        ]
        if self.args['job_id']:
            command_params.extend(["--job-id", self.args['job_id']])
        if self.args['name']:
            command_params.extend(["--name", self.args['name']])
        if self.args['jar-path']:
            command_params.extend(['--jar-path', self.args['jar-path']])
        return command_params


def _check_amaterasu_properties():
    supported_platforms = ['mesos', 'yarn']
    if not os.path.exists(
        os.path.expanduser('~/.amaterasu/amaterasu.properties')):
        print('Amaterasu hasn\'t been configured yet, please fill in the following details:')
        platform = None
        while not platform:
            platform = input('Choose execution platform [{}]:'.format(', '.join(supported_platforms)))
            if platform.strip() not in supported_platforms:
                print('Invalid platform: {}'.format(platform))
                platform = None
        kwargs = {platform: True}
        handler = config_handlers.get_handler(**kwargs)
        handler()


def get_handler(**kwargs):
    with open(os.path.expanduser('~/.amaterasu/amaterasu.properties')) as f:
        for line in f.read().splitlines():
            var, value = line.split('=')
            if var == 'platform':
                if value == 'mesos':
                    return RunMesosPipelineHandler
                elif value == 'yarn':
                    return RunYarnPipelineHandler
                else:
                    raise NotImplemented('Unsupported platform: {}'.format(value))
        else:
            raise HandlerError('platform is missing from configuring! Please run ama config and try again.')