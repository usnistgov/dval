"""
Validate and score prediction files.
Requires a prediction file and the file organization in the each problem's SCORE directory.
Available as a subdirectory for all seed datasets at `https://datadrivendiscovery.org/data/seed_datasets_current`

USAGE:
>>> result_file_path = 'test/data/185_baseball_SCORE/mitll_predictions.csv'
>>> path_to_score_root = 'test/data/185_baseball_SCORE'
>>> groundtruth_path = 'test/data/185_baseball_SCORE/targets.csv'

Option 1: Using the Predictions class
>>> from d3m_outputs import Predictions
>>> p = Predictions(result_file_path, path_to_score_root)
>>> p.is_valid()
True
>>> p.score(groundtruth_path)
[Score(target='Hall_Of_Fame', metric='f1', scorevalue=0.691369766848)]

Option 2: Using the wrapper functions
>>> from d3m_outputs import is_predictions_file_valid, score_predictions_file
>>> is_predictions_file_valid(result_file_path, path_to_score_root)
True
>>> score_predictions_file(result_file_path, path_to_score_root, groundtruth_path)
[Score(target='Hall_Of_Fame', metric='f1', scorevalue=0.691369766848)]
"""

import logging
from collections import namedtuple
from pathlib import Path
import json

import pandas

from . import schemas
from .file_checker import FileChecker
from .metrics import METRICS_DICT, valid_metric, apply_metric
from .validation_type_checks import valid_d3mindex, valid_boolean, valid_real, valid_integer, valid_string, \
    valid_categorical, valid_datetime


class Score(namedtuple('Score', ['target', 'metric', 'scorevalue'])):

    @property
    def json(self):
        score_dict = self._asdict()
        return json.dumps(score_dict)


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

        file_readable = self._is_file_readable()
        header_valid = self._is_header_valid()
        targets_valid = self._are_targets_valid()
        index_valid = self._is_index_valid()

        valid = file_readable and targets_valid and index_valid and header_valid
        return valid

    def score(self, targets_filepath):
        scores = list()
        # Score = namedtuple('Score', ['target', 'metric', 'scorevalue'])

        self.ds.load_targets(targets_filepath)
        # scoring_metrics = self.ds.metrics
        scoring_metrics = self.ds.problemschema.metrics_wparams

        for metric in scoring_metrics:
            if not valid_metric(metric['metric']):
                logging.error(
                    f'Invalid metric {metric}.\nAvailable metrics: {METRICS_DICT.keys()}')
                continue

            if 'pos_label' in metric['params']:
                # no pos_label specified for metric f1, setting to '1'
                metric['params']['pos_label'] = int(metric['params']['pos_label'])

        # In the metric is applicable to all, need to
            if 'applicabilityToTarget' in metric['params'] and metric['params']['applicabilityToTarget'] == "allTargets":
                gt_l = [self.ds.targets_df[target] for target in self.ds.target_names]
                pred_l = [self.frame[target] for target in self.ds.target_names]
                value = apply_metric(metric['metric'], gt_l, pred_l, **metric['params'])
                scores.append(Score('allTargets', metric['metric'], value))
            else:
                for target in self.ds.target_names:
                    value = apply_metric(metric['metric'], self.ds.targets_df[target], self.frame[target], **metric['params'])
                    scores.append(Score(target, metric['metric'], value))

        return Scores(scores)

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
        is_nan = pandas.isnull(self.frame).any().all().all()
        targets_path=str(self.score_root)+'/targets.csv'
        targets = pandas.read_csv(
            targets_path,
            delimiter=self.separator)
        if is_nan:
            valid = False
            logging.error(f'Certain entries are invalid or empty')
        if valid:
            for i, (e1, e2) in enumerate(
                    zip(self.frame.index, self.ds.expected_index)):
                if e1 != e2:
                    valid = False
                    logging.error(
                        f'Index number {i} differs between predictions file and ground truth '
                        f'Predictions: {e1} '
                        f'Ground Truth: {e2} ')
                if str(self.frame.iloc[i,0]) != str(targets.iloc[i,0]):
                    valid = False
                    logging.error(
                        f'Index number {i} differs between predictions file and ground truth\n'
                        f'Predictions: {self.frame.iloc[e1,0]} '
                        f'Ground Truth: {targets.iloc[e2,0]}')

        return valid

    def _are_targets_valid(self):
        valid_types = ["boolean", "integer", "real", "string", "categorical", "dateTime", "realVector", "json", "geojson"]

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
            elif ttype in valid_types :
                pass
            else:
                logging.error(f'type: {ttype} is not supported.')
                return False

    def _is_file_readable(self):
        FileChecker(
            self.result_file_path).check_exists_read(
            self.result_file_path)
        logging.info('Predictions file exists and is readable.')
        return True

from collections.abc import Collection
class Scores(Collection):
    def __init__(self, scores):
        super().__init__()
        self.scores = scores

    def __iter__(self):
        return iter(self.scores)

    def __contains__(self, score):
        return score in self.scores

    def __len__(self):
        return len(self.scores)

    def __repr__(self):
        return self.scores.__repr__()

    def to_json(self, fileobject=None):
        scores_to_json = [score._asdict() for score in self.scores]
        if fileobject is not None:
            json.dump(scores_to_json, fileobject, sort_keys=True, indent=4)
        return json.dumps(scores_to_json, sort_keys=True, indent=4)


def is_predictions_file_valid(result_file, score_dir_path):
    return Predictions(result_file, score_dir_path).is_valid()


def score_predictions_file(result_file, score_dir_path, groundtruth_path, check_valid=True):
    predictions = Predictions(result_file, score_dir_path)
    if check_valid and not predictions.is_valid():
        logging.error('Invalid predictions file')
        raise InvalidPredictionsError('Invalid predictions file')

    return predictions.score(groundtruth_path)


class InvalidPredictionsError(Exception):
    pass
