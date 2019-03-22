from os import environ
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from dval import cli


ROOT_DIR = Path(__file__).parent.parent
SEED_DATA_DIR = Path(environ.get("SEED_DATA_DIR", "./data"))


def env_check(var):
    """Minimal checks to point out if the variable is not set correctly"""
    if not var.exists() or not var.is_dir() or len([x for x in var.iterdir()]) == 0:
        return False
    return True


skip_if_no_data = pytest.mark.skipif(
    not env_check(SEED_DATA_DIR),
    reason="SEED_DATA_DIR does not appear to be set correctly.",
)


def tuple_for(root, dataset, expected):
    direc = Path(root) / dataset
    return (direc / "mitll_predictions.csv", direc / "SCORE", expected)


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
    test_args = [
        "test",
        f"score",
        "-d",
        f"{path_to_score_dir}",
        f"{path_to_predictions}",
    ]
    compare_main_with_expected_output(test_args, expected, capsys)


def compare_main_with_expected_output(test_args, expected, capsys):
    with patch.object(sys, "argv", test_args):
        cli.main()
        out, err = capsys.readouterr()
        assert f'"scorevalue": {expected}' in out.strip()


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
