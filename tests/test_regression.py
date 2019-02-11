import unittest
import numpy as np

from d3m_outputs.metrics import l2, avg_l2, l1, r2, METRICS_DICT

GROUND_TRUTH = [0.5, 6, 2, 5.6]
PREDICTED_BEST = [0.5, 6, 2, 5.6]
PREDICTED_OK = [0.0, 7.2, 2.1, 4.7]
PREDICTED_BAD = [5435, -45, 45646, 34]


class TestL2(unittest.TestCase):

    def runTest(self):
        self.testBest()
        self.testOk()
        self.testBad()

    def testBest(self):
        self.assertEqual(0.0, l2(GROUND_TRUTH, PREDICTED_BEST))

        self.assertEqual(0.0, METRICS_DICT['rootMeanSquaredError'](GROUND_TRUTH, PREDICTED_BEST))

    def testOk(self):
        self.assertAlmostEqual(0.79214897588774291, l2(GROUND_TRUTH, PREDICTED_OK))

        self.assertAlmostEqual(0.79214897588774291, METRICS_DICT['rootMeanSquaredError'](GROUND_TRUTH, PREDICTED_OK))

    def testBad(self):
        self.assertAlmostEqual(22983.210903885905, l2(GROUND_TRUTH, PREDICTED_BAD))

        self.assertAlmostEqual(22983.210903885905, METRICS_DICT['rootMeanSquaredError'](GROUND_TRUTH, PREDICTED_BAD))


class TestAvgL2(unittest.TestCase):

    def runTest(self):
        self.test()

    def test(self):
        gt = [GROUND_TRUTH, PREDICTED_OK]
        pred = [PREDICTED_BAD, PREDICTED_BEST]

        # We're expecting [[xi,yi],...] as an input,
        # Not [[xi...], [yi...]]
        gt = np.transpose(gt)
        pred = np.transpose(pred)

        score1 = l2(GROUND_TRUTH, PREDICTED_BAD)
        score2 = l2(PREDICTED_OK, PREDICTED_BEST)
        total_score = (score1 + score2) / 2

        self.assertAlmostEqual(total_score, avg_l2(gt, pred))

        self.assertAlmostEqual(total_score, METRICS_DICT['rootMeanSquaredErrorAvg'](gt, pred))


class TestL1(unittest.TestCase):

    def runTest(self):
        self.testBest()
        self.testOk()
        self.testBad()

    def testBest(self):
        self.assertEqual(0.0, l1(GROUND_TRUTH, PREDICTED_BEST))

        self.assertEqual(0.0, METRICS_DICT['meanAbsoluteError'](GROUND_TRUTH, PREDICTED_BEST))

    def testOk(self):
        self.assertAlmostEqual(0.67499999999999993, l1(GROUND_TRUTH, PREDICTED_OK))

        self.assertAlmostEqual(0.67499999999999993, METRICS_DICT['meanAbsoluteError'](GROUND_TRUTH, PREDICTED_OK))

    def testBad(self):
        self.assertAlmostEqual(12789.475, l1(GROUND_TRUTH, PREDICTED_BAD))

        self.assertAlmostEqual(12789.475, METRICS_DICT['meanAbsoluteError'](GROUND_TRUTH, PREDICTED_BAD))


class TestR2(unittest.TestCase):

    def runTest(self):
        self.testBest()
        self.testOk()
        self.testBad()

    def testBest(self):
        self.assertEqual(1.0, r2(GROUND_TRUTH, PREDICTED_BEST))

        self.assertEqual(1.0, METRICS_DICT['rSquared'](GROUND_TRUTH, PREDICTED_BEST))

    def testOk(self):
        self.assertAlmostEqual(0.88542736505762865, r2(GROUND_TRUTH, PREDICTED_OK))

        self.assertAlmostEqual(0.88542736505762865, METRICS_DICT['rSquared'](GROUND_TRUTH, PREDICTED_OK))

    def testBad(self):
        self.assertAlmostEqual(-96446966.194339842, r2(GROUND_TRUTH, PREDICTED_BAD))

        self.assertAlmostEqual(-96446966.194339842, METRICS_DICT['rSquared'](GROUND_TRUTH, PREDICTED_BAD))


if __name__ == '__main__':
    unittest.main()
