# Contents subject to LICENSE.txt at project root

"""
Validate and score prediction files.
Requires a prediction file and the file organization in the each problem's SCORE directory.
Available as a subdirectory for all seed datasets at `https://datadrivendiscovery.org/data/seed_datasets_current`

USAGE:
>>> result_file_path = 'test/data/185_baseball_SCORE/mitll_predictions.csv'
>>> path_to_score_root = 'test/data/185_baseball_SCORE'
>>> groundtruth_path = 'test/data/185_baseball_SCORE/targets.csv'

Option 1: Using the Predictions class
>>> from dval import predictions.Predictions
>>> p = Predictions(result_file_path, path_to_score_root)
>>> p.is_valid()
True
>>> p.score(groundtruth_path)
[Score(target='Hall_Of_Fame', metric='f1', scorevalue=0.691369766848)]

Option 2: Using the wrapper functions
>>> from dval import predictions.is_predictions_file_valid, score_predictions_file
>>> is_predictions_file_valid(result_file_path, path_to_score_root)
True
>>> score_predictions_file(result_file_path, path_to_score_root, groundtruth_path)
[Score(target='Hall_Of_Fame', metric='f1', scorevalue=0.691369766848)]
"""

import logging
from pathlib import Path

import numpy as np
import pandas

from . import schemas
from .file_checker import FileChecker
from .metrics import METRICS_DICT, valid_metric, apply_metric
from .score import Score, Scores, MxeScore
from .validation_type_checks import (
    valid_index,
    valid_boolean,
    valid_real,
    valid_integer,
    valid_string,
    valid_categorical,
    valid_datetime,
)


class Predictions:
    SEPARATOR = ","

    def __init__(
        self,
        result_file_path,
        path_to_score_root,
        separator=SEPARATOR,
        indices_file=None,
    ):
        self.result_file_path = result_file_path

        self.score_root = Path(path_to_score_root)
        self.ds = schemas.D3MDataStructure(
            root=self.score_root, indices_file=indices_file
        )
        self.dataset_schema_path = self.ds.dataschema.filepath
        self.problem_schema_path = self.ds.problemschema.filepath

        self.indices_path = indices_file
        self.separator = separator
        self._load_data()
        self.ds.load_targets()

    def is_valid(self):
        # Check the shape of the predictions first
        valid = self._is_file_readable() and self._is_header_valid()

        # Then compute the other checks
        return valid and self._is_index_valid() and self._are_targets_valid()

    def score(self, targets_filepath, score_mxe=False):
        scores = list()
        # Score = namedtuple('Score', ['target', 'metric', 'scorevalue'])

        self.ds.load_targets(targets_filepath)

        try:
            baseline_score = self.ds.get_baseline_score()
        except FileNotFoundError:
            baseline_score = "None"

        # scoring_metrics = self.ds.metrics
        scoring_metrics = self.ds.problemschema.metrics_wparams

        for metric in scoring_metrics:
            if not valid_metric(metric["metric"]):
                logging.error(
                    f"Invalid metric {metric}.\nAvailable metrics: {METRICS_DICT.keys()}"
                )
                continue

            if "pos_label" in metric["params"]:
                # no pos_label specified for metric f1, setting to '1'
                metric["params"]["pos_label"] = int(metric["params"]["pos_label"])

            # In the metric is applicable to all, need to
            if (
                "applicabilityToTarget" in metric["params"]
                and metric["params"]["applicabilityToTarget"] == "allTargets"
            ):

                # Reorder and align the targets and the predictions columns
                gt_l = [self.ds.targets_df[target] for target in self.ds.target_names]
                pred_l = [self.frame[target] for target in self.ds.target_names]

                # Transpose them into a list of rows
                gt_l = np.transpose(gt_l)
                pred_l = np.transpose(pred_l)

                # Apply the metric on the array
                value = apply_metric(metric["metric"], gt_l, pred_l, **metric["params"])
                score = Score("allTargets", metric["metric"], value, baseline_score)
            else:
                for target in self.ds.target_names:
                    value = apply_metric(
                        metric["metric"],
                        self.ds.targets_df[target],
                        self.frame[target],
                        **metric["params"],
                    )
                    score = Score(target, metric["metric"], value, baseline_score)
            score.transform_normalize()
            scores.append(score)

        # Add the multi cross entropy if desired, and if the problem is a classification problem
        if score_mxe:
            if self.ds.problemschema.task_type == "classification":
                # MXE handles only one target currently
                value = apply_metric(
                    "crossEntropyNonBinarized",
                    self.ds.targets_df[target],
                    self.frame[target],
                )
                score = MxeScore(value)
                scores.append(score)
            else:
                logging.warning(f"Ignoring MXE. Task is not a classification task")
        return Scores(scores)

    def _load_data(self):
        """
            Load the predicted targets, sort them by index if any
        """

        self.frame = pandas.read_csv(self.result_file_path, delimiter=self.separator)

        index_name = self.ds.dataschema.index_name
        if index_name in self.frame.columns:
            self.frame.sort_values(by=index_name, inplace=True)

    def _is_header_valid(self):
        """
        :return: bool
        """
        headers = set(self.frame)
        expected = set(self.ds.expected_header)
        if headers != expected:
            logging.error(f"Invalid header. Found {headers}, expected {expected}")
            return False

        logging.info("Header is valid.")
        return True

    def _is_index_valid(self):
        valid = valid_index(self.ds.expected_index)
        is_nan = pandas.isnull(self.frame).any().all().all()
        targets = self.ds.targets_df
        if is_nan:
            valid = False
            logging.error(f"Certain entries are invalid or empty")
        if valid:
            index_name = self.ds.dataschema.index_name
            if set(targets.loc[:, index_name]) != set(self.frame.loc[:, index_name]):
                valid = False
                logging.error("Missing indexes in predictions file")

        return valid

    def _are_targets_valid(self):
        valid_types = [
            "boolean",
            "integer",
            "real",
            "string",
            "categorical",
            "dateTime",
            "realVector",
            "json",
            "geojson",
        ]

        target_types = self.ds.target_types

        for target, ttype in target_types.items():
            column = self.frame[target]
            if target == self.ds.index_name:
                return valid_index(column)
            elif ttype == "boolean":
                return valid_boolean(column)
            elif ttype == "real":
                return valid_real(column)
            elif ttype == "integer":
                return valid_integer(column)
            elif ttype == "string":
                return valid_string(column)
            elif ttype == "categorical":
                authorized_labels = None
                try:
                    authorized_labels = self.ds.targets_df[target].unique()
                except AttributeError:
                    logging.exception(
                        f"Wrong categorical values, actual: {self.ds.targets_df[target]} expected: ",
                        exc_info=False,
                    )
                    return False
                return valid_categorical(
                    column, authorized_labels=authorized_labels.tolist()
                )
            elif ttype == "dateTime":
                return valid_datetime(column)
            elif ttype in valid_types:
                pass
            else:
                logging.error(f"type: {ttype} is not supported.")
                return False

    def _is_file_readable(self):
        FileChecker(self.result_file_path).check_exists_read(self.result_file_path)
        logging.info("Predictions file exists and is readable.")
        return True


def is_predictions_file_valid(result_file, score_dir_path):
    return Predictions(result_file, score_dir_path).is_valid()


def score_predictions_file(
    result_file,
    score_dir_path,
    groundtruth_path,
    check_valid=True,
    score_mxe=False,
    indices_file=None,
):
    predictions = Predictions(result_file, score_dir_path, indices_file=indices_file)
    if check_valid and not predictions.is_valid():
        logging.error("Invalid predictions file")
        raise InvalidPredictionsError("Invalid predictions file")

    return predictions.score(groundtruth_path, score_mxe)


class InvalidPredictionsError(Exception):
    pass
