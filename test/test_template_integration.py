"""
These tests check that valid8 and the valid8 templates for D3M work as expected.

WARNING: they are slow. On 02/11/2019 they took 3m47s to run on a laptop.

They require:
    * the ``$SUBM_DIR`` environment variable to point to the test submissions directory,
    formatted as explained below. The default is './test_submissions'
    * the ``$DATA_DIR`` environment variable to point to the data directory, e.g. a directory containing
    both `datasets` and `eval_datasets` git repositories.

The D3M valid8 templates are in the `templates/` directory. These are tested against real submissions.
The tests look for these real submissions the directory specified in the ``$SUBM_DIR`` directory.
The layout of the directory must be:

.. code-block::

    $SUBM_DIR/
    ├── d3m_ta1_basic
    │   ├── fail/
    │   └── pass/
    ├── d3m_ta1_full
    │   ├── fail/
    │   └── pass/
    ├── d3m_ta1_pipeline_check
    │   ├── fail/
    │   └── pass/
    ├── d3m_ta2_basic
    │   ├── fail/
    │   └── pass/
    ├── d3m_ta2_full
    │   ├── fail/
    │   └── pass/
    └── d3m_ta2_with_checks
        ├── fail/
        └── pass/

Some complex templates (see ``templates_with_env_*`` variables below) require the
``SCORE_DIR`` environment to be set. Because of inconsistencies in how this directory was reported
in previous submissions, there are 2 ways this environment variable is extracted:

    1. By extracting the `problem_id` field from the ``metadata.yml`` file in the submission package
    2. By reading the parent directory name for the source dataset

In the first case, we expect submission packages directly under the pass/ or fail/ directories:

.. code-block::

    d3m_ta1_basic
    ├── fail
    │   ├── submission_dir_1
    │   └── submission_dir_2
    └── pass
        ├── submission_dir_3
        └── submission_dir_4

In the second case, we expect submission packages under a parent directory with the dataset name:

.. code-block::

    d3m_ta2_with_checks
    ├── fail
    │   ├── 1491_one_hundred_plants_margin
    │   │   └── submission_dir_1
    │   └── 49_facebook
    │       └── submission_dir_2
    └── pass
        ├── 1491_one_hundred_plants_margin
        │   └── submission_dir_3
        └── 49_facebook
            └── submission_dir_4

The test functions have two different criteria:

    * pass/fail
        * A passing function checks that when running the valid8 template on the submission package,
        no errors are raised. This type of test will fail if any errors are raised because ``valid8``
        returning a non-zero code makes the test function raise a ``subprocess.CalledProcessError``
        exception.
        * A failing function expects certain exception to be raised and will fail if they are not.
    * template env/no-env
        * A regular no-env template tests just runs a check on every submission package corresponding to
        the matching template.
        * A env-from yaml template test runs a check on every submission pacakge and pulls the SCORE_ENV
        environment variable gstfrom the ``metadata.yml`` file
        * A env-from directory name where the submission packages are nested under a directory with the dataset name.
"""

import glob
from os import environ
from pathlib import Path
import subprocess

import pytest

EXT = ".yml"
ROOT_DIR = Path(__file__).parent.parent

TEMPLATE_DIR = ROOT_DIR / "templates"
SUBM_DIR = Path(environ.get("SUBM_DIR", "./test_submissions"))
DATA_DIR = Path(environ.get("DATA_DIR", "./data"))

templates = ["d3m_ta1_basic", "d3m_ta1_pipeline_check", "d3m_ta2_basic"]
templates_with_env_from_yaml = ["d3m_ta1_full"]
templates_with_env_from_directory = ["d3m_ta2_with_checks", "d3m_ta2_full"]


def env_check(var):
    """Minimal checks to point out if the variable is not set correctly"""
    if not var.exists() or not var.is_dir() or len([x for x in var.iterdir()]) == 0:
        return False
    return True


skip_if_no_subm = pytest.mark.skipif(
    not env_check(SUBM_DIR), reason="SUBM_DIR does not appear to be set correctly."
)
skip_if_no_data = pytest.mark.skipif(
    not env_check(DATA_DIR), reason="DATA_DIR does not appear to be set correctly."
)


def submission_directories_for_template(template_name, expected):
    key = "pass" if expected else "fail"
    return glob.glob((SUBM_DIR / template_name / key / "D3M*").as_posix())


def template_call(template, submd, env=None):
    template_path = TEMPLATE_DIR / (template + EXT)
    # subprocess call to valid8
    # raises subprocess.CalledProcessError if error code not 0
    subprocess.run(
        f"valid8 apply -d {submd} {template_path}",
        shell=True,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )


def extract_score_dir_from_yaml(ymlfile):
    """Returns the location of the SCORE_DIR of the dataset mentioned in the yml file"""
    import yaml

    with open(ymlfile) as f:
        contents = yaml.safe_load(f)

    problem_id = contents["problem_id"]

    locations = glob.glob(f"{DATA_DIR}/*/*/{problem_id}")
    if len(locations) == 0:
        # some datasets have an extra level of nesting
        locations = glob.glob(f"{DATA_DIR}/*/*/*/{problem_id}")

    return f"{locations[0]}/SCORE"


@skip_if_no_subm
@pytest.mark.valid8
@pytest.mark.parametrize("template", templates)
class TestSimpleTemplates:
    def test_template_passes(self, template):
        subdirs = submission_directories_for_template(template, True)

        for subdir in subdirs:
            try:
                template_call(template, subdir)
            except Exception as e:
                pytest.fail(f"{e} exception raised for {Path(subdir).name}")

    def test_template_fails(self, template):
        subdirs = submission_directories_for_template(template, False)

        for subdir in subdirs:
            with pytest.raises(subprocess.CalledProcessError):
                template_call(template, subdir)


@skip_if_no_data
@skip_if_no_subm
@pytest.mark.valid8
@pytest.mark.parametrize("template", templates_with_env_from_yaml)
class TestDataFromYamlTemplates:
    def test_passes_with_env_from_yaml(self, template):

        subdirs = submission_directories_for_template(template, True)

        for subdir in subdirs:
            try:
                environ["SCORE_DIR"] = extract_score_dir_from_yaml(
                    f"{subdir}/metadata.yml"
                )
                template_call(template, subdir, env=environ)
            except Exception as e:
                pytest.fail(f"{e} exception raised for {Path(subdir).name}")

    def test_fails_with_env_from_yaml(self, template):
        subdirs = submission_directories_for_template(template, False)

        for subdir in subdirs:
            try:
                environ["SCORE_DIR"] = extract_score_dir_from_yaml(
                    f"{subdir}/metadata.yml"
                )
                template_call(template, subdir, env=environ)
            except (IndexError, FileNotFoundError, subprocess.CalledProcessError):
                pass  # this is what should happen
            else:
                pytest.fail(
                    f"An exception should have been raised, {Path(subdir).name}"
                )


@skip_if_no_data
@skip_if_no_subm
@pytest.mark.valid8
@pytest.mark.parametrize("template", templates_with_env_from_directory)
class TestDataFromDirectoryTemplates:
    def test_passes_with_env_from_directory(self, template):
        subdirs = submission_directories_for_template(template, True)

        for datadir in subdirs:
            datadir_p = Path(datadir)
            for subdir in datadir_p.iterdir():

                try:
                    environ["SCORE_DIR"] = datadir_p.name
                    template_call(template, subdir, env=environ)
                except Exception as e:
                    pytest.fail(f"{e} exception raised for {Path(subdir).name}")

    def test_fails_with_env_from_directory(self, template):
        subdirs = submission_directories_for_template(template, False)

        for subdir in subdirs:
            try:
                environ["SCORE_DIR"] = extract_score_dir_from_yaml(
                    f"{subdir}/metadata.yml"
                )
                template_call(template, subdir, env=environ)
            except (IndexError, FileNotFoundError, subprocess.CalledProcessError):
                pass  # this is what should happen
            else:
                pytest.fail(
                    f"An exception should have been raised, {Path(subdir).name}"
                )
