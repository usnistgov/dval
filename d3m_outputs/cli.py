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
import json
import logging
from . import score_predictions_file, is_predictions_file_valid, is_pipeline_valid, generated_problems

subparsers_l = ['valid_predictions', 'valid_pipelines', 'valid_pipeline_dir', 'valid_executables_dir', 'validate_post_search', 'test_script',
                'valid_generated_problems', 'score', 'score_seed_baselines']


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
            logging.exception(e)
        return False

    valid = True
    for predictions_file in args.predictions_file:
        s = single_valid_predictions(predictions_file, args.score_dir)
        valid &= s
        print('{0: <50} valid={1}'.format(predictions_file, s))

    if not valid:
        sys.exit('ERROR: At least one predictions file is invalid. ')

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

    if 'allow_2017_format' in args and args.allow_2017_format is not None:
        kwargs['allow_2017_format'] = args.allow_2017_format
    if 'check_bare_2018_format' in args and args.check_bare_2018_format is not None:
        kwargs['check_bare_2018_format'] = args.check_bare_2018_format
    if 'enforce_full_2018_format' in args and args.enforce_full_2018_format is not None:
        kwargs['enforce_2018_format'] = args.enforce_full_2018_format

    valid = True
    for pipeline_f in args.pipeline_log_file:
        s = single_valid_pipeline(pipeline_f, **kwargs)
        valid &= s
        print('{0: <50} valid={1}'.format(pipeline_f, s))

    if not valid:
        sys.exit('ERROR: At least one pipeline log is invalid. ')


@catch_fnf
def cmd_valid_gen_problems(args):
    
    is_valid = generated_problems.check_generated_problems_directory(args.problems_directory, args.output_file)

    if is_valid:
        print('Directory {} is valid'.format(args.problems_directory))
    else:
        print('Directory {} is not valid'.format(args.problems_directory))

    return is_valid


@catch_fnf
def cmd_score(args):

    if args.outfile is not None and len(args.predictions_file) > 1:
        sys.exit('Writing JSON scores only supported for one predictions file at the time')

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
            logging.exception(f'Predictions file {predictions_file} could not be scored. try validating your file first')

    for predictions_file in args.predictions_file:
        scores = single_score_predictions(predictions_file)

        if scores and args.outfile is None:
            print('{0: <50} scores={1}'.format(predictions_file, scores.to_json()))
        else:
            if scores and args.outfile is not None:
                to_dump = [s.__dict__ for s in scores]
                json.dump(to_dump, args.outfile, sort_keys=True, indent=4)
                print(f'Scores written to {args.outfile.name}')


def add_yn_flag(subparser, flag_name):
    group = subparser.add_mutually_exclusive_group()
    group.add_argument(f'--{flag_name}', action='store_true')
    group.add_argument(f'--no-{flag_name}', action='store_false')

def cli_parser():
    logging.getLogger().setLevel(logging.INFO)
    
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
    add_yn_flag(subparsers['valid_pipelines'], 'check-bare-2018-format')

    subparsers['valid_pipelines'].set_defaults(func=cmd_valid_pipeline)

    subparsers['valid_generated_problems'].description = 'Validate a generated problems directory.'
    subparsers['valid_generated_problems'].add_argument('problems_directory',
                                                     help='path to directory containing the generated problems.'
                                                     )
    subparsers['valid_generated_problems'].add_argument('-o', '--output_file', help='path to csv file containing valid problem ids')
    subparsers['valid_generated_problems'].set_defaults(func=cmd_valid_gen_problems)

    # score -d score_dir [-g ground_truth_file] [--validation | --no-validation] predictions_file
    subparsers['score'].description = 'Score a predictions file.'
    subparsers['score'].add_argument('-d', '--score-dir',
                                     help='d3m data structure (use SCORE)')
    subparsers['score'].add_argument('-g', '--ground-truth-file', help='path to ground truth file', nargs='?')
    subparsers['score'].add_argument('predictions_file', help='path to predictions file to score.', nargs='+')
    subparsers['score'].add_argument('--validation', dest='validation', action='store_true')
    subparsers['score'].add_argument('--no-validation', dest='validation', action='store_false')
    subparsers['score'].add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'),
                                     help='Write scores in JSON to file')
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
