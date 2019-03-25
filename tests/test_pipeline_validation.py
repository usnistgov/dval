from glob import glob
from dval.pipeline_logs_validator import (
    load_json,
    is_pipeline_valid_old_schema,
    is_pipeline_valid_bare,
    is_pipeline_valid,
    is_pipeline_valid_full_validation,
)
from glob import glob

from dval.pipeline_logs_validator import (
    load_json,
    is_pipeline_valid_old_schema,
    is_pipeline_valid_bare,
    is_pipeline_valid,
    is_pipeline_valid_full_validation,
)


# logging.disable(logging.NOTSET)
# logging.getLogger().setLevel(logging.DEBUG)

# ---------------------------------------------------------------------------
# Test is_pipeline_valid_old_schema
# ---------------------------------------------------------------------------


def test_old_pipeline_pass():
    files = glob("tests/pipelines/old_format/pass/*.json")
    assert len(files) > 0
    for file in files:
        jpipeline = load_json(file)
        assert is_pipeline_valid_old_schema(jpipeline) == True


def test_old_pipeline_fail():
    files = glob("tests/pipelines/old_format/fail/*.json")
    assert len(files) > 0
    for file in files:
        jpipeline = load_json(file)
        assert is_pipeline_valid_old_schema(jpipeline) == False


# ---------------------------------------------------------------------------
# Test is_pipeline_valid_full_validation
# ---------------------------------------------------------------------------


def test_pipeline_pass():
    files = glob("tests/pipelines/new_format/pass/*.json")
    assert len(files) > 0
    for file in files:
        print(file)
        assert is_pipeline_valid_full_validation(file) == True


def test_pipeline_fail():
    files = glob("tests/pipelines/new_format/fail/*.json")
    assert len(files) > 0
    for file in files:
        assert is_pipeline_valid_full_validation(file) == False


# ---------------------------------------------------------------------------
# Test is_pipeline_valid_bare
# ---------------------------------------------------------------------------


def test_bare_pipeline_pass():
    files = glob("tests/pipelines/new_format_bare/pass/*.json")
    assert len(files) > 0
    for file in files:
        jpipeline = load_json(file)
        assert is_pipeline_valid_bare(jpipeline) == True


def test_bare_pipeline_fail():
    files = glob("tests/pipelines/new_format_bare/fail/*.json")
    assert len(files) > 0
    for file in files:
        jpipeline = load_json(file)
        assert is_pipeline_valid_bare(jpipeline) == False


# ---------------------------------------------------------------------------
# Test is_valid_pipeline
# ---------------------------------------------------------------------------


def test_old_format_is_pipeline_valid_fail():
    files = glob("tests/pipelines/old_format/fail/*.json")
    assert len(files) > 0
    for file in files:
        assert is_pipeline_valid(file, False, False, False) == False
        assert is_pipeline_valid(file, False, False, True) == False
        assert is_pipeline_valid(file, False, True, False) == False
        assert is_pipeline_valid(file, False, True, True) == False
        assert is_pipeline_valid(file, True, False, False) == False
        assert is_pipeline_valid(file, True, False, True) == False
        assert is_pipeline_valid(file, True, True, False) == False
        assert is_pipeline_valid(file, True, True, True) == False


def test_old_format_is_pipeline_valid_pass():
    files = glob("tests/pipelines/old_format/pass/*.json")
    assert len(files) > 0
    for file in files:
        assert is_pipeline_valid(file, False, False, False) == False
        assert is_pipeline_valid(file, False, False, True) == False
        assert is_pipeline_valid(file, False, True, False) == False
        assert is_pipeline_valid(file, False, True, True) == False
        assert is_pipeline_valid(file, True, False, False) == True
        assert is_pipeline_valid(file, True, False, True) == True
        assert is_pipeline_valid(file, True, True, False) == True
        assert is_pipeline_valid(file, True, True, True) == True


def test_bare_format_is_pipeline_valid_fail():
    files = glob("tests/pipelines/new_format_bare/fail/*.json")
    assert len(files) > 0
    for file in files:
        assert is_pipeline_valid(file, False, False, False) == False
        assert is_pipeline_valid(file, False, False, True) == False
        assert is_pipeline_valid(file, False, True, False) == False
        assert is_pipeline_valid(file, False, True, True) == False
        assert is_pipeline_valid(file, True, False, False) == False
        assert is_pipeline_valid(file, True, False, True) == False
        assert is_pipeline_valid(file, True, True, False) == False
        assert is_pipeline_valid(file, True, True, True) == False


def test_bare_format_is_pipeline_valid_pass():
    files = glob("tests/pipelines/new_format_bare/pass/*.json")
    assert len(files) > 0
    for file in files:
        assert is_pipeline_valid(file, False, False, False) == False
        assert is_pipeline_valid(file, False, False, True) == False
        assert is_pipeline_valid(file, False, True, False) == True
        assert is_pipeline_valid(file, False, True, True) == False
        assert is_pipeline_valid(file, True, False, False) == False
        assert is_pipeline_valid(file, True, False, True) == False
        assert is_pipeline_valid(file, True, True, False) == True
        assert is_pipeline_valid(file, True, True, True) == False


def test_new_format_is_pipeline_valid_fail():
    files = glob("tests/pipelines/new_format/fail/*.json")
    assert len(files) > 0
    for file in files:
        assert is_pipeline_valid(file, False, False, False) == False
        assert is_pipeline_valid(file, False, False, True) == False
        assert is_pipeline_valid(file, False, True, False) == True
        assert is_pipeline_valid(file, False, True, True) == False
        assert is_pipeline_valid(file, True, False, False) == False
        assert is_pipeline_valid(file, True, False, True) == False
        assert is_pipeline_valid(file, True, True, False) == True
        assert is_pipeline_valid(file, True, True, True) == False


def test_new_format_is_pipeline_valid_pass():
    files = glob("tests/pipelines/new_format/pass/*.json")
    assert len(files) > 0
    for file in files:
        assert is_pipeline_valid(file, False, False, False) == False
        assert is_pipeline_valid(file, False, False, True) == True
        assert is_pipeline_valid(file, False, True, False) == True
        assert is_pipeline_valid(file, False, True, True) == True
        assert is_pipeline_valid(file, True, False, False) == False
        assert is_pipeline_valid(file, True, False, True) == True
        assert is_pipeline_valid(file, True, True, False) == True
        assert is_pipeline_valid(file, True, True, True) == True
