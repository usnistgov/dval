import math
import unittest

import pytest

from d3m_outputs.metrics import f1_micro, f1_macro, roc_auc_micro, roc_auc_macro, jacc_sim, mxe, METRICS_DICT

GROUND_TRUTH_BBALL = [1, 0, 0, 2, 1]
PREDICTED_BBALL = [0, 0, 1, 2, 1]
PREDICTED_BBALL_PROBS = [[1,0,0], [1,0,0], [0,1,0], [0,0,1], [0,1,0]]


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
# Picked PREDICTED_OK_PROB to have same predictions as PREDICTED_OK
PREDICTED_OK_PROB = [A, B, A, C, A, A, A, B, B, C, C, B]

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
# Picked PREDICTED_OK_PROB_4 to have same predictions as PREDICTED_OK
PREDICTED_OK_PROB_4 = [B, B, A, D, C, A, A, B, A, C, D, B]
PREDICTED_OK_4 = ['b', 'b', 'a', 'd', 'c', 'a', 'a', 'b', 'a', 'c', 'd','b']

GROUND_TRUTH_REAL_EXAMPLE = ['value_a','value_b','value_a','value_b',
                             'value_c','value_a','value_a','value_b',
                             'value_a','value_c','value_c','value_b']


class TestMXE(unittest.TestCase):

    def runTest(self):
        self.testBest()
        self.testOk()
        self.testBad()
        self.testBaseballEx1()

    def testBest(self):
        # a perfect cross entropy takes 0 bits
        self.assertAlmostEqual(mxe(GROUND_TRUTH, PREDICTED_BEST_PROB), 0.0)
        self.assertAlmostEqual(METRICS_DICT['crossEntropy'](GROUND_TRUTH, PREDICTED_BEST_PROB), 0.0)
        self.assertAlmostEqual(METRICS_DICT['crossEntropyNonBinarized'](GROUND_TRUTH, PREDICTED_BEST), 0.0)

        self.assertAlmostEqual(mxe(GROUND_TRUTH_4, PREDICTED_BEST_PROB_4), 0.0)
        self.assertAlmostEqual(METRICS_DICT['crossEntropy'](GROUND_TRUTH_4, PREDICTED_BEST_PROB_4), 0.0)
        self.assertAlmostEqual(METRICS_DICT['crossEntropyNonBinarized'](GROUND_TRUTH_4, PREDICTED_BEST_4), 0.0)


    def testOk(self):
        # takes the avg of the log predicted probabilities for the true class
        ## note in this example, the class contribution toward the mxe is the same for all classes
        ## and the same is true for all trials, so we can compute it for a single trial.
        # ct is correct trial
        ct_mxe = math.log2(1/0.9)
        # it = incorrect trial
        it_mxe = math.log2(1/0.05)
        expected_OK_mxe_prob = (1/3)*((1/5)*(4*ct_mxe + 1*it_mxe) + (1/4)*(3*ct_mxe + 1*it_mxe) + (1/3)*(2*ct_mxe + 1*it_mxe))
        expected_OK_mxe_bin = (-math.log(2**-100,2)/3)*(1/5 + 1/4 + 1/3)
        self.assertAlmostEqual(mxe(GROUND_TRUTH, PREDICTED_OK_PROB), expected_OK_mxe_prob)
        self.assertAlmostEqual(METRICS_DICT['crossEntropy'](GROUND_TRUTH, PREDICTED_OK_PROB), expected_OK_mxe_prob)
        self.assertAlmostEqual(METRICS_DICT['crossEntropyNonBinarized'](GROUND_TRUTH, PREDICTED_OK), expected_OK_mxe_bin)

        ct4_mxe = math.log2(1 / 0.9)
        it4ab_mxe = math.log2(1 / 0.05)
        expected_OK4_mxe_prob = (1/4)*((1/5)*(4*ct4_mxe + 1*it4ab_mxe) + (1/3)*(3*ct4_mxe) + (1/3)*(3*ct4_mxe) + (1/2)*(2*ct4_mxe))
        expected_OK4_mxe_bin = (-math.log(2 ** -100, 2)/4) * (1/5)
        self.assertAlmostEqual(mxe(GROUND_TRUTH_4, PREDICTED_OK_PROB_4), expected_OK4_mxe_prob)
        self.assertAlmostEqual(METRICS_DICT['crossEntropy'](GROUND_TRUTH_4, PREDICTED_OK_PROB_4), expected_OK4_mxe_prob)
        self.assertAlmostEqual(METRICS_DICT['crossEntropyNonBinarized'](GROUND_TRUTH_4, PREDICTED_OK_4), expected_OK4_mxe_bin)

    def testOkRealExample(self):
        ct_mxe = math.log2(1/0.9)
        # it = incorrect trial
        it_mxe = math.log2(1/0.05)
        expected_OK_mxe_prob = (1/3)*((1/5)*(4*ct_mxe + 1*it_mxe) + (1/4)*(3*ct_mxe + 1*it_mxe) + (1/3)*(2*ct_mxe + 1*it_mxe))
        expected_OK_mxe_bin = (-math.log(2**-100,2)/3)*(1/5 + 1/4 + 1/3)
        self.assertAlmostEqual(mxe(GROUND_TRUTH_REAL_EXAMPLE, PREDICTED_OK_PROB), expected_OK_mxe_prob)
        self.assertAlmostEqual(METRICS_DICT['crossEntropy'](GROUND_TRUTH_REAL_EXAMPLE, PREDICTED_OK_PROB), expected_OK_mxe_prob)
        self.assertAlmostEqual(METRICS_DICT['crossEntropyNonBinarized'](GROUND_TRUTH_REAL_EXAMPLE, PREDICTED_OK), expected_OK_mxe_bin)

    def testBad(self):
        eps = 2**-100 # log2(0) is undefined, so mxe uses log2(eps) instead of log2(0) Log2 is the base, which is what prompts the epsilon
        self.assertAlmostEqual(mxe(GROUND_TRUTH, PREDICTED_WORST_PROB), -math.log2(eps))
        self.assertAlmostEqual(METRICS_DICT['crossEntropy'](GROUND_TRUTH, PREDICTED_WORST_PROB), -math.log2(eps))
        self.assertAlmostEqual(METRICS_DICT['crossEntropyNonBinarized'](GROUND_TRUTH, PREDICTED_BAD), -math.log2(eps))

        self.assertAlmostEqual(mxe(GROUND_TRUTH_4, PREDICTED_WORST_PROB_4), -math.log2(eps))
        self.assertAlmostEqual(METRICS_DICT['crossEntropy'](GROUND_TRUTH_4, PREDICTED_WORST_PROB_4), -math.log2(eps))
        self.assertAlmostEqual(METRICS_DICT['crossEntropyNonBinarized'](GROUND_TRUTH_4, PREDICTED_WORST_4), -math.log2(eps))

    def testBaseballEx1(self):
        expected_mxe = (-math.log(2**-100,2)/3)
        self.assertAlmostEqual(mxe(GROUND_TRUTH_BBALL,PREDICTED_BBALL_PROBS), expected_mxe)
        self.assertAlmostEqual(METRICS_DICT['crossEntropyNonBinarized'](GROUND_TRUTH_BBALL, PREDICTED_BBALL), expected_mxe)
        self.assertAlmostEquals(mxe(GROUND_TRUTH_BBALL,PREDICTED_BBALL_PROBS),METRICS_DICT['crossEntropyNonBinarized'](GROUND_TRUTH_BBALL, PREDICTED_BBALL), expected_mxe)

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
