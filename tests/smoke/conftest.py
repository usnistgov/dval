from pathlib import Path

import pytest


@pytest.fixture
def setting_up_a_submission(request, tmpdir):
    root, dataset, expected, score_d_at_root = request.param
    direc = Path(root) / dataset
    score_d = Path(direc) if score_d_at_root else direc / "SCORE"
    predictions_file = direc / "mitll_predictions.csv"

    # copy mitll_predictions.csv as predictions.csv in its own directory
    submitted_pfile = tmpdir / "predictions.csv"
    submitted_pfile.write_text(predictions_file.read_text(), encoding="utf-8")

    yield (str(tmpdir), score_d, expected)
