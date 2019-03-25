import sys
from unittest.mock import patch

import pytest

from dval import cli

from . import LOCAL_DATA_DIR, SEED_DATA_DIR, skip_if_no_data


def compare_main_with_expected_output(test_args, expected, capture_fixture):
    with patch.object(sys, "argv", test_args):
        cli.main()
        out, err = capture_fixture.readouterr()
        assert f"valid={expected}".lower() in out.strip().lower()


def argv_for_vs_subcommand(path_to_submission_dir, path_to_score_dir):
    return ["test", f"vs", "-d", f"{path_to_score_dir}", f"{path_to_submission_dir}"]


def content_for_vs_subcommand(setting_up_a_submission, capture_fixture):
    submission_dir, score_dir, expected = setting_up_a_submission
    test_args = argv_for_vs_subcommand(submission_dir, score_dir)
    compare_main_with_expected_output(test_args, expected, capture_fixture)


data_for_ss_subcommand_w_core_data = [
    (LOCAL_DATA_DIR, "185_baseball", True, True),
    (LOCAL_DATA_DIR, "1491_one_hundred_plants_margin", True, True),
]

data_for_ss_subcommand_w_flexible_data = [
    (SEED_DATA_DIR, "185_baseball", True, False),
    (SEED_DATA_DIR, "1491_one_hundred_plants_margin", True, False),
    (SEED_DATA_DIR, "57_hypothyroid", True, False),
]


@pytest.mark.parametrize(
    "setting_up_a_submission",
    data_for_ss_subcommand_w_core_data,
    indirect=["setting_up_a_submission"],
)
def test_validate_subm_cmd(setting_up_a_submission, capfd):
    content_for_vs_subcommand(setting_up_a_submission, capfd)


@skip_if_no_data
@pytest.mark.parametrize(
    "setting_up_a_submission",
    data_for_ss_subcommand_w_flexible_data,
    indirect=["setting_up_a_submission"],
)
def test_validate_subm_cmd_flexible_data(setting_up_a_submission, capfd):
    content_for_vs_subcommand(setting_up_a_submission, capfd)
