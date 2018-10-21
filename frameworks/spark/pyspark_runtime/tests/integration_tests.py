import pip._internal
import zipfile
from virtualenv import create_environment, make_environment_relocatable
from amaterasu import conf
from unittest import TestCase, mock
mock_stomp = mock.MagicMock()
mock_stomp.send = lambda x: print(x)
mock.patch('stomp.Connection', new_callable=mock_stomp)
from amaterasu_pyspark.runtime import ama_context
import subprocess
import sys
import shutil
import glob
import os

venv_dir = '/tmp/ama_test_dir/venv'


def _create_amaterasu_venv():
    create_environment(venv_dir)
    make_environment_relocatable(venv_dir)
    activate_script = os.path.join(venv_dir, "bin", "activate_this.py")
    with open(activate_script, 'r') as f:
        exec(f.read())
    pip._internal.main(['install', '../'])


def setUpModule():
    _create_amaterasu_venv()
    dir_path = os.path.dirname(__file__)
    path = os.path.normpath(dir_path + '/' + os.pardir + '/dist/amaterasu_pyspark*.zip')
    ama_pyspark_package = glob.glob(path)[0]
    shutil.copy(ama_pyspark_package, '.')


def tearDownModule():
    shutil.rmtree(venv_dir)
    dir_path = os.path.dirname(__file__)
    path = os.path.normpath(dir_path + '/amaterasu_pyspark*.zip')
    ama_pyspark_package = glob.glob(path)[0]
    os.remove(ama_pyspark_package)


def _run_program(program, *args):
    if sys.version_info.minor >= 5:
        subprocess.run((program, *args))
    else:
        subprocess.call((program, *args))


class ActualScriptsNoSparkSubmit(TestCase):

    VENV_ZIP_PATH = '/tmp/amaterasu_venv.zip'

    @classmethod
    def setUpClass(cls):
        with open(cls.VENV_ZIP_PATH, 'wb') as f:
            zipf = zipfile.ZipFile(f, mode='w')
            zipf.write(venv_dir)


    @classmethod
    def tearDownClass(cls):
        os.remove(cls.VENV_ZIP_PATH)


    def test_simple_script_with_spark_submit_should_persist_list_of_squares(self):
        _run_program('spark-submit', '--files', self.VENV_ZIP_PATH, 'test_scripts/simple.py')
        sdf = ama_context.get_dataset(conf.job_metadata.actionName, 'odd')
        stored_list = sdf.select('pow_number').orderBy('pow_number').rdd.flatMap(lambda x: x).collect()
        expected_list = [1, 4, 9, 16]
        self.assertEqual(stored_list, expected_list)




class ActualScriptsTests(TestCase):



    def tearDown(self):
        shutil.rmtree(conf.env.workingDir.split('file://')[1])

    def test_simple_script(self):
        _run_program('python', 'test_scripts/simple.py')
        sdf = ama_context.get_dataset(conf.job_metadata.actionName, 'odd')
        stored_list = sdf.select('pow_number').orderBy('pow_number').rdd.flatMap(lambda x: x).collect()
        expected_list = [1, 4, 9, 16]
        self.assertEquals(stored_list, expected_list)

