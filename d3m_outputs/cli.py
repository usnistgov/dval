"""
USAGE

valid_predictions     -d score_dir predictions_file
valid_pipelines        pipeline_log_file
valid_pipeline_dir     pipeline_log_dir
valid_executables_dir -p pipeline_log_dir [--validation | --no-validation] executables_dir
score                 -d score_dir [-g ground_truth_file] [--validation | --no-validation] predictions_file
score_seed_baselines  [--validation | --no-validation] seed_root_dir
"""

import argparse
import sys
import os
from . import score_predictions_file, is_predictions_file_valid, is_pipeline_valid

subparsers_l = ['valid_predictions', 'valid_pipelines', 'valid_pipeline_dir', 'valid_executables_dir', 'validate_post_search', 'test_script',
                'score', 'score_seed_baselines']


def catch_fnf(func):
    def wrapped_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as fnf:
            message = 'ERROR: '
            if fnf.filename is None:
                message += fnf.args[0]
            else:
                message += f'Could not find file {fnf.filename}'
            sys.exit(message)

    return wrapped_func


@catch_fnf
def cmd_valid_predictions(args):
    @catch_fnf
    def single_valid_predictions(predictions_file, score_dir):
        try:
            return is_predictions_file_valid(predictions_file, score_dir)
        except Exception as e:
            print(e)
        return False

    valid = True
    for predictions_file in args.predictions_file:
        s = single_valid_predictions(predictions_file, args.score_dir)
        valid &= s
        print('{0: <50} valid={1}'.format(predictions_file, s))

    if not valid:
        sys.exit('ERROR: At least one predictions file is invalid. ')


@catch_fnf
def cmd_valid_pipeline(args):
    @catch_fnf
    def single_valid_pipeline(pipeline_file, **kwargs):
        return is_pipeline_valid(pipeline_file, **kwargs)

    kwargs = dict()
    if 'allow_2017_format' in args and args.allow_2017_format is not None:
        kwargs['allow_2017_format'] = args.allow_2017_format
    if 'enforce_full_2018_format' in args and args.enforce_2018_format is not None:
        kwargs['enforce_full_2018_format'] = args.enforce_full_2018_format

    valid = True
    for pipeline_f in args.pipeline_log_file:
        s = single_valid_pipeline(pipeline_f, **kwargs)
        valid &= s
        print('{0: <50} valid={1}'.format(pipeline_f, s))

    if not valid:
        sys.exit('ERROR: At least one pipeline log is invalid. ')


@catch_fnf
def cmd_valid_pipeline_dir(args):
    raise NotImplementedError("Validating a pipeline directory has not been implemented yet")


@catch_fnf
def cmd_valid_exec_dir(args):
    raise NotImplementedError("Validating the executable directory has not been implemented yet")


@catch_fnf
def cmd_score(args):
    if 'ground_truth_file' in args and args.ground_truth_file is not None:
        # if ground truth is not set, will default to the `targets.csv` present in the SCORE directory
        args.ground_truth_file = os.path.join(args.score_dir, 'targets.csv')

    @catch_fnf
    def single_score_predictions(predictions_file):
        try:
            scores = score_predictions_file(predictions_file, args.score_dir,
                                          args.ground_truth_file, check_valid=args.validation)
            return scores
        except Exception as e:
            print(e)
            print(f'Predictions file {predictions_file} could not be scored. try validating your file first')

    for predictions_file in args.predictions_file:
        scores = single_score_predictions(predictions_file)
        print('{0: <50} scores={1}'.format(predictions_file, scores))


@catch_fnf
def cmd_seed_dir(args):
    raise NotImplementedError("Recursively scoring the baselines for multiple problems has not been implemented yet")


def add_yn_flag(subparser, flag_name):
    group = subparser.add_mutually_exclusive_group()
    group.add_argument(f'--{flag_name}', action='store_true', dest=flag_name)
    group.add_argument(f'--no-{flag_name}', action='store_false', dest=flag_name)



def cli_parser():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(title='subcommands')

    subparsers = {name: subs.add_parser(name) for name in subparsers_l}

    for subparser in subparsers.values():
        group = subparser.add_mutually_exclusive_group()
        group.add_argument('-v', '--verbose', action='store_true', dest='verbose')
        group.add_argument('-q', '--no-verbose', action='store_false', dest='verbose')
        group.set_defaults(verbose=True)

    # valid_predictions -d score_dir predictions_file
    subparsers['valid_predictions'].description = 'Validate a predictions file against the d3m data directory.'
    subparsers['valid_predictions'].add_argument('-d', '--score-dir', help='d3m data structure (use SCORE)')
    subparsers['valid_predictions'].add_argument('predictions_file', nargs='+',
                                                 help='path to predictions file to validate.'
                                                 )
    subparsers['valid_predictions'].set_defaults(func=cmd_valid_predictions)

    # valid_pipelines   pipeline_log_file
    subparsers['valid_pipelines'].description = 'Validate a pipeline log file.'
    subparsers['valid_pipelines'].add_argument('pipeline_log_file', nargs='+',
                                               help='path to predictions file to validate.'
                                               )
    # flag_allow_2017 = subparsers['valid_pipelines'].add_mutually_exclusive_group()
    # flag_allow_2017.add_argument(f'--allow-2017-format', action='store_true', dest='verbose')
    # flag_allow_2017.add_argument(f'--no-allow-2017-format', action='store_false', dest='verbose')
    # flag_allow_2017.set_defaults(verbose=True)

    add_yn_flag(subparsers['valid_pipelines'], 'allow-2017-format')
    add_yn_flag(subparsers['valid_pipelines'], 'enforce-full-2018-format')

    subparsers['valid_pipelines'].set_defaults(func=cmd_valid_pipeline)

    # valid_pipeline_dir pipeline_log_dir
    subparsers['valid_pipeline_dir'].description = 'Validate a directory of pipeline log files.'
    subparsers['valid_pipeline_dir'].add_argument('pipeline_log_dir', type=str,
                                                  help='path to directory with the pipeline logs to validate.'
                                                  )
    subparsers['valid_pipeline_dir'].set_defaults(func=cmd_valid_pipeline_dir)

    # valid_executables_dir -p pipeline_log_dir [--validation | --no-validation] executables_dir
    subparsers['valid_executables_dir'].description = 'Validate the directory of executables against the pipelines.'
    subparsers['valid_executables_dir'].add_argument('-p', '--pipeline-log-dir',
                                                     help='path to directory with the pipeline logs to validate.'
                                                     )
    subparsers['valid_executables_dir'].add_argument('executables_dir', help='path to directory with the executables')
    subparsers['valid_executables_dir'].add_argument('--validation', dest='validation', action='store_true')
    subparsers['valid_executables_dir'].add_argument('--no-validation', dest='validation', action='store_false')
    subparsers['valid_executables_dir'].set_defaults(validation=True, func=cmd_valid_exec_dir)


    # score -d score_dir [-g ground_truth_file] [--validation | --no-validation] predictions_file
    subparsers['score'].description = 'Score a predictions file.'
    subparsers['score'].add_argument('-d', '--score-dir',
                                     help='d3m data structure (use SCORE)')
    subparsers['score'].add_argument('-g', '--ground-truth-file', help='path to ground truth file', nargs='?')
    subparsers['score'].add_argument('predictions_file', help='path to predictions file to score.', nargs='+')
    subparsers['score'].add_argument('--validation', dest='validation', action='store_true')
    subparsers['score'].add_argument('--no-validation', dest='validation', action='store_false')
    subparsers['score'].set_defaults(validation=True, func=cmd_score)

    args = parser.parse_args()

    if hasattr(args, 'func') and args.func:
        args.func(args)
    else:
        parser.print_help()


def main():
    cli_parser()


if __name__ == '__main__':
    main()
