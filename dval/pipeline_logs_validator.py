"""
Validate a pipeline log file (TA2 search output).

Usage:

>>> from dval import is_pipeline_valid
>>> is_pipeline_valid('path/to/my.json')
True
"""

import json
import logging
import typing

from d3m.metadata.pipeline import Pipeline, Resolver
from d3m.primitive_interfaces import base

from .validation_type_checks import is_castable_to_type

ALLOW_2017_FORMAT = False
CHECK_BARE_2018_FORMAT = True
ENFORCE_2018_FORMAT = True

logger = logging.Logger(__name__)


class NoPrimitiveCheckResolver(Resolver):
    """
    A resolver which never looks for primitives
    """

    def __init__(self):
        super().__init__(strict_resolving=True)

    def _get_primitive(
        self, primitive_description: typing.Dict
    ) -> typing.Optional[typing.Type[base.PrimitiveBase]]:
        return None


def is_pipeline_valid(
    pipeline_uri,
    allow_2017_format=ALLOW_2017_FORMAT,
    check_bare_2018_format=CHECK_BARE_2018_FORMAT,
    enforce_2018_format=ENFORCE_2018_FORMAT,
):
    pipeline = load_json(pipeline_uri)

    # If we allow 2017 format, return True if the pipeline is valid
    format_2017_valid = False
    if allow_2017_format:
        format_2017_valid = is_pipeline_valid_old_schema(pipeline)
        logging.info(f"2017 pipeline format, valid={format_2017_valid}")

        if format_2017_valid:
            return True

    # If we check any of the 2018 conditions, &= them
    if check_bare_2018_format or enforce_2018_format:
        valid_2018 = True
        if check_bare_2018_format:
            bare_2018_valid = is_pipeline_valid_bare(pipeline)
            logging.info(f"2018 'bare' format, valid={bare_2018_valid}")
            valid_2018 &= bare_2018_valid

        if enforce_2018_format:
            full_2018_valid = is_pipeline_valid_full_validation(pipeline_uri)
            logging.info(f"2018 full format, valid={full_2018_valid}")
            valid_2018 &= full_2018_valid

        return valid_2018

    # If we come here, either the 2017 test didn't pass, or no check was performed
    # If the 2017 test didn't happen, no test was performed so it's invalid by default
    if not allow_2017_format:
        logging.error("No check performed")

    return False


def is_pipeline_valid_full_validation(pipeline_path):
    resolver = NoPrimitiveCheckResolver()

    try:
        with open(pipeline_path, "r") as pipeline_file:
            if pipeline_path.endswith(".yml"):
                pipeline = Pipeline.from_yaml(pipeline_file, resolver=resolver)
            elif pipeline_path.endswith(".json"):
                pipeline = Pipeline.from_json(pipeline_file, resolver=resolver)
            else:
                logger.error("Unknown file extension.")
                return False

    except Exception:
        logger.exception(
            "Unable to parse pipeline: {pipeline_path}".format(
                pipeline_path=pipeline_path
            )
        )
        return False

    try:
        pipeline.check(allow_placeholders=False)
    except Exception:
        logger.exception(
            "Unable to validate pipeline: {pipeline_path}".format(
                pipeline_path=pipeline_path
            )
        )
        return False

    return True


def load_json(pipeline_uri):
    with open(pipeline_uri) as f:
        return json.load(f)


def is_pipeline_valid_old_schema(pipeline):
    valid = True

    required_fields = {
        "name": lambda x: isinstance(x, str),
        "pipeline_rank": lambda x: is_castable_to_type(x, float),  # previously int
        "primitives": lambda x: isinstance(x, list) and len(x) > 0,
    }

    for field, constraint in required_fields.items():
        if field not in pipeline:
            logging.error(f"Missing field {field}")
            valid = False
        elif not constraint(pipeline[field]):
            logging.error(f"Field {field} has an incorrect value.")
            valid = False

    if not valid:
        return valid

    duplicate_primitives = set(
        [x for x in pipeline["primitives"] if pipeline["primitives"].count(x) > 1]
    )
    if len(duplicate_primitives) > 0:
        logging.error(
            f"Found duplicate primitives in the primitive set: {duplicate_primitives}"
        )
        valid = False

    logging.info(
        f'Log file for pipeline of rank {pipeline["pipeline_rank"]} was valid.'
    )
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
        "pipeline_rank": lambda x: is_castable_to_type(x, float),
        "steps": lambda x: primitives_check(x),
    }

    for field, cond in required_fields.items():
        if field not in pipeline:
            logging.error(f"Missing field {field}")
            valid = False
        elif not cond(pipeline[field]):
            logging.error(f"Field {field} has an incorrect value.")
            valid = False

    return valid
