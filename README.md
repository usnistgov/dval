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

### Installation

This package works with Python 3.6+ and **requires** the [d3m core package](https://gitlab.com/datadrivendiscovery/d3m).

To install latest released version:

```
$ pip install git+https://gitlab.datadrivendiscovery.org/nist/nist_eval_output_validation_scoring.git@master
```

To install a particular release of the package, e.g., `v2018.4.28`:

```
$ pip install git+https://gitlab.datadrivendiscovery.org/nist/nist_eval_output_validation_scoring.git@v2018.4.28
```

To install latest development (unreleased) version:

```
$ pip install git+https://gitlab.datadrivendiscovery.org/nist/nist_eval_output_validation_scoring.git@develop
```

### CLI Usage

#### Validate a pipeline log
```
d3m_outputs valid_pipelines pipeline_log_file [pipeline_log_file ...]
```
Parameters:
* `pipeline_log_file`: path to the predictions file to validate

For example
`d3m_outputs valid_pipelines mylog1.json mylog2.json`

In shells like bash, you can also do : `d3m_outputs valid_pipelines *.json`

#### Validate a predictions file

```
d3m_outputs valid_predictions -d score_dir predictions_file [predictions_file ...]
```
Parameters:
* `score_dir`: path to the directory described in Section Requirements. Use the `SCORE` directory of the seed datasets.
* `predictions_file`: path to the predictions file to validate

#### Score a predictions file

```
d3m_outputs score -d score_dir [-g ground_truth_file] [--validation | --no-validation] predictions_file [predictions_file ...]
```

Parameters:
* `score_dir`: path to the directory described in Section Requirements. Use the `SCORE` directory of the seed datasets.
* `ground_truth_file`: path to the ground truth file. If absent, will default to `score_dir/targets.csv`
* `predictions_file`: path to the predictions file to score
* `--validation | --no-validation`: validation is on by default. turn in off with `--no-validation`


#### Validate a generated problems directory

```
d3m_outputs valid_generated_problems ./test/generated_problems/correct_submission/
```

Parameters:
* `problems_directory`: path to directory containing the generated problems.


### Docker usage

Same usage as the CLI.

:warning: Remember to mount as volumes the data that you want to validate or score.

For example, to validate a `predictions.csv` file:
```bash
image='registry.datadrivendiscovery.org/nist/nist_eval_output_validation_scoring/d3m_outputs:v2018.4.28'
docker run -v /hostpath/to/data:/tmp/data $image valid_predictions -d /tmp/data/SCORE /tmp/data/predictions.csv
```

Images are in the project registry under `registry.datadrivendiscovery.org/nist/nist_eval_output_validation_scoring/IMAGE_NAME`
Example images:  
* `d3m_outputs:latest`, which points to the latest release - e.g. `d3m_outputs:v2018.4.28`
* `d3m_outputs:v2018.4.20` for a specific release. The commit is the one tagged with `v2018.4.20`.
* `branches/develop`: the latest commit on the `develop` branch (unreleased)


### Code Usage

```python
path_to_score_root = 'test/data/185_baseball_SCORE'
groundtruth_path = 'test/data/185_baseball_SCORE/targets.csv'
result_file_path = 'test/data/185_baseball_SCORE/mitll_predictions.csv'
```

Option 1: Using the Predictions class
```python
>>> from d3m_outputs import Predictions
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
>>> from d3m_outputs import is_predictions_file_valid, score_predictions_file
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


## Pipeline Validation

### Usage

```python
>>> from d3m_outputs import PipelineLog
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

## Documentation

Docs were build using sphinx and autodoc with the following commands in the `docs` directory

```
sphinx-apidoc -f -o source/ ../d3m_outputs
sphinx-build -b html source build
```

And the web docs can be loaded in `docs/build/index.html`
