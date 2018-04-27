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
from . import score_predictions_file, is_predictions_file_valid, PipelineLog, generate_test_script, PostSearchValidator, TestScriptGenerator

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
    def single_valid_pipeline(pipeline_file):
        return PipelineLog(pipeline_file).is_valid()

    valid = True
    for pipeline_f in args.pipeline_log_file:
        s = single_valid_pipeline(pipeline_f)
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


@catch_fnf
def cmd_generate_test_script(args):
    '''

    Usage: python3.6 -m d3m_outputs.cli test_script -p test/testscriptgen/pipelines/ -e test/testscriptgen/executables/ --predictions_dir test/testscriptgen/predictions -o test/testscriptgen/tmp.sh -c test/testscriptgen/config_test.json -v

    '''

    context = {
        'pipeline_directory': args.pipeline_log_dir[0],
        'executable_directory': args.executables_dir[0],
        'predictions_directory': args.predictions_dir[0],
        'output_file': args.output[0],
        'verbose': args.verbose
    }

    if not args.config_test_file == None :
        context['config_json_path'] = args.config_test_file

    TestScriptGenerator(**context).generate()


@catch_fnf
def cmd_validate_post_search(args):
    '''
    Validates the post_search phase browsing the pipelines and the executables folders

    Usages: 

        To load the folders using the paths as arguments:
            python3.6 -m d3m_outputs.cli validate_post_search -p test/postsearch_validation/pipelines/ -e test/postsearch_validation/executables/ 

        To load the folders using the fields from a search configuration file
            python3.6 -m d3m_outputs.cli validate_post_search -c test/postsearch_validation/config_test.json -v

    '''

    # Load the directory paths as is 
    if args.config_search_file == None:
        pipeline_dir = args.pipeline_log_dir[0]
        exec_dir = args.executables_dir[0]
    
    # Or load the directory paths from a config file
    else:
        with open(args.config_search_file[0], 'r') as f:
            config = json.load(f)

            pipeline_dir = config["pipeline_logs_root"]
            exec_dir = config["executables_root"]


    context = {
        'pipeline_directory': pipeline_dir,
        'executable_directory': exec_dir,
        'verbose': args.verbose
    }

    PostSearchValidator(**context).validate()


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


    subparsers['validate_post_search'].description = 'Validate the pipeline logs and the executables after the post_search phase'

    # First mode: provide a JSON config file as an argument
    validate_post_search_config_file_args = subparsers['validate_post_search'].add_argument_group('From a JSON config file', 'Get the executables and the pipelines directories from a config file')
    validate_post_search_config_file_args.add_argument('-c', '--config_search_file', nargs=1, help='path to the search configuration file.')

    # Second mode: pass the arguments directly using the CLI
    validate_post_search_cli_args = subparsers['validate_post_search'].add_argument_group('From CLI args', 'Get the executables and the pipelines directories from CLI args')
    validate_post_search_cli_args.add_argument('-p', '--pipeline-log-dir', nargs=1, help='path to directory with the pipeline logs.')
    validate_post_search_cli_args.add_argument('-e', '--executables_dir', nargs=1, help='path to directory with the executables')

    subparsers['validate_post_search'].set_defaults(func=cmd_validate_post_search)

    
    subparsers['test_script'].description = 'Generate a script to run the executables pointed by the pipeline logs.'
    subparsers['test_script'].add_argument('-p', '--pipeline-log-dir', nargs=1, help='path to directory with the pipeline logs.', required=True)
    subparsers['test_script'].add_argument('-e', '--executables_dir', nargs=1, help='path to directory with the executables', required=True)
    subparsers['test_script'].add_argument('--predictions_dir', nargs=1, help='path to the folder that will contains the predictions', required=True)
    subparsers['test_script'].add_argument('-o', '--output', nargs=1, help='path to the script file that will be generated', required=True)
    subparsers['test_script'].add_argument('-c', '--config_test_file', nargs='?', help='path to the test configuration file. This defaults to /outputs/config_test.json')

    subparsers['test_script'].set_defaults(func=cmd_generate_test_script)


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
