"""
These tests require an environment variable: SEED_DATA_DIR

This can point to any location that holds datasets. For example:

    $SEED_DATA_DIR/
    ├── 185_baseball/
    │   ├── datasetTEST/
    │   ├── problemTEST/
    │   ├── mitll_predictions.csv
    │   └── SCORE/
    ...
"""
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from dval import cli

from . import (
    compare_main_with_expected_output,
    LOCAL_DATA_DIR,
    SEED_DATA_DIR,
    skip_if_no_data,
)


def tuple_for(root, dataset, expected, score_d_at_root=None):
    direc = Path(root) / dataset
    score_d = Path(direc) if score_d_at_root else direc / "SCORE"
    return direc / "mitll_predictions.csv", score_d, expected


def score_argv(path_to_predictions, path_to_score_dir):
    return ["test", f"score", "-d", f"{path_to_score_dir}", f"{path_to_predictions}"]


@pytest.mark.smoke
@skip_if_no_data
@pytest.mark.parametrize(
    "path_to_predictions, path_to_score_dir, expected",
    [
        tuple_for(SEED_DATA_DIR, "185_baseball", "0.691"),
        tuple_for(SEED_DATA_DIR, "1491_one_hundred_plants_margin", "0.693"),
        tuple_for(SEED_DATA_DIR, "57_hypothyroid", "0.842"),
    ],
)
def test_seed_score(path_to_predictions, path_to_score_dir, expected, capsys):
    test_args = score_argv(path_to_predictions, path_to_score_dir)
    compare_main_with_expected_output(test_args, expected, capsys)


@pytest.mark.smoke
@pytest.mark.parametrize(
    "path_to_predictions, path_to_score_dir, expected",
    [
        tuple_for(LOCAL_DATA_DIR, "185_baseball", "0.691", score_d_at_root=True),
        tuple_for(
            LOCAL_DATA_DIR,
            "1491_one_hundred_plants_margin",
            "0.693",
            score_d_at_root=True,
        ),
    ],
)
def test_core_data_score(path_to_predictions, path_to_score_dir, expected, capsys):
    test_args = score_argv(path_to_predictions, path_to_score_dir)
    compare_main_with_expected_output(test_args, expected, capsys)


@pytest.mark.smoke
def test_shows_help(capsys):
    test_args = ["dval"]
    with patch.object(sys, "argv", test_args):
        try:
            cli.main()
        except SystemExit:
            pass
        out, err = capsys.readouterr()
        assert out.startswith("usage") or err.startswith("usage")
