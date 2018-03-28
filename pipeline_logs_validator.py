"""
Validate a pipeline log file (TA2 search output).

Usage:

>>> from pipeline_logs_validator import PipelineLog
>>> PipelineLog('path/to/my.json').is_valid()
True
"""

import json
import logging

from file_checker import FileChecker
from validation_type_checks import is_castable_to_type


class PipelineLog(dict):
    """
    Handles a single pipeline log. Init from log filepath.
    """

    def __init__(self, filepath):

        self.filepath = filepath

        if not FileChecker(self.filepath).check_exists_read():
            exit(1)

        try:
            with open(self.filepath) as f:
                filecontents = json.load(f)
                super().__init__(filecontents)
        except json.JSONDecodeError as e:
            logging.error(f'Incorrect json file {self.filepath}')
            raise e

    def is_valid(self):
        valid = True

        required_fields = {
            'name': lambda x: isinstance(x, str),
            'pipeline_rank': lambda x: is_castable_to_type(x, int),
            'primitives': lambda x: isinstance(x, list) and len(x) > 0,
            'problem_id': lambda x: isinstance(x, str)
        }

        for field, constraint in required_fields.items():
            if field not in self:
                logging.error(f'Missing field {field}')
                valid = False
            elif not constraint(self[field]):
                logging.error(f'Field {field} has an incorrect value.')
                valid = False

        # if the log file is invalid, stop here
        if not valid:
            return False

        duplicate_primitives = set([x for x in self['primitives'] if self['primitives'].count(x) > 1])
        if len(duplicate_primitives) > 0:
            logging.error(f'Found duplicate primitives in the primitive set: {duplicate_primitives}')

        logging.info(f'Log file for pipeline of rank {self["pipeline_rank"]} was valid.')
        return True
