"""
Validate a generated problem directory (TA3 problem generation).

Usage:
    python3.6 -m d3m_outputs.generated_problems your/problems/dir/

Checks that your/problems/dir/labels.csv exists with

    labels.csv:

    problem_id, system, meaningful
    p_id, s_id, yes/no
    ...

    your/problems/dir/:

        <p_id>/:
            schema.json
            ssapi.yyy
        labels.csv


"""

import glob
import logging
import os
import pandas as pd

from .file_checker import FileChecker
from .schemas import ProblemSchema

logger = logging.Logger(__name__)


def check_generated_problems_directory(directory_path, output_file):
    """
    Checks that a directory contains a labels.csv file, with
    the ['problem_id', 'system', 'meaningful'] columns.

    Then, for each entry p in the 'problem_id' column,
    look for the directory_path/p subfolder
    and run the check_generated_problems_subdirectory
    function over it.

    Returns false if any of the execution returns False

    Parameters:
    -----------
    directory_path: path to a directory

    Returns:
    --------
    is_valid: boolean
        True if and only if every subdirectory referenced by
        the labels file is valid subdirectory.


    """

    # Get the labels file path
    gen_problems_md_file_path = os.path.join(directory_path, "labels.csv")

    # Check that it exists
    gen_problems_md_file = FileChecker(gen_problems_md_file_path)

    if not gen_problems_md_file._exists():
        logger.error("Cannot find {}".format(gen_problems_md_file_path))
        return False

    # Load the labels.csv file content
    gen_problems_md_df = pd.read_csv(gen_problems_md_file_path)

    # Check that the headers of this file are correct
    expected_columns = ["problem_id", "system", "meaningful"]

    if set(expected_columns) != set(gen_problems_md_df.columns):
        logger.error(
            "Wrong headers: {}, Expected: {}".format(
                gen_problems_md_df.columns.tolist(), expected_columns
            )
        )

        return False

    # Define a function to call on each subdirectory
    def check_all_generated_problems_subdirectories(root_dir, sub_dir):
        full_path = os.path.join(root_dir, sub_dir)

        if not os.path.isdir(full_path):
            logger.error(
                "Cannot find subdirectory named {} at {}".format(sub_dir, root_dir)
            )
            return False

        return check_generated_problems_subdirectory(full_path)

    # Gather the results in a boolean array
    gen_problems_md_df["correct"] = gen_problems_md_df.apply(
        lambda row: check_all_generated_problems_subdirectories(
            directory_path, row["problem_id"]
        ),
        axis=1,
    )

    # Look for the False booleans
    failed_checks = gen_problems_md_df.loc[lambda row: ~row["correct"]]

    gen_problems_md_df.to_csv(output_file, index=False)

    # Return the list of failures if any
    if failed_checks.size > 0:
        logger.error(
            "Validation of problems {} failed".format(
                failed_checks["problem_id"].tolist()
            )
        )
        return False

    return True


def check_generated_problems_subdirectory(directory_path):
    """
    Checks that a directory contains a 'schema.json' file,
    that satisfies the .schemas.ProblemSchema syntax.

    then, check that a ssapi.* file exists

    Parameters:
    -----------
    directory_path: path to a directory


    Returns:
    --------
    is_valid: boolean
        True if and only if the required files exists
        and 'schema.json' is valid


    """

    # Generated problem check
    gen_problem_schema_file_path = os.path.join(directory_path, "schema.json")

    # Check that it exists
    gen_problem_schema_file = FileChecker(gen_problem_schema_file_path)

    if not gen_problem_schema_file._exists():
        logger.error("Cannot find {}".format(gen_problem_schema_file_path))
        return False

    # Check schema structure
    try:
        _ = ProblemSchema(gen_problem_schema_file_path)
    except Exception as e:
        logger.warning(
            "Invalid problem schema at {}. The following error occured: {}".format(
                gen_problem_schema_file_path, e
            )
        )

    # Generated pipeline check
    gen_pipeline_schema_file_glob = glob.glob(os.path.join(directory_path, "ssapi*"))

    # Check that a ssapi file exists
    if not gen_pipeline_schema_file_glob:
        logger.error("Cannot find any ssapi file at {}".format(directory_path))
        return False

    # if not gen_problem_schema_file._exists():
    #     logger.error('Cannot find {}'.format(gen_pipeline_schema_file_path))
    #     return False

    # Check schema structure
    # Right now the only check will be that the ssapi file exists
    # if not is_pipeline_valid_full_validation(gen_pipeline_schema_file_path):
    #     logger.error('Invalid pipeline schema at {}.'.format(gen_pipeline_schema_file_path))
    #     return False

    return True
