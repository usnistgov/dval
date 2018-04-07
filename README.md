# NIST Validation and Scoring code

This repository contains the NIST validation and scoring code components for the D3M evaluation.

In order to run the tests, it is required to use **python version >3.6**.

## Predictions file validation

### Requirements

**Requires** a local copy of the directory for the problem/dataset that contains:
* the dataset schema at `path_to_score_root/dataset_TEST/datasetDoc.json`
* the problem schema at `path_to_score_root/problem_TEST/problemDoc.json`
* the test `learningData.csv` at `path_to_score_root/dataset_TEST/tables/learningData.csv`

Download the seed datasets at [https://datadrivendiscovery.org/data/seed_datasets_current/]. Each problem/dataset has a `SCORE` folder that contains this structure.

### Usage

```python
path_to_score_root = 'test/data/185_baseball_SCORE'
groundtruth_path = 'test/data/185_baseball_SCORE/targets.csv'
result_file_path = 'test/data/185_baseball_SCORE/mitll_predictions.csv'
```

Option 1: Using the Predictions class
```python
>>> from predictions import Predictions
>>> p = Predictions(result_file_path, path_to_score_root)
>>> p.is_valid()
True
>>> scores = p.score(groundtruth_path)
>>> scores
[Score(target='Hall_Of_Fame', metric='f1', scorevalue=0.691369766848)]
>>> scores[0]['scorevalue']
0.691369766848
```

with the Score object being a named tuple defined the following way
```python
Score = collections.namedtuple('Score', ['target', 'metric', 'scorevalue'])
```

If a problem schema describes multiple targets and/or multiple metrics, the `.score()` function will return a
list of `Score` objects, one for each combination of `(target, metric)`.

Option 2: Using the wrapper functions
```python
>>> from predictions import is_predictions_file_valid, score_predictions_file
>>> is_predictions_file_valid(result_file_path, path_to_score_root)
True
>>> scores = score_predictions_file(result_file_path, path_to_score_root, groundtruth_path)
>>> scores
[Score(target='Hall_Of_Fame', metric='f1', scorevalue=0.691369766848)]
>>> scores[0]['scorevalue']
0.691369766848
```

### Checks

Checks that the validation code does on the prediction file include:

* Checks that file exists and is readable
* Checks the header (needs to be indexName, targetName1, [targetName2, ...])
* Check target types (from dataset schema data field types)
* Check length of the index
* Compare index with expected index


## Pipeline Logs file Validation

### Usage

```python
>>> from pipeline_logs_validator import PipelineLog
>>> PipelineLog('path/to/my.json').is_valid()
True
```

### Checks

Checks that the validation code does on the pipeline log files include:

* Checks that file exists and is readable
* Checks that the file is correct JSON
* Checks for all required fields
* Checks that `primitives` is a json list, with no duplicates
* Checks that `pipeline_rank` is an integer

## Run Tests
To run all tests: `python -m unittest discover`
