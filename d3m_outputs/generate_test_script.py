"""
Generate a test script file from a pipeline direcotry, an executable directory and a predictions path
This script assumes that an /outputs/config_test.json file already exists

Usage:

>>> from d3m_outputs import TestScriptGenerator
>>> TestScriptGenerator(pipeline_directory, executable_directory, predictions_directory, output_file).generate()

"""
import os
import json
import logging

from . import PipelineLog
from .file_checker import FileChecker
from .validation_type_checks import is_castable_to_type


class TestScriptGenerator(object):
    '''
        Class that handles test script generation

    '''
    def __init__(self, pipeline_directory: str, executable_directory: str, predictions_directory: str, output_file: str, config_json_path='/outputs/config_test.json', verbose=False):
        '''
        Instanciate the class and create the first line of the future script file

        :param pipeline_directory:
        :type str:
        :param executable_directory:
        :type str:
        :param predictions_directory:
        :type str:
        :param output_file:
        :type str:
        :param config_json_path:
        :type str:
        '''
        super(TestScriptGenerator, self).__init__()
        self.pipeline_directory = pipeline_directory
        self.executable_directory = executable_directory
        self.predictions_directory = predictions_directory

        self.script_content = '#!/bin/bash\n'

        self.config_json_path = config_json_path

        self.output_file = output_file

        if verbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.CRITICAL)

    def generate(self):
        '''
        Browse the pipeline directory, and appends new entries in the script_content field for valid pipelines
        Writes the result at the location specified by output_file
        '''

        for root, dirs, files in os.walk(self.pipeline_directory):
            # Make sure all systems write files in same order for testing
            files.sort()
            for pipeline_file in files:
                pipeline_file_path = os.path.join(root, pipeline_file)

                if not PipelineLog(pipeline_file_path).is_valid():
                    logging.warning(f'Found invalid pipeline file at {pipeline_file_path}')
                    continue

                with open(pipeline_file_path) as f:
                    pipeline = json.load(f)

                    logging.info(f'Generating script block for pipeline {pipeline["name"]}')

                    self.script_content += parse_test_script(pipeline['name'], pipeline['pipeline_rank'], self.executable_directory, self.predictions_directory, self.config_json_path)


        with open(self.output_file, 'w') as f:
            f.write(self.script_content)

            os.chmod(self.output_file, 0o755)


def parse_test_script(pipeline_name: str, pipeline_rank: int, exec_directory: str, predictions_dir: str, config_json_path: str):
    '''
    Generates a script file content to run a pipeline from a set of information about this pipeline

    :param pipeline_name:
    :type str:
    :param pipeline_rank:
    :type int:
    :param exec_directory:
    :type str:
    :param predictions_dir:
    :type str:
    :param config_json_path:
    :type str:
    :rtype: str

    '''

    predictions_sub_dir = os.path.join(predictions_dir, str(pipeline_rank))

    predictions_sub_dir_esc = predictions_sub_dir.replace('/', r'\/')

    return f'''
    # Test script to run {pipeline_name}
    exec=$(find {exec_directory}  -maxdepth 1 -name {pipeline_name}*)
    if [[ $exec ]]; then
    mkdir -p {predictions_sub_dir};
    echo `sed -E 's/"results_root":[ "a-z0-9\/]+,/"results_root":"{predictions_sub_dir_esc}",/g' {config_json_path}` > {config_json_path};
    export CONFIG_JSON_PATH={config_json_path};
    export CONFIG_JSON=`cat {config_json_path}`;
    export JSON_CONFIG_PATH={config_json_path};
    export JSON_CONFIG=`cat {config_json_path}`;
    echo "Executing $exec"
    $exec {config_json_path} && echo done;
    fi
    '''
