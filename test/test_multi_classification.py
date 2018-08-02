import unittest
import math

from d3m_outputs.metrics import f1_micro, f1_macro, roc_auc_micro, roc_auc_macro, jacc_sim, mxe, METRICS_DICT

GROUND_TRUTH = ['a', 'b', 'a', 'b', 'c', 'a', 'a', 'b', 'a', 'c', 'c', 'b']
PREDICTED_BEST = ['a', 'b', 'a', 'b', 'c', 'a', 'a', 'b', 'a', 'c', 'c', 'b']
PREDICTED_OK = ['a', 'b', 'a', 'c', 'a', 'a', 'a', 'b', 'b', 'c', 'c', 'b']
PREDICTED_BAD = ['b', 'c', 'b', 'c', 'a', 'b', 'b', 'c', 'b', 'a', 'a', 'c']
A = [1, 0, 0]
B = [0, 1, 0]
C = [0, 0, 1]
PREDICTED_BEST_PROB = [A, B, A, B, C, A, A, B, A, C, C, B]
PREDICTED_WORST_PROB = [B, C, B, C, A, B, B, C, B, A, A, C]
A = [.9, .05, .05]
B = [.05, .9, .05]
C = [.05, .05, .9]
PREDICTED_OK_PROB = [A, B, A, B, C, A, A, B, A, C, C, B]

## test cases with 4 classes
GROUND_TRUTH_4 = ['a', 'b', 'a', 'd', 'c', 'a', 'a', 'b', 'a', 'c', 'd','b']

A = [1, 0, 0, 0]
B = [0, 1, 0, 0]
C = [0, 0, 1, 0]
D = [0, 0, 0, 1]
PREDICTED_BEST_PROB_4 = [A, B, A, D, C, A, A, B, A, C, D, B]
PREDICTED_BEST_4 = ['a', 'b', 'a', 'd', 'c', 'a', 'a', 'b', 'a', 'c', 'd', 'b']

PREDICTED_WORST_PROB_4 = [B, C, C, A, D, B, B, C, B, D, A, C]
PREDICTED_WORST_4 = ['b', 'c', 'c', 'a', 'd', 'b', 'b', 'c', 'b', 'd', 'a', 'c']

A = [.9, .05, .025, .025]
B = [.05, .9, .025, .025]
C = [.05, .025, .9, .025]
D = [.05, .025, .025, .9]
PREDICTED_OK_PROB_4 = [A, B, A, D, C, A, A, B, A, C, D, B]
PREDICTED_OK_4 = ['b', 'b', 'a', 'd', 'c', 'a', 'a', 'b', 'a', 'c', 'd','b']

class TestMXE(unittest.TestCase):

    def runTest(self):
        self.testBest()
        self.testOk()
        self.testBad()

    def testBest(self):
        # a perfect cross entropy takes 0 bits
        self.assertAlmostEqual(0.0, mxe(GROUND_TRUTH, PREDICTED_BEST_PROB))
        self.assertAlmostEqual(0.0, METRICS_DICT['crossEntropy'](GROUND_TRUTH, PREDICTED_BEST_PROB))
        self.assertAlmostEqual(0.0, METRICS_DICT['crossEntropyNonBinarized'](GROUND_TRUTH, PREDICTED_BEST))

        self.assertAlmostEqual(0.0, mxe(GROUND_TRUTH_4, PREDICTED_BEST_PROB_4))
        self.assertAlmostEqual(0.0, METRICS_DICT['crossEntropy'](GROUND_TRUTH_4, PREDICTED_BEST_PROB_4))
        self.assertAlmostEqual(0.0, METRICS_DICT['crossEntropyNonBinarized'](GROUND_TRUTH_4, PREDICTED_BEST_4))


    def testOk(self):
        # takes the avg of the log predicted probabilities for the true class
        self.assertAlmostEqual(-math.log(.9), mxe(GROUND_TRUTH, PREDICTED_OK_PROB))
        self.assertAlmostEqual(-math.log(.9), METRICS_DICT['crossEntropy'](GROUND_TRUTH, PREDICTED_OK_PROB))
        self.assertAlmostEqual(math.log(5623.413251903499), METRICS_DICT['crossEntropyNonBinarized'](GROUND_TRUTH, PREDICTED_OK))


        self.assertAlmostEqual(-math.log(.9), mxe(GROUND_TRUTH_4, PREDICTED_OK_PROB_4))
        self.assertAlmostEqual(-math.log(.9), METRICS_DICT['crossEntropy'](GROUND_TRUTH_4, PREDICTED_OK_PROB_4))
        self.assertAlmostEqual(math.log(17.78279410038926), METRICS_DICT['crossEntropyNonBinarized'](GROUND_TRUTH_4, PREDICTED_OK_4))


    def testBad(self):
        eps = 1e-15 # log(0) is undefined, so mxe uses log(eps) instead of log(0)
        self.assertAlmostEqual(-math.log(eps), mxe(GROUND_TRUTH, PREDICTED_WORST_PROB))
        self.assertAlmostEqual(-math.log(eps), METRICS_DICT['crossEntropy'](GROUND_TRUTH, PREDICTED_WORST_PROB))
        self.assertAlmostEqual(-math.log(eps), METRICS_DICT['crossEntropyNonBinarized'](GROUND_TRUTH, PREDICTED_BAD))

        self.assertAlmostEqual(-math.log(eps), mxe(GROUND_TRUTH_4, PREDICTED_WORST_PROB_4))
        self.assertAlmostEqual(-math.log(eps), METRICS_DICT['crossEntropy'](GROUND_TRUTH_4, PREDICTED_WORST_PROB_4))
        self.assertAlmostEqual(-math.log(eps), METRICS_DICT['crossEntropyNonBinarized'](GROUND_TRUTH_4, PREDICTED_WORST_4))



class TestF1Micro(unittest.TestCase):
    def runTest(self):
        self.testBest()
        self.testOk()
        self.testBad()

    def testBest(self):
        self.assertEqual(1.0, f1_micro(GROUND_TRUTH, PREDICTED_BEST))
        self.assertEqual(1.0, METRICS_DICT['f1Micro'](GROUND_TRUTH, PREDICTED_BEST))

    def testOk(self):
        self.assertEqual(0.75, f1_micro(GROUND_TRUTH, PREDICTED_OK))
        self.assertEqual(0.75, METRICS_DICT['f1Micro'](GROUND_TRUTH, PREDICTED_OK))

    def testBad(self):
        self.assertEqual(0.0, f1_micro(GROUND_TRUTH, PREDICTED_BAD))
        self.assertEqual(0.0, METRICS_DICT['f1Micro'](GROUND_TRUTH, PREDICTED_BAD))


class TestF1Macro(unittest.TestCase):
    def runTest(self):
        self.testBest()
        self.testOk()
        self.testBad()

    def testBest(self):
        self.assertEqual(1.0, f1_macro(GROUND_TRUTH, PREDICTED_BEST))
        self.assertEqual(1.0, METRICS_DICT['f1Macro'](GROUND_TRUTH, PREDICTED_BEST))

    def testOk(self):
        self.assertEqual(0.73888888888888893, f1_macro(GROUND_TRUTH, PREDICTED_OK))
        self.assertEqual(0.73888888888888893, METRICS_DICT['f1Macro'](GROUND_TRUTH, PREDICTED_OK))

    def testBad(self):
        self.assertEqual(0.0, f1_macro(GROUND_TRUTH, PREDICTED_BAD))
        self.assertEqual(0.0, METRICS_DICT['f1Macro'](GROUND_TRUTH, PREDICTED_BAD))


class TestROCAUCMicro(unittest.TestCase):

    def runTest(self):
        self.testBest()
        self.testOk()
        self.testBad()

    def testBest(self):
        self.assertEqual(1.0, roc_auc_micro(GROUND_TRUTH, PREDICTED_BEST))
        self.assertEqual(1.0, METRICS_DICT['rocAucMicro'](GROUND_TRUTH, PREDICTED_BEST))

    def testOk(self):
        self.assertEqual(0.8125, roc_auc_micro(GROUND_TRUTH, PREDICTED_OK))
        self.assertEqual(0.8125, METRICS_DICT['rocAucMicro'](GROUND_TRUTH, PREDICTED_OK))

    def testBad(self):
        self.assertEqual(0.25, roc_auc_micro(GROUND_TRUTH, PREDICTED_BAD))
        self.assertEqual(0.25, METRICS_DICT['rocAucMicro'](GROUND_TRUTH, PREDICTED_BAD))


class TestROCAUCMacro(unittest.TestCase):

    def runTest(self):
        self.testBest()
        self.testOk()
        self.testBad()

    def testBest(self):
        self.assertEqual(1.0, roc_auc_macro(GROUND_TRUTH, PREDICTED_BEST))
        self.assertEqual(1.0, METRICS_DICT['rocAucMacro'](GROUND_TRUTH, PREDICTED_BEST))

    def testOk(self):
        self.assertEqual(0.80628306878306877, roc_auc_macro(GROUND_TRUTH, PREDICTED_OK))
        self.assertEqual(0.80628306878306877, METRICS_DICT['rocAucMacro'](GROUND_TRUTH, PREDICTED_OK))

    def testBad(self):
        self.assertEqual(0.25033068783068785, roc_auc_macro(GROUND_TRUTH, PREDICTED_BAD))
        self.assertEqual(0.25033068783068785, METRICS_DICT['rocAucMacro'](GROUND_TRUTH, PREDICTED_BAD))


class TestJaccSim(unittest.TestCase):

    def runTest(self):
        self.testBest()
        self.testOk()
        self.testBad()

    def testBest(self):
        self.assertEqual(1.0, jacc_sim(GROUND_TRUTH, PREDICTED_BEST))
        self.assertEqual(1.0, METRICS_DICT['jaccardSimilarityScore'](GROUND_TRUTH, PREDICTED_BEST))

    def testOk(self):
        self.assertEqual(0.75, jacc_sim(GROUND_TRUTH, PREDICTED_OK))
        self.assertEqual(0.75, METRICS_DICT['jaccardSimilarityScore'](GROUND_TRUTH, PREDICTED_OK))

    def testBad(self):
        self.assertEqual(0, jacc_sim(GROUND_TRUTH, PREDICTED_BAD))
        self.assertEqual(0, METRICS_DICT['jaccardSimilarityScore'](GROUND_TRUTH, PREDICTED_BAD))


if __name__ == '__main__':
    unittest.main()
