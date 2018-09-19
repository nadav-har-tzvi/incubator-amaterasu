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

def setUpModule():
    dir_path = os.path.dirname(__file__)
    path = os.path.normpath(dir_path + '/' + os.pardir + '/dist/amaterasu_pyspark*.zip')
    ama_pyspark_package = glob.glob(path)[0]
    shutil.copy(ama_pyspark_package, '.')

def tearDownModule():
    dir_path = os.path.dirname(__file__)
    path = os.path.normpath(dir_path + '/amaterasu_pyspark*.zip')
    ama_pyspark_package = glob.glob(path)[0]
    os.remove(ama_pyspark_package)


class ActualScriptsTests(TestCase):

    def _run_program(self, program, *args):
        if sys.version_info.minor >= 5:
            subprocess.run((program, *args))
        else:
            subprocess.call((program, *args))

    def tearDown(self):
        shutil.rmtree(conf.env.workingDir.split('file://')[1])

    def test_simple_script(self):
        self._run_program('python', 'test_scripts/simple.py')
        sdf = ama_context.get_dataset(conf.job_metadata.actionName, 'odd')
        stored_list = sdf.select('pow_number').orderBy('pow_number').rdd.flatMap(lambda x: x).collect()
        expected_list = [1, 4, 9, 16]
        self.assertEquals(stored_list, expected_list)

    def test_simple_script_with_spark_submit(self):
        dir_path = os.path.dirname(__file__)
        path = os.path.normpath(dir_path + '/amaterasu_pyspark*.zip')
        ama_pyspark_package = glob.glob(path)[0]
        self._run_program('spark-submit', '--py-files', ama_pyspark_package, 'test_scripts/simple.py')
        sdf = ama_context.get_dataset(conf.job_metadata.actionName, 'odd')
        stored_list = sdf.select('pow_number').orderBy('pow_number').rdd.flatMap(lambda x: x).collect()
        expected_list = [1, 4, 9, 16]
        self.assertEqual(stored_list, expected_list)