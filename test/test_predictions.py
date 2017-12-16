import unittest
from pathlib import Path

from predictions import Predictions

class TestPredictions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_cases = dict()

        path = Path(__file__).parent / 'data'
        directories = (i for i in path.iterdir() if i.is_dir())

        for d in directories:
            result_file = d / 'mitll_predictions.csv'
            cls.test_cases[d.name] = Predictions(
                result_file_path=result_file,
                path_to_score_root=d
            )


    def testIsValid(self):
        for name, test_case in self.test_cases.items():
            self.assertTrue(test_case.is_valid())


    def testScore(self):
        for name, test_case in self.test_cases.items():
            scores = test_case.score(test_case.score_root / 'targets.csv')
            for score in scores:
                try:
                    float(score.scorevalue)
                except AssertionError:
                    self.fail(f'Score value {score.scorevalue} is could not be cast to float.'
                              f'Found type {type(score.scorevalue)}')
                self.assertGreaterEqual(score.scorevalue, 0.)


if __name__ == '__main__':
    unittest.main()
