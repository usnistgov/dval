# D3M Validation Templates

The templates in this directory reprensent different types of validation according to a set of rules.

Using the `rbv` tool, they will check if a submission package follows all the rules described in the template. 

| Template                     | Description |
| ---                          | ----------- |
| `d3m_ta1_basic.yml`          | {TA1} checks for single predictions and pipeline, and for a match btw both |
| `d3m_ta1_pipeline_check.yml` | {TA1} `d3m_ta1_basic.yml` and validates pipeline|
| `d3m_ta1_full.yml`           | {TA1} `d3m_ta1_pipeline_check.yml`, checks for metadata, executables and runs predictions validation. |
| `d3m_ta2_basic.yml`          | {TA2} checks for predictions and pipelines, and that they all match |
| `d3m_ta2_with_checks.yml`    | {TA2} `d3m_ta2_basic.yml` and validates pipelines |
| `d3m_ta2_full.yml`           | {TA2} `d3m_ta2_with_checks.yml`, checks for metadata, executables and runs predictions validation|

:warning: Some templates require `ENV` variables to be set. For example, any template running
predictions validation requires `$SCORE_DIR` to be set to the path of the full data directory.

:warning: The current version of `rbv` does not support requiring a non exact count (e.g. at least one `count: +`)
so the {TA2} and {TA3} file checks are incomplete and could pass validation if there are *no* files matching a pattern.

## Requirements

This requires both this package (`d3m_outputs`) and the human-readable validation package.
For convenience, a `Pipfile` is provided in this folder.

The following lines will create a virtual environement with the right dependencies.

```bash
pip install pipenv
pipenv install --skip-lock
pipenv shell
```

## Running the validation

```bash
rbv -d submission_package template.yml
```

The standard output will reflect whether the validation
passed and the return code will be 0 (or 1) if it passed (or failed).

Some validation runs require environment variables.

You can set them in the same shell:
```bash
SCORE_DIR='/path/to/data'
[...]
rbv -d submission_package template.yml
```

or prepend the `rbv` command with a set of environment variables.
This will override variables set earlier in the same shell. 

```bash
SCORE_DIR='/path/to/data' rbv -d submission_package template.yml
```