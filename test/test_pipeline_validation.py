from glob import glob
from d3m_outputs.pipeline_logs_validator import load_json, is_pipeline_valid_old_schema, is_pipeline_valid_bare

def test_old_pipeline_pass():
    files = glob('test/pipelines/old_format/pass/*.json')
    assert len(files) > 0
    for file in files:
        jpipeline = load_json(file)
        assert is_pipeline_valid_old_schema(jpipeline) == True

def test_old_pipeline_fail():
    files = glob('test/pipelines/old_format/fail/*.json')
    assert len(files) > 0
    for file in files:
        jpipeline = load_json(file)
        assert is_pipeline_valid_old_schema(jpipeline) == False


def test_pipeline_pass():
    files = glob('test/pipelines/new_format/pass/*.json')
    assert len(files) > 0
    for file in files:
        jpipeline = load_json(file)
        assert is_pipeline_valid_bare(jpipeline) == True

def test_pipeline_fail():
    files = glob('test/pipelines/new_format/fail/*.json')
    assert len(files) > 0
    for file in files:
        jpipeline = load_json(file)
        assert is_pipeline_valid_old_schema(jpipeline) == False


def test_bare_pipeline_pass():
    files = glob('test/pipelines/new_format_bare/pass/*.json')
    assert len(files) > 0
    for file in files:
        jpipeline = load_json(file)
        assert is_pipeline_valid_bare(jpipeline) == True

def test_bare_pipeline_fail():
    files = glob('test/pipelines/new_format_bare/fail/*.json')
    assert len(files) > 0
    for file in files:
        jpipeline = load_json(file)
        assert is_pipeline_valid_old_schema(jpipeline) == False
