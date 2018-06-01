"""
Validate a pipeline log file (TA2 search output).

Usage:

>>> from d3m_outputs import PipelineLog
>>> PipelineLog('path/to/my.json').is_valid_old()
True
"""

import json
import logging
from pathlib import Path

from d3m.metadata.pipeline import Pipeline

from .file_checker import FileChecker
from .validation_type_checks import is_castable_to_type

logger = logging.Logger(__name__)


def is_pipeline_valid(pipeline_uri):
    try:
        with open(pipeline_uri) as pipeline_file:
            pipeline_description = Pipeline.from_json_content(string_or_file=pipeline_file)
    except (IOError, ):
        return False

    return True

def valid(filename):
    return getattr(Pipeline, "from_yaml_content" if filename.endswith(".yml") or filename.endswith(".yaml")  else "from_json_content")(open(filename, "r")).check(allow_placeholders=False)


def load_json(pipeline_uri):
    with open(pipeline_uri) as f:
        return json.load(f)


def is_pipeline_valid_old_schema(pipeline):
    valid = True

    required_fields = {
        'name'         : lambda x: isinstance(x, str),
        'pipeline_rank': lambda x: is_castable_to_type(x, float),  # previously int
        'primitives'   : lambda x: isinstance(x, list) and len(x) > 0,
    }

    for field, constraint in required_fields.items():
        if field not in pipeline:
            logging.error(f'Missing field {field}')
            valid = False
        elif not constraint(pipeline[field]):
            logging.error(f'Field {field} has an incorrect value.')
            valid = False

    if not valid:
        return valid

    duplicate_primitives = set([x for x in pipeline['primitives'] if pipeline['primitives'].count(x) > 1])
    if len(duplicate_primitives) > 0:
        logging.error(f'Found duplicate primitives in the primitive set: {duplicate_primitives}')
        valid = False

    logging.info(f'Log file for pipeline of rank {pipeline["pipeline_rank"]} was valid.')
    return valid


def is_pipeline_valid_bare(pipeline):
    valid = True

    def primitives_check(steps):
        if not isinstance(steps, list):
            return False

        if len(steps) == 0:
            return False

        try:
            primitives = [step['primitive']['name'] for step in steps]

            if len(primitives) != len(set(primitives)):
                # duplicates!
                return False

        except (KeyError, ):
            # print some error message
            return False

        return True

    required_fields = {
        'name'         : lambda x: isinstance(x, str),
        'pipeline_rank': lambda x: is_castable_to_type(x, float),
        'steps'   : lambda x: primitives_check(x)
    }

    for field, cond in required_fields.items():
        if field not in pipeline:
            logging.error(f'Missing field {field}')
            valid = False
        elif not cond(pipeline[field]):
            logging.error(f'Field {field} has an incorrect value.')
            valid = False

    return valid


class PipelineLog(dict):
    """
    Handles a single pipeline log. Init from log filepath.
    """

    def __init__(self, filepath):

        self.filepath = filepath
        self.filename = Path(filepath).name

        if not FileChecker(self.filepath).check_exists_read():
            exit(1)

        try:
            with open(self.filepath) as f:
                filecontents = json.load(f)
                super().__init__(filecontents)
        except json.JSONDecodeError as e:
            logging.error(f'Incorrect json file {self.filepath}')
            raise e

    def is_valid_old(self):
        valid = True

        required_fields = {
            'name': lambda x: isinstance(x, str),
            'pipeline_rank': lambda x: is_castable_to_type(x, float),
            'primitives': lambda x: isinstance(x, list) and len(x) > 0,
            'problem_id': lambda x: isinstance(x, str)
        }

        for field, constraint in required_fields.items():
            if field not in self:
                logging.error(f'{self.filename}: Missing field {field}')
                valid = False
            elif not constraint(self[field]):
                logging.error(f'{self.filename} Field {field} has an incorrect value.')
                valid = False

        # if the log file is invalid, stop here
        if not valid:
            return False

        duplicate_primitives = set([x for x in self['primitives'] if self['primitives'].count(x) > 1])
        if len(duplicate_primitives) > 0:
            logging.error(f'Found duplicate primitives in the primitive set: {duplicate_primitives}')

        logging.info(f'Log file for pipeline of rank {self["pipeline_rank"]} was valid.')
        return True


    def is_valid_bare(self):
        valid = True

        required_fields = {
            'name': lambda x: isinstance(x, str),
            'pipeline_rank': lambda x: is_castable_to_type(x, int),
            'steps': lambda x: isinstance(x, list) and len(x) > 0,
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


if __name__ == '__main__':
    from glob import glob
    files = glob('test/pipelines/new_format_bare/pass/*.json')

    for f in files:
        jpipeline = load_json(f)
        is_pipeline_valid_bare(jpipeline)
