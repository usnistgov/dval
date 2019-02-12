import unittest
import sys
import os
from glob import glob

from d3m_outputs.cli import cli_parser, cmd_valid_pipeline

CURRENT_PATH = os.path.abspath(__file__)
TEST_DIR_PATH = os.path.dirname(CURRENT_PATH)


class TestCmdValidPipelines(unittest.TestCase):
    def testFileNotFound(self):
        sys.argv[1:] = ["valid_pipelines", ""]
        with self.assertRaises(SystemExit):
            cli_parser()

    def testNotValidate(self):
        sys.argv[1:] = [
            "valid_pipelines",
            os.path.join(TEST_DIR_PATH, "pipelinelogs/missing_rank.json"),
            "--allow-2017-format",
        ]
        with self.assertRaises(SystemExit):
            cli_parser()

    def testOk(self):
        sys.argv[1:] = [
            "valid_pipelines",
            os.path.join(TEST_DIR_PATH, "pipelinelogs/correct_pipeline.json"),
            "--allow-2017-format",
        ]
        try:
            cli_parser()
        except Exception:
            self.fail("valid_pipelines raised an exception")


class TestCmdValidPredictions(unittest.TestCase):
    def testFileNotFound(self):
        sys.argv[1:] = [
            "valid_predictions",
            "-d",
            os.path.join(TEST_DIR_PATH, "data/185_baseball"),
            "",
        ]
        with self.assertRaises(SystemExit):
            cli_parser()

    def testDirectoryNotFound(self):
        sys.argv[1:] = [
            "valid_predictions",
            "-d",
            "",
            os.path.join(TEST_DIR_PATH, "data/185_baseball/mitll_predictions.csv"),
        ]
        with self.assertRaises(SystemExit):
            cli_parser()

    def testOk(self):
        sys.argv[1:] = [
            "valid_predictions",
            "-d",
            os.path.join(TEST_DIR_PATH, "data/185_baseball"),
            os.path.join(TEST_DIR_PATH, "data/185_baseball/mitll_predictions.csv"),
        ]
        try:
            cli_parser()
        except Exception:
            self.fail("valid_predictions raised an exception")


class TestCmdValidGeneratedProblem(unittest.TestCase):
    def testLabelsNotValid(self):
        sys.argv[1:] = [
            "valid_generated_problems",
            os.path.join(TEST_DIR_PATH, "generated_problems/wrong_labels_missing"),
            "-o",
            os.path.join(
                TEST_DIR_PATH, "generated_problems/result_generated_problems.csv"
            ),
        ]
        with self.assertRaises(SystemExit):
            cli_parser()

    def testOk(self):
        sys.argv[1:] = [
            "valid_generated_problems",
            os.path.join(TEST_DIR_PATH, "generated_problems/correct_submission"),
            "-o",
            os.path.join(
                TEST_DIR_PATH, "generated_problems/result_generated_problems.csv"
            ),
        ]
        try:
            cli_parser()
        except Exception:
            self.fail("valid_generated_problems raised an exception")

    def tearDown(self):
        subdirs = glob(
            os.path.join(
                TEST_DIR_PATH, "generated_problems/result_generated_problems.csv"
            )
        )
        for file in subdirs:
            os.remove(file)


class TestCmdScore(unittest.TestCase):
    def testOk(self):
        sys.argv[1:] = [
            "score",
            "-d",
            os.path.join(TEST_DIR_PATH, "data/185_baseball"),
            "-g",
            os.path.join(TEST_DIR_PATH, "data/185_baseball/targets.csv"),
            "--validation",
            os.path.join(TEST_DIR_PATH, "data/185_baseball/mitll_predictions.csv"),
        ]
        try:
            cli_parser()
        except SystemExit:
            self.fail("score raised an exception")

    def testScoreDirectoryNotFound(self):
        sys.argv[1:] = [
            "score",
            "-d",
            "",
            "-g",
            os.path.join(TEST_DIR_PATH, "data/185_baseball/targets.csv"),
            "--validation",
            os.path.join(TEST_DIR_PATH, "data/185_baseball/mitll_predictions.csv"),
        ]

        # with self.assertRaises(Exception):
        #    cli_parser()

    def testTargetNotFound(self):
        sys.argv[1:] = [
            "score",
            "-d",
            os.path.join(TEST_DIR_PATH, "data/185_baseball"),
            "-g",
            "",
            "--validation",
            os.path.join(TEST_DIR_PATH, "data/185_baseball/mitll_predictions.csv"),
        ]

        try:
            cli_parser()
        except SystemExit:
            self.fail("score raised an exception")

    def testPredictionNotFound(self):
        sys.argv[1:] = [
            "score",
            "-d",
            os.path.join(TEST_DIR_PATH, "data/185_baseball"),
            "-g",
            os.path.join(TEST_DIR_PATH, "data/185_baseball/targets.csv"),
            "--validation",
            "",
        ]

        # with self.assertRaises(Exception):
        #    cli_parser()

    def testMultiplePredictionFiles(self):
        sys.argv[1:] = [
            "score",
            "-d",
            os.path.join(TEST_DIR_PATH, "data/185_baseball"),
            "-g",
            os.path.join(TEST_DIR_PATH, "data/185_baseball/targets.csv"),
            "--validation",
            os.path.join(TEST_DIR_PATH, "data/185_baseball/mitll_predictions.csv"),
            os.path.join(TEST_DIR_PATH, "data/22_handgeometry/mitll_predictions.csv"),
        ]

        try:
            cli_parser()
        except SystemExit:
            self.fail("score raised an exception")


if __name__ == "__main__":
    unittest.main()
