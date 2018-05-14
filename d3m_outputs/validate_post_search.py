"""
Validates a post search phase: checks for the validity of the pipeline logs, and the existence of the executables 
The valid pipelines are available in a dictionary, stored in the valid_pipelines field of the class

Usage:

>>> from d3m_outputs import validate_post_search
>>> validator = PostSearchValidator(pipeline_directory, executable_directory, predictions_directory, output_file).validate()
>>> validator.valid_pipelines


"""
import os, sys
import json
import logging
import glob

from . import PipelineLog
from .file_checker import FileChecker
from .validation_type_checks import is_castable_to_type


class PostSearchValidator(object):
    '''
        Class that handles test script generation

    '''
    def __init__(self, pipeline_directory: str, executable_directory: str, verbose=False):
        '''
        Instanciate the class of the validator

        :param pipeline_directory:
        :type str:
        :param executable_directory:
        :type str:
        :param verbose:
        :type bool:
        '''
        super(PostSearchValidator, self).__init__()
        self.pipeline_directory = pipeline_directory
        self.executable_directory = executable_directory

        self.valid_pipelines = []

        if verbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.CRITICAL)

    def add_valid_pipeline(self, pipeline):
        '''
        Append a new pipeline to the vaid_pipelines field, after checking the unicity of its rank
        Returns True if the new pipeline has been appended

        :param pipeline:
        :type dict:
        :rtype: bool


        '''

        existing_ranks = [ p['pipeline_rank'] for p in self.valid_pipelines ]

        if pipeline['pipeline_rank'] in existing_ranks:
            logging.error(f'Ignoring pipeline {pipeline["name"]}: a pipeline with rank {pipeline["pipeline_rank"]} already exists')
            return False
        else:
            logging.info(f'Adding pipeline {pipeline["name"]} as a valid pipeline')

            self.valid_pipelines.append(pipeline)
            return True


    def validate(self, exit_on_error=True):
        '''
        Browse the pipeline directory, and validates each pipeline
        For each pipeline, checks the existence of the executable file it points to.

        Updates the valid_pipelines field with all valid pipelines and executables found

        Exits with an error if exit_on_error is set to True

        :param exit_on_error:
        :type bool:

        '''

        valid = True

        for root, dirs, files in os.walk(self.pipeline_directory):

            for pipeline_file in files:

                pipeline_file_path = os.path.join(root, pipeline_file)

                if not PipelineLog(pipeline_file_path).is_valid():
                    logging.error(f'Found invalid pipeline file at {pipeline_file_path}')
                    valid = False
                    continue

                with open(pipeline_file_path) as f:

                    pipeline = json.load(f)

                    executable_path = glob.glob(os.path.join(self.executable_directory, pipeline["name"]) + '*')

                    if len(executable_path) == 0:
                        logging.error(f'Cannot find the executable at {pipeline_file_path}')
                        valid = False
                        continue

                    if len(executable_path) > 1:
                        logging.error(f'Found several executables at {pipeline_file_path}')
                        valid = False
                        continue

                    logging.info(f'Checking executable {pipeline_file_path} pointed by pipeline {pipeline["name"]}')

                    file_checker = FileChecker(executable_path[0])

                    if file_checker._exists() and file_checker._executable():
                        logging.info('Found valid executable')
                    else:
                        logging.error(f'Found invalid executable at {executable_path[0]}')
                        valid = False
                        continue


                    self.add_valid_pipeline(pipeline)

        if not self.valid_pipelines:
            logging.error('Cannot find  valid pipeline files in the specified folder')
            valid = False
        else:
            logging.info(f'Valid pipelines pointing to a valid executable: {self.valid_pipelines}')

        if exit_on_error and not valid:
            logging.error('One or several error occured. Exiting.')
            sys.exit(1)


            





