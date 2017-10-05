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

from .. import common, consts, compat
from .base import MakiMixin, ValidateRepositoryMixin, BaseHandler, HandlerError
from string import Template
from distutils.sysconfig import get_python_lib

import uuid
import os
import socket
import netifaces
import git


__version__ = '0.2.0-incubating'


class RunPipelineHandler(BaseHandler, MakiMixin,  ValidateRepositoryMixin):
    """
    This handler takes care of starting up Amaterasu Scala process.
    First, we validate the inputs we get. The user is expected to pass at least the repository URL.
    We inspect the submitted repository and validate that it exists and fits the structure of a valid Amaterasu job repository
    If all validations are passed, we invoke the Scala runtime.
    """

    def __init__(self, **args):
        super(RunPipelineHandler, self).__init__(**args)
        self.base_dir = '/tmp/amaterasu/repos'
        self.dir_path = '{}/{}'.format(self.base_dir, uuid.uuid4())
        self.amaterasu_root = os.path.abspath('{}/amaterasu/process/apache-amaterasu-{}'.format(get_python_lib(), __version__))

    def _validate_repository(self):
        super(RunPipelineHandler, self)._validate_repository()
        RunPipelineHandler.load_maki(os.path.join(self.dir_path, 'maki.yml'))

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

    def handle(self):
        try:
            git.Repo.clone_from(self.args['repository'][0], self.dir_path)
            self._validate_repository()
            self._generate_amaterasu_properties()
            command_params = [
                'java',
                '-cp',
                '{}/bin/leader-{}-all.jar'.format(self.amaterasu_root, __version__),
                "-Djava.library.path=/usr/lib",
                "org.apache.amaterasu.leader.mesos.JobLauncher",
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
            os.environ.setdefault('AWS_ACCESS_KEY_ID', "0")
            os.environ.setdefault('AWS_SECRET_ACCESS_KEY', "0")
            os.environ.setdefault('AMA_NODE', socket.gethostname())

            compat.run_subprocess(command_params, cwd=self.amaterasu_root)
        except git.GitError as e:
            raise HandlerError(inner_errors=[e])
