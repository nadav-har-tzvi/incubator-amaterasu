from functools import partial
from unittest import mock
from behave import *

from cli import consts
from cli.handlers.base import HandlerError
# from cli.handlers.run import RunPipelineHandler
from tests.utils import MockArgs, noop
from uuid import uuid4

import os
import git



def mock_git_clone(uid, context, url, dest_dir):
    repository_dest = os.path.abspath('/tmp/amaterasu/repos/{}'.format(uid))
    if url == 'http://git.sunagakure.com/ama-job-non-exist.git':
        raise git.GitError("failed to send request: The server name or address could not be resolved")
    elif url == "http://git.sunagakure.com/ama-job-valid.git":
        os.makedirs(repository_dest, exist_ok=True)
        os.makedirs(os.path.join(repository_dest, 'src'), exist_ok=True)
        os.makedirs(os.path.join(repository_dest, 'env'), exist_ok=True)
        os.makedirs(os.path.join(repository_dest, 'env', 'default'), exist_ok=True)
        with open(os.path.join(repository_dest, 'maki.yml'), 'w') as maki:
            maki.write(context.test_resources['maki_valid.yml'])
        with open(os.path.join(repository_dest, 'env', 'default', consts.SPARK_CONF), 'w') as spark:
            spark.write(context.test_resources[consts.SPARK_CONF])
        with open(os.path.join(repository_dest, 'env', 'default', consts.JOB_FILE), 'w') as job:
            job.write(context.test_resources[consts.JOB_FILE])

    elif url == 'http://git.sunagakure.com/some-repo.git':
        os.makedirs(repository_dest)
        os.mkdir(os.path.join(repository_dest, 'sasuke'))
        os.mkdir(os.path.join(repository_dest, 'sasuke', 'is'))
        os.mkdir(os.path.join(repository_dest, 'sasuke', 'is', 'lame'))  # (NOT) TODO: Na nach nachman meuman
    else:
        raise NotImplementedError()


@given("A valid repository")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.repository_uri = 'http://git.sunagakure.com/ama-job-valid.git'


@when("Running a pipeline with the given repository")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # uid = uuid4()
    # with mock.patch('git.Repo.clone_from', partial(mock_git_clone, uid, context)), \
    #      mock.patch('uuid.uuid4', lambda: uid), \
    #      mock.patch('amaterasu.cli.compat.run_subprocess', noop):
        # handler = RunPipelineHandler(repository=[context.repository_uri], env='default', name=None, report='code', branch='master', job_id=None)
        # handler.amaterasu_root = '/tmp/amaterasu/assets'
        # os.makedirs(handler.amaterasu_root, exist_ok=True)
        # try:
        #     handler.handle()
        # except HandlerError as ex:
        #     context.ex = ex


@given("A valid file URI repository")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.repository_uri = 'http://git.sunagakure.com/ama-job-valid.git'


@given("A repository that doesn't exist")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.repository_uri = 'http://git.sunagakure.com/ama-job-non-exist.git'


@given("A repository that is not Amaterasu compliant")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.repository_uri = 'http://git.sunagakure.com/some-repo.git'


@then("Amaterasu should run")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@given("It is the first time the user runs a pipeline")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.first_run = True