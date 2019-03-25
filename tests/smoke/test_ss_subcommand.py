import pytest

from . import (
    compare_main_with_expected_output,
    LOCAL_DATA_DIR,
    SEED_DATA_DIR,
    skip_if_no_data,
)


def argv_for_ss_subcommand(path_to_submission_dir, path_to_score_dir):
    return ["test", f"ss", "-d", f"{path_to_score_dir}", f"{path_to_submission_dir}"]


def content_for_ss_subcommand(setting_up_a_submission, capture_fixture):
    submission_dir, score_dir, expected = setting_up_a_submission
    test_args = argv_for_ss_subcommand(submission_dir, score_dir)
    compare_main_with_expected_output(test_args, expected, capture_fixture)


data_for_ss_subcommand_w_core_data = [
    (LOCAL_DATA_DIR, "185_baseball", "0.691", True),
    (LOCAL_DATA_DIR, "1491_one_hundred_plants_margin", "0.693", True),
]

data_for_ss_subcommand_w_flexible_data = [
    (SEED_DATA_DIR, "185_baseball", "0.691", False),
    (SEED_DATA_DIR, "1491_one_hundred_plants_margin", "0.693", False),
    (SEED_DATA_DIR, "57_hypothyroid", "0.842", False),
]


@pytest.mark.parametrize(
    "setting_up_a_submission",
    data_for_ss_subcommand_w_core_data,
    indirect=["setting_up_a_submission"],
)
def test_score_subm_cmd(setting_up_a_submission, capfd):
    content_for_ss_subcommand(setting_up_a_submission, capfd)


@skip_if_no_data
@pytest.mark.parametrize(
    "setting_up_a_submission",
    data_for_ss_subcommand_w_flexible_data,
    indirect=["setting_up_a_submission"],
)
def test_score_subm_cmd_flexible_data(setting_up_a_submission, capfd):
    content_for_ss_subcommand(setting_up_a_submission, capfd)
