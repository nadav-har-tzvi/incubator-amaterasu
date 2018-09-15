from unittest import TestCase, mock
mock_stomp = mock.MagicMock()
mock_stomp.send = lambda x: print(x)
mock.patch('stomp.Connection', new_callable=mock_stomp)
from amaterasu_pyspark.runtime import ama_context
import subprocess
import sys

class ActualScriptsTests(TestCase):

    def _run_script(self, script_path):
        if sys.version_info.minor >= 5:
            subprocess.run(('python', script_path))
        else:
            subprocess.call(('python', script_path))

    def test_simple_script(self):
        self._run_script('test_scripts/simple.py')
        sdf = ama_context.get_dataset('simple_test', 'powered_df')
        stored_list = sdf.select('pow_number').orderBy('pow_number').rdd.flatMap(lambda x: x).collect()
        expected_list = [1, 4, 9, 16]
        self.assertEquals(stored_list, expected_list)