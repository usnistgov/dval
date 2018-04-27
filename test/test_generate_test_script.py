import unittest
from pathlib import Path
import subprocess

from d3m_outputs import TestScriptGenerator


class TestTestScriptGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.testdir = Path(__file__).parent / 'testscriptgen'

    def testScriptFileContent(self):

        pipeline_directory = self.testdir / 'pipelines'
        executable_directory = self.testdir / 'executables'
        predictions_directory = self.testdir / 'predictions'
        output_file = self.testdir / 'tmp.sh'
        config_json_path = self.testdir / 'config_test.json'
        
        TestScriptGenerator(pipeline_directory, executable_directory, predictions_directory, output_file, config_json_path).generate()
        
        with open(output_file) as f:
            file_content = f.read()

        result = subprocess.run([output_file], stdout=subprocess.PIPE).stdout.decode("utf-8") 

        expected_output = (f'Executing {executable_directory}/d35f3bd7-8191-4f2b-a679-d168c2813bd8.sh\n'
                        'Pipeline d35f3bd7-8191-4f2b-a679-d168c2813bd8 executed.\n'
                        'done\n'
                        f'Executing {executable_directory}/d35f3bd7-8191-4f2b-a679-d168c2813bd9.sh\n'
                        'Pipeline d35f3bd7-8191-4f2b-a679-d168c2813bd9 executed.\n'
                        'done\n')

        self.assertEqual(expected_output, result)


if __name__ == '__main__':
    unittest.main()
