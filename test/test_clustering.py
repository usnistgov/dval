import unittest

from ..metrics import norm_mut_info, METRICS_DICT

GROUND_TRUTH = ['a', 'b', 'a', 'b', 'c', 'a', 'a', 'b', 'a', 'c', 'c', 'b']
PREDICTED_BEST = ['a', 'b', 'a', 'b', 'c', 'a', 'a', 'b', 'a', 'c', 'c', 'b']
PREDICTED_OK = ['a', 'b', 'a', 'c', 'a', 'a', 'a', 'b', 'b', 'c', 'c', 'b']
PREDICTED_BAD = ['b', 'c', 'b', 'c', 'a', 'b', 'b', 'c', 'b', 'a', 'a', 'c']


class TestNormMutInfo(unittest.TestCase):
    
    def runTest(self):
        self.testBest()
        self.testOk()
        self.testBad()


    def testBest(self):
        self.assertEqual(1.0, norm_mut_info(GROUND_TRUTH, PREDICTED_BEST))
        self.assertEqual(1.0, METRICS_DICT['normalizedMutualInformation'](GROUND_TRUTH, PREDICTED_BEST))


    def testOk(self):
        self.assertEqual(0.48487648752570484, norm_mut_info(GROUND_TRUTH, PREDICTED_OK))
        self.assertEqual(0.48487648752570484, METRICS_DICT['normalizedMutualInformation'](GROUND_TRUTH, PREDICTED_OK))


    def testBad(self):
        self.assertEqual(1.0, norm_mut_info(GROUND_TRUTH, PREDICTED_BAD))
        self.assertEqual(1.0, METRICS_DICT['normalizedMutualInformation'](GROUND_TRUTH, PREDICTED_BAD))


if __name__ == '__main__':
    unittest.main()
