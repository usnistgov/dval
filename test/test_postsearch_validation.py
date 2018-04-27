import unittest
import os 
import json 

from pathlib import Path
import subprocess

from d3m_outputs import PostSearchValidator


class TestPostSearchValidation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.testdir = Path(__file__).parent / 'postsearch_validation'

        cls.search_config_file_content = {
                    "problem_schema": "/inputs/problem_TRAIN/problemDoc.json",
                    "problem_root": "/inputs/problem_TRAIN",
                    "dataset_schema": "/inputs/dataset_TRAIN/datasetDoc.json",
                    "training_data_root": "/inputs/dataset_TRAIN",
                    "pipeline_logs_root": os.path.join(cls.testdir, "pipelines"),
                    "executables_root": os.path.join(cls.testdir, "executables"),
                    "user_problems_root": "/outputs/user_problems",
                    "temp_storage_root": "/outputs/temp",
                    "timeout": 60,
                    "cpus"  : "28",
                    "ram"   : "56Gi"
        }

        cls.expected_valid_pipelines = [{'problem_id': '196_ag_problem_TRAIN', 
                                'pipeline_rank': 1, 
                                'name': 'd35f3bd7-8191-4f2b-a679-d168c2813bd8', 
                                'primitives': 
                                ['common_primitives.bayesian_ridge.bayesian_ridge.BayesianRidge',
                                 'dsbox.datapreprocessing.cleaner.greedy.GreedyImputation']}
                                ]

    def testPostSearchValidationUsingConfigFile(self):
        '''
        Test the execution of the post search validation using a config file
        '''

        search_config_file_path = os.path.join(self.testdir, 'config_search.json')
        
        with open(search_config_file_path, 'w') as f:
            json.dump(self.search_config_file_content, f)

        with open(search_config_file_path, 'r') as f:
            config_file_content = json.load(f)

            pipeline_directory = config_file_content["pipeline_logs_root"]
            executable_directory = config_file_content["executables_root"]

            
            validator = PostSearchValidator(pipeline_directory, executable_directory, verbose=True)
            validator.validate(exit_on_error=False)

            self.assertEqual(validator.valid_pipelines, self.expected_valid_pipelines)

    def testPostSearchValidationUsingArgs(self):
        '''
        Test the execution of the post search validation using classical args
        '''

        pipeline_directory = self.testdir / 'pipelines'
        executable_directory = self.testdir / 'executables'

        validator = PostSearchValidator(pipeline_directory, executable_directory, verbose=True)
        validator.validate(exit_on_error=False)

        self.assertEqual(validator.valid_pipelines, self.expected_valid_pipelines)

if __name__ == '__main__':
    unittest.main()
