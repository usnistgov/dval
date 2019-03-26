import sys
from os import environ
from pathlib import Path
from unittest.mock import patch

import pytest

from dval import cli

ROOT_DIR = Path(__file__).parent.parent
LOCAL_DATA_DIR = ROOT_DIR / "data"
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


def compare_main_with_expected_output(test_args, expected, capture_fixture):
    with patch.object(sys, "argv", test_args):
        cli.main()
        out, err = capture_fixture.readouterr()
        assert f'"scorevalue": {expected}' in out.strip()
