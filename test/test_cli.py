import unittest
import sys

from d3m_outputs.cli import cli_parser, cmd_valid_pipeline


class TestCmdValidPipelines(unittest.TestCase):

    def testFileNotFound(self):
        sys.argv[1:] = ['valid_pipelines', '']
        with self.assertRaises(Exception):
            cli_parser()

    def testNotValidate(self):
        sys.argv[1:] = ['valid_pipelines', 'test/pipelinelogs/missing_rank.json']
        with self.assertRaises(SystemExit):
            cli_parser()

    def testOk(self):
        sys.argv[1:] = ['valid_pipelines', 'test/pipelinelogs/correct_pipeline.json']
        try:
            cli_parser()
        except Exception:
           self.fail("valid_pipelines raised an exception")


class TestCmdValidPredictions(unittest.TestCase):

    def testFileNotFound(self):
        sys.argv[1:] = ['valid_predictions', '-d', 'test/data/185_baseball', '']
        with self.assertRaises(SystemExit):
            cli_parser()

    def testDirectoryNotFound(self):
        sys.argv[1:] = ['valid_predictions', '-d', '', 'test/data/185_baseball/mitll_predictions.csv']
        with self.assertRaises(SystemExit):
            cli_parser()

    def testOk(self):
        sys.argv[1:] = ['valid_predictions', '-d', 'test/data/185_baseball',
                        'test/data/185_baseball/mitll_predictions.csv']
        try:
            cli_parser()
        except Exception:
            self.fail("valid_predictions raised an exception")


class TestCmdScore(unittest.TestCase):

    def testOk(self):
        sys.argv[1:] = ['score', '-d','test/data/185_baseball', '-g', 'test/data/185_baseball/targets.csv',
                        '--validation', 'test/data/185_baseball/mitll_predictions.csv']
        try:
            cli_parser()
        except SystemExit:
            self.fail("score raised an exception")

    def testScoreDirectoryNotFound(self):
        sys.argv[1:] = ['score', '-d', '', '-g', 'test/data/185_baseball/targets.csv',
                        '--validation', 'test/data/185_baseball/mitll_predictions.csv']

        #with self.assertRaises(Exception):
        #    cli_parser()

    def testTargetNotFound(self):
        sys.argv[1:] = ['score', '-d', 'test/data/185_baseball', '-g', '',
                        '--validation', 'test/data/185_baseball/mitll_predictions.csv']

        try:
            cli_parser()
        except SystemExit:
            self.fail("score raised an exception")

    def testPredictionNotFound(self):
        sys.argv[1:] = ['score', '-d', 'test/data/185_baseball', '-g', 'test/data/185_baseball/targets.csv',
                        '--validation', '']

        #with self.assertRaises(Exception):
        #    cli_parser()

    def testMultiplePredictionFiles(self):
        sys.argv[1:] = ['score', '-d', 'test/data/185_baseball', '-g', 'test/data/185_baseball/targets.csv',
                        '--validation', 'test/data/185_baseball/mitll_predictions.csv',
                        'test/data/22_handgeometry/mitll_predictions.csv']

        try:
            cli_parser()
        except SystemExit:
            self.fail("score raised an exception")


class TestCmdGenerateTestScript(unittest.TestCase):

    def testCmdGenerateTestScript(self):
        pass


class TestCmdValidatePostSearch(unittest.TestCase):

    def testOk(self):
        sys.argv[1:] = ['validate_post_search', '-p', 'test/postsearch_validation/valid_pipelines', '-e'
                        'test/postsearch_validation/executables']
        try:
            cli_parser()
        except SystemExit:
            self.fail("valid_post_search raised an exception")

    def testInvalidPipelineFolder(self):
        sys.argv[1:] = ['validate_post_search', '-p', 'test/postsearch_validation/pipelines', '-e'
                        'test/postsearch_validation/executables']

        with self.assertRaises(SystemExit):
            cli_parser()

    def testInvalidExecutableFolder(self):
        #TODO
        pass


if __name__ == '__main__':
    unittest.main()
