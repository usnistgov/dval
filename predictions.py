"""
Validate and score prediction files.
Requires a prediction file and the file organization in the each problem's SCORE directory.
Available as a subdirectory for all seed datasets at `https://datadrivendiscovery.org/data/seed_datasets_current`

USAGE:
>>> result_file_path = 'test/data/185_baseball_SCORE/mitll_predictions.csv'
>>> path_to_score_root = 'test/data/185_baseball_SCORE'
>>> groundtruth_path = 'test/data/185_baseball_SCORE/targets.csv'

Option 1: Using the Predictions class
>>> from predictions import Predictions
>>> p = Predictions(result_file_path, path_to_score_root)
>>> p.is_valid()
True
>>> p.score(groundtruth_path)
0.691369766848

Option 2: Using the wrapper functions
>>> from predictions import is_predictions_file_valid, score_predictions_file
>>> is_predictions_file_valid(result_file_path, path_to_score_root)
True
>>> score_predictions_file(result_file_path, path_to_score_root, groundtruth_path)
0.691369766848
"""

from collections import namedtuple
from pathlib import Path

import logging
import pandas

import schemas
from file_checker import FileChecker
from metrics import METRICS_DICT, valid_metric, apply_metric
from validation_type_checks import valid_d3mindex, valid_boolean, valid_real, valid_integer, valid_string, \
    valid_categorical, valid_datetime


class Predictions:
    SEPARATOR = ','

    def __init__(self,
                 result_file_path,
                 path_to_score_root,
                 separator=SEPARATOR):
        self.result_file_path = result_file_path

        self.score_root = Path(path_to_score_root)
        self.ds = schemas.D3MDataStructure(root=self.score_root)
        self.dataset_schema_path = self.ds.dataschema.filepath
        self.problem_schema_path = self.ds.problemschema.filepath

        self.separator = separator
        self._load_data()

    def is_valid(self):
        valid = True

        valid &= self._is_file_readable()
        valid &= self._is_header_valid()
        valid &= self._are_targets_valid()
        valid &= self._is_index_valid()

        return valid

    def score(self, targets_filepath):
        scores = list()
        Score = namedtuple('Score', ['target', 'metric', 'scorevalue'])

        self.ds.load_targets(targets_filepath)
        scoring_metrics = self.ds.metrics

        for metric in scoring_metrics:
            if not valid_metric(metric):
                logging.error(
                    f'Invalid metric {metric}.\nAvailable metrics: {METRICS_DICT.keys()}')
                continue

            for target in self.ds.target_names:
                score = Score(target, metric, apply_metric(metric, self.ds.targets_df[target], self.frame[target]))
                scores.append(score)

        return scores

    def _load_data(self):
        self.frame = pandas.read_csv(
            self.result_file_path,
            delimiter=self.separator)

    def _is_header_valid(self):
        """
        :return: bool
        """
        headers = list(self.frame)
        expected = self.ds.expected_header
        if headers != expected:
            logging.error(
                f'Invalid header. Found {headers}, expected {expected}')
            return False

        logging.info('Header is valid.')
        return True

    def _is_index_valid(self):
        valid = valid_d3mindex(self.ds.expected_index)

        if valid:
            for i, (e1, e2) in enumerate(
                    zip(self.frame.index, self.ds.expected_index)):
                if e1 != e2:
                    valid = False
                    logging.error(
                        f'Index number {i} differs between predictions file and ground truth'
                        f'Predictions: {e1}'
                        f'Ground Truth: {e2}')

        return valid

    def _are_targets_valid(self):
        target_types = self.ds.target_types

        for target, ttype in target_types.items():
            column = self.frame[target]
            if target == self.ds.index_name:
                return valid_d3mindex(column)
            elif ttype == 'boolean':
                return valid_boolean(column)
            elif ttype == 'real':
                return valid_real(column)
            elif ttype == 'integer':
                return valid_integer(column)
            elif ttype == 'string':
                return valid_string(column)
            elif ttype == 'categorical':
                authorized_labels = None
                try:
                    authorized_labels = self.ds.targets_df[target].unique()
                except AttributeError:
                    pass
                return valid_categorical(
                    column, authorized_labels=authorized_labels)
            elif ttype == 'dateTime':
                return valid_datetime(column)
            else:
                logging.error(f'type: {ttype} is not supported.')
                return False

    def _is_file_readable(self):
        FileChecker(
            self.result_file_path).check_exists_read(
            self.result_file_path)
        logging.info('Predictions file exists and is readable.')
        return True


def is_predictions_file_valid(result_file, score_dir_path):
    return Predictions(result_file, score_dir_path).is_valid()


def score_predictions_file(result_file, score_dir_path, groundtruth_path):
    predictions = Predictions(result_file, score_dir_path)
    if not predictions.is_valid():
        logging.error('Invalid predictions file')
        exit(1)

    return predictions.score(groundtruth_path)

