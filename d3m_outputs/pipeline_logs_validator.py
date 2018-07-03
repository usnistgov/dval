"""
Validate a pipeline log file (TA2 search output).

Usage:

>>> from d3m_outputs import is_pipeline_valid
>>> is_pipeline_valid('path/to/my.json')
True
"""

import json
import logging
import warnings

from d3m.metadata.pipeline import Pipeline
from .validation_type_checks import is_castable_to_type

ALLOW_2017_FORMAT = True
ENFORCE_2018_FORMAT = False

logger = logging.Logger(__name__)


def is_pipeline_valid(pipeline_uri,
                      allow_2017_format=ALLOW_2017_FORMAT,
                      enforce_2018_format=ENFORCE_2018_FORMAT):
    pipeline = load_json(pipeline_uri)
    if allow_2017_format:
        format_2017_valid = is_pipeline_valid_old_schema(pipeline)
        print("2017 pipeline format, valid=", allow_2017_format)

    bare_2018_valid = is_pipeline_valid_bare(pipeline)
    print("2018 'bare' format, valid=", bare_2018_valid)
    full_2018_valid = is_pipeline_valid_full_validation(pipeline_uri)
    print("2018 full format, valid=", full_2018_valid)

    valid = (allow_2017_format and format_2017_valid) or \
            (bare_2018_valid and not enforce_2018_format) or \
            full_2018_valid

    if valid and not bare_2018_valid:
        warnings.warn("This pipeline does not follow bare 2018 pipeline format. Update before eval.", UserWarning)

    if valid and not full_2018_valid:
        warnings.warn("This pipeline does not follow full pipeline format. Update before eval.", UserWarning)

    return valid


def phase1(pipeline_uri):

    valid = is_pipeline_valid_old_schema(pipeline_uri)



def is_pipeline_valid_full_validation(filename):
    try:
        func = getattr(Pipeline, "from_yaml" if filename.endswith(".yml") or filename.endswith(".yaml") else "from_json")
        func(open(filename, "r")).check(allow_placeholders=False)
        return True
    except Exception as error:
        return False


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

        return True

    required_fields = {
        'name'          : lambda x: isinstance(x, str),
        'pipeline_rank' : lambda x: is_castable_to_type(x, float),
        'steps'         : lambda x: primitives_check(x)
    }

    for field, cond in required_fields.items():
        if field not in pipeline:
            logging.error(f'Missing field {field}')
            valid = False
        elif not cond(pipeline[field]):
            logging.error(f'Field {field} has an incorrect value.')
            valid = False

    return valid
