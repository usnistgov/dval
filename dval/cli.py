# Contents subject to LICENSE.txt at project root

"""
USAGE

version
valid_predictions     -d score_dir predictions_file
valid_pipelines        pipeline_log_file
score                 -d score_dir [-g ground_truth_file] [--validation | --no-validation] predictions_file
"""

import argparse
import json
import logging
import os
import sys

from . import (
    score_predictions_file,
    is_predictions_file_valid,
    is_pipeline_valid,
    generated_problems,
)


def main():
    """"
    Main package function, reads CLI args and launches program.
    """
    parser = cli_parser()
    args = parser.parse_args()

    if hasattr(args, "func") and args.func:
        args.func(args)
    else:
        parser.print_help()


def cli_parser():
    """
    Defines accepted CLI syntax and the actions to take for command and args.

    Returns:
        argparse parser
    """
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser("Validate and score a DSE or D3M submission.")
    subs = parser.add_subparsers(
        title="subcommands", help="Available subcommands, call -h to see usage"
    )

    def add_protocol_subparser(name, kwargs, func, arguments):
        subp = subs.add_parser(name, **kwargs)
        for a, b in arguments:
            subp.add_argument(*a, **b)

        subp.set_defaults(func=func)

        group = subp.add_mutually_exclusive_group()
        group.add_argument("-v", "--verbose", action="store_true", dest="verbose")
        group.add_argument("-q", "--no-verbose", action="store_false", dest="verbose")
        group.set_defaults(verbose=True)

        return subp

    # version
    add_protocol_subparser(
        "version",
        dict(help="Print dval version"),
        func=print_package_version,
        arguments=[],
    )

    vpredictions_args = [
        [
            ["predictions_file"],
            dict(help="path to predictions file to validate.", nargs="+"),
        ],
        [
            ["-d", "--score-dir"],
            dict(help="Path to data ground truth (use SCORE/ directory)"),
        ],
    ]

    # valid_predictions -d score_dir predictions_file
    add_protocol_subparser(
        "valid_predictions",
        dict(help="Validate a predictions file against the d3m data directory."),
        func=cmd_valid_predictions,
        arguments=vpredictions_args,
    )

    vpipeline_args = [
        # Main positional argument
        [
            ["pipeline_log_file"],
            dict(help="path to predictions file to validate.", nargs="+"),
        ],
        [
            ["--allow-2017-format"],
            dict(
                help="Allow current and 2017 D3M pipeline format", action="store_true"
            ),
        ],
        [
            ["--no-enforce-full-2018-format"],
            dict(help="Lax 2018 D3M format enforcement", action="store_true"),
        ],
        [
            ["--no-check-bare-2018-format"],
            dict(help="Toggles primitive registration checks off", action="store_true"),
        ],
    ]

    # valid_pipelines [--allow-2017-format] [--no-enforce-full-2018-format] [--no-check-bare-2018-format] pipeline_log_file
    add_protocol_subparser(
        "valid_pipelines",
        dict(help="Validate a pipeline log file."),
        func=cmd_valid_pipeline,
        arguments=vpipeline_args,
    )

    vgenproblems_args = [
        [
            ["problems_directory"],
            dict(help="path to directory containing the generated problems."),
        ],
        [
            ["-o", "--output_file"],
            dict(help="path to csv file containing valid problem ids"),
        ],
    ]

    add_protocol_subparser(
        "valid_generated_problems",
        dict(help="Validate a generated problems directory."),
        func=cmd_valid_gen_problems,
        arguments=vgenproblems_args,
    )

    score_args = [
        [
            ["predictions_file"],
            dict(help="path to predictions file to score.", nargs="+"),
        ],
        [
            ["-d", "--score-dir"],
            dict(help="Path to data ground truth (use SCORE/ directory)"),
        ],
        [["-g"], dict(help="path to ground truth file", nargs="?")],
        [
            ["--validation"],
            dict(
                help="Toggle validation ahead of the scoring",
                dest="validation",
                action="store_true",
            ),
        ],
        [
            ["--no-validation"],
            dict(
                help="Toggle off validation ahead of the scoring.",
                dest="validation",
                action="store_false",
            ),
        ],
        [
            ["-o", "--outfile"],
            dict(
                help="Write scores in JSON to file",
                nargs="?",
                type=argparse.FileType("w"),
            ),
        ],
        [
            ["--mxe"],
            dict(
                help="Include the multi-cross-entropy score in the output.",
                action="store_true",
            ),
        ],
        [
            ["--subset-indices"],
            dict(
                help="Subset the predictions using a list of indices in a csv file",
                nargs=1,
            ),
        ],
    ]

    # score -d score_dir [-g ground_truth_file] [--validation | --no-validation] predictions_file
    score_parser = add_protocol_subparser(
        "score",
        dict(help="Score a predictions file."),
        func=cmd_score,
        arguments=score_args,
    )
    score_parser.set_defaults(validation=True)

    return parser


def catch_fnf(func):
    def wrapped_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as fnf:
            message = "ERROR: "
            if fnf.filename is None:
                message += fnf.args[0]
            else:
                message += f"Could not find file {fnf.filename}"
            sys.exit(message)

    return wrapped_func


@catch_fnf
def cmd_valid_predictions(args):
    @catch_fnf
    def single_valid_predictions(predictions_file, score_dir):
        try:
            return is_predictions_file_valid(predictions_file, score_dir)
        except Exception as e:
            logging.exception(e)
        return False

    valid = True
    for predictions_file in args.predictions_file:
        s = single_valid_predictions(predictions_file, args.score_dir)
        valid &= s
        print("{0: <50} valid={1}".format(predictions_file, s))

    if not valid:
        sys.exit("ERROR: At least one predictions file is invalid. ")

    return valid


@catch_fnf
def cmd_valid_pipeline(args):
    @catch_fnf
    def single_valid_pipeline(pipeline_file, **kwargs):
        try:
            return is_pipeline_valid(pipeline_file, **kwargs)
        except Exception as e:
            logging.exception(e)
        return False

    kwargs = dict()

    if "allow_2017_format" in args and args.allow_2017_format is not None:
        kwargs["allow_2017_format"] = args.allow_2017_format
    if (
        "no_check_bare_2018_format" in args
        and args.no_check_bare_2018_format is not None
    ):
        kwargs["check_bare_2018_format"] = not args.no_check_bare_2018_format
    if (
        "no_enforce_full_2018_format" in args
        and args.no_enforce_full_2018_format is not None
    ):
        kwargs["enforce_2018_format"] = not args.no_enforce_full_2018_format

    valid = True
    for pipeline_f in args.pipeline_log_file:
        s = single_valid_pipeline(pipeline_f, **kwargs)
        valid &= s
        print("{0: <50} valid={1}".format(pipeline_f, s))

    if not valid:
        sys.exit("ERROR: At least one pipeline log is invalid. ")


@catch_fnf
def cmd_valid_gen_problems(args):
    is_valid = generated_problems.check_generated_problems_directory(
        args.problems_directory, args.output_file
    )

    if is_valid:
        print("Directory {} is valid".format(args.problems_directory))
    else:
        sys.exit("ERROR: Directory {} is not valid".format(args.problems_directory))

    return is_valid


@catch_fnf
def cmd_score(args):
    if args.outfile is not None and len(args.predictions_file) > 1:
        sys.exit(
            "Writing JSON scores only supported for one predictions file at the time"
        )

    if "ground_truth_file" in args and args.ground_truth_file is not None:
        # if ground truth is not set, will default to the `targets.csv` present in the SCORE directory
        args.ground_truth_file = os.path.join(args.score_dir, "targets.csv")

    @catch_fnf
    def single_score_predictions(predictions_file):
        try:
            scores = score_predictions_file(
                predictions_file,
                args.score_dir,
                args.ground_truth_file,
                check_valid=args.validation,
                score_mxe=args.mxe,
                indices_file=args.subset_indices[0] if args.subset_indices else None,
            )
            return scores
        except Exception:
            logging.exception(
                f"Predictions file {predictions_file} could not be scored. try validating your file first"
            )

    for predictions_file in args.predictions_file:
        scores = single_score_predictions(predictions_file)

        if scores and args.outfile is None:
            print("{0: <50} scores={1}".format(predictions_file, scores.to_json()))
        else:
            if scores and args.outfile is not None:
                to_dump = [s.__dict__ for s in scores]
                json.dump(to_dump, args.outfile, sort_keys=True, indent=4)
                print(f"Scores written to {args.outfile.name}")


def print_package_version(_):
    print(__import__(__package__).__version__)


if __name__ == "__main__":
    main()
