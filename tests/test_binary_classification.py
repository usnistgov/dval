import unittest

from d3m_outputs.metrics import accuracy, f1, roc_auc, METRICS_DICT

GROUND_TRUTH = [1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1]
GROUND_TRUTH_LABEL = ["a", "a", "b", "a", "a", "b", "b", "b", "a", "b", "a", "a"]

PREDICTED_BEST = [1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1]
PREDICTED_BEST_LABEL = ["a", "a", "b", "a", "a", "b", "b", "b", "a", "b", "a", "a"]

PREDICTED_OK = [1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0]
PREDICTED_OK_LABEL = ["a", "a", "a", "b", "a", "b", "a", "a", "b", "b", "a", "b"]

PREDICTED_OK_B = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
PREDICTED_OK_B_LABEL = ["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a"]

PREDICTED_BAD = [0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0]
PREDICTED_BAD_LABEL = ["b", "b", "a", "b", "b", "a", "a", "a", "b", "a", "b", "b"]


class TestAccuracyIndicator(unittest.TestCase):
    def testBest(self):
        self.assertEqual(1.0, accuracy(GROUND_TRUTH, PREDICTED_BEST))
        self.assertEqual(1.0, METRICS_DICT["accuracy"](GROUND_TRUTH, PREDICTED_BEST))

    def testOk(self):
        self.assertEqual(0.5, accuracy(GROUND_TRUTH, PREDICTED_OK))
        self.assertEqual(0.5, METRICS_DICT["accuracy"](GROUND_TRUTH, PREDICTED_OK))

    def testOkB(self):
        self.assertEqual(accuracy(GROUND_TRUTH, PREDICTED_OK_B), (7 / 12))
        self.assertEqual(
            METRICS_DICT["accuracy"](GROUND_TRUTH, PREDICTED_OK_B), (7 / 12)
        )

    def testBad(self):
        self.assertEqual(0.0, accuracy(GROUND_TRUTH, PREDICTED_BAD))
        self.assertEqual(0.0, METRICS_DICT["accuracy"](GROUND_TRUTH, PREDICTED_BAD))


class TestAccuracyLabels(unittest.TestCase):
    def testBest(self):
        self.assertEqual(1.0, accuracy(GROUND_TRUTH_LABEL, PREDICTED_BEST_LABEL))
        self.assertEqual(
            1.0, METRICS_DICT["accuracy"](GROUND_TRUTH_LABEL, PREDICTED_BEST_LABEL)
        )

    def testOk(self):
        self.assertEqual(0.5, accuracy(GROUND_TRUTH_LABEL, PREDICTED_OK_LABEL))
        self.assertEqual(
            0.5, METRICS_DICT["accuracy"](GROUND_TRUTH_LABEL, PREDICTED_OK_LABEL)
        )

    def testBad(self):
        self.assertEqual(0.0, accuracy(GROUND_TRUTH_LABEL, PREDICTED_BAD_LABEL))
        self.assertEqual(
            0.0, METRICS_DICT["accuracy"](GROUND_TRUTH_LABEL, PREDICTED_BAD_LABEL)
        )


class TestF1Indicator(unittest.TestCase):
    def testBest(self):
        self.assertEqual(1.0, f1(GROUND_TRUTH, PREDICTED_BEST))
        self.assertEqual(1.0, METRICS_DICT["f1"](GROUND_TRUTH, PREDICTED_BEST))

    def testBestLabel0(self):
        self.assertEqual(1.0, f1(GROUND_TRUTH, PREDICTED_BEST, pos_label=0))
        self.assertEqual(
            1.0, METRICS_DICT["f1"](GROUND_TRUTH, PREDICTED_BEST, pos_label=0)
        )

    def testOk(self):
        self.assertAlmostEqual(0.571428571428, f1(GROUND_TRUTH, PREDICTED_OK))
        self.assertAlmostEqual(
            0.571428571428, METRICS_DICT["f1"](GROUND_TRUTH, PREDICTED_OK)
        )

    def testOkLabel0(self):
        self.assertAlmostEqual(0.4, f1(GROUND_TRUTH, PREDICTED_OK, pos_label=0))
        self.assertAlmostEqual(
            0.4, METRICS_DICT["f1"](GROUND_TRUTH, PREDICTED_OK, pos_label=0)
        )

    def testBad(self):
        self.assertEqual(0.0, f1(GROUND_TRUTH, PREDICTED_BAD))
        self.assertEqual(0.0, METRICS_DICT["f1"](GROUND_TRUTH, PREDICTED_BAD))

    def testBadLabel0(self):
        self.assertEqual(0.0, f1(GROUND_TRUTH, PREDICTED_BAD, pos_label=0))
        self.assertEqual(
            0.0, METRICS_DICT["f1"](GROUND_TRUTH, PREDICTED_BAD, pos_label=0)
        )


class TestF1Labels(unittest.TestCase):
    def testBestLabelb(self):
        self.assertEqual(
            1.0, f1(GROUND_TRUTH_LABEL, PREDICTED_BEST_LABEL, pos_label="b")
        )
        self.assertEqual(
            1.0,
            METRICS_DICT["f1"](GROUND_TRUTH_LABEL, PREDICTED_BEST_LABEL, pos_label="b"),
        )

    def testBestLabela(self):
        self.assertEqual(
            1.0, f1(GROUND_TRUTH_LABEL, PREDICTED_BEST_LABEL, pos_label="a")
        )
        self.assertEqual(
            1.0,
            METRICS_DICT["f1"](GROUND_TRUTH_LABEL, PREDICTED_BEST_LABEL, pos_label="a"),
        )

    def testOkLabelb(self):
        self.assertEqual(
            0.40000000000000008,
            f1(GROUND_TRUTH_LABEL, PREDICTED_OK_LABEL, pos_label="b"),
        )
        self.assertEqual(
            0.40000000000000008,
            METRICS_DICT["f1"](GROUND_TRUTH_LABEL, PREDICTED_OK_LABEL, pos_label="b"),
        )

    def testOkLabela(self):
        self.assertEqual(
            0.5714285714285714,
            f1(GROUND_TRUTH_LABEL, PREDICTED_OK_LABEL, pos_label="a"),
        )
        self.assertEqual(
            0.5714285714285714,
            METRICS_DICT["f1"](GROUND_TRUTH_LABEL, PREDICTED_OK_LABEL, pos_label="a"),
        )

    def testBadLabelb(self):
        self.assertEqual(
            0.0, f1(GROUND_TRUTH_LABEL, PREDICTED_BAD_LABEL, pos_label="b")
        )
        self.assertEqual(
            0.0,
            METRICS_DICT["f1"](GROUND_TRUTH_LABEL, PREDICTED_BAD_LABEL, pos_label="b"),
        )

    def testBadLabela(self):
        self.assertEqual(
            0.0, f1(GROUND_TRUTH_LABEL, PREDICTED_BAD_LABEL, pos_label="a")
        )
        self.assertEqual(
            0.0,
            METRICS_DICT["f1"](GROUND_TRUTH_LABEL, PREDICTED_BAD_LABEL, pos_label="a"),
        )


class TestROCAUCIndicator(unittest.TestCase):
    def testBest(self):
        self.assertEqual(1.0, roc_auc(GROUND_TRUTH, PREDICTED_BEST))
        self.assertEqual(1.0, METRICS_DICT["rocAuc"](GROUND_TRUTH, PREDICTED_BEST))

    def testOk(self):
        self.assertAlmostEqual(0.48571428571428565, roc_auc(GROUND_TRUTH, PREDICTED_OK))
        self.assertAlmostEqual(
            0.48571428571428565, METRICS_DICT["rocAuc"](GROUND_TRUTH, PREDICTED_OK)
        )

    def testBad(self):
        self.assertEqual(0.0, roc_auc(GROUND_TRUTH, PREDICTED_BAD))
        self.assertEqual(0.0, METRICS_DICT["rocAuc"](GROUND_TRUTH, PREDICTED_BAD))


class TestROCAUCLabels(unittest.TestCase):
    def testBestLabela(self):
        self.assertEqual(
            1.0, roc_auc(GROUND_TRUTH_LABEL, PREDICTED_BEST_LABEL, pos_label="a")
        )
        self.assertEqual(
            1.0,
            METRICS_DICT["rocAuc"](
                GROUND_TRUTH_LABEL, PREDICTED_BEST_LABEL, pos_label="a"
            ),
        )

    def testOkLabela(self):
        self.assertAlmostEqual(
            0.48571428571428565,
            roc_auc(GROUND_TRUTH_LABEL, PREDICTED_OK_LABEL, pos_label="a"),
        )
        self.assertAlmostEqual(
            0.48571428571428565,
            METRICS_DICT["rocAuc"](
                GROUND_TRUTH_LABEL, PREDICTED_OK_LABEL, pos_label="a"
            ),
        )

    def testOkLabelb(self):
        self.assertAlmostEqual(
            0.48571428571428565,
            roc_auc(GROUND_TRUTH_LABEL, PREDICTED_OK_LABEL, pos_label="b"),
        )
        self.assertAlmostEqual(
            0.48571428571428565,
            METRICS_DICT["rocAuc"](
                GROUND_TRUTH_LABEL, PREDICTED_OK_LABEL, pos_label="b"
            ),
        )


if __name__ == "__main__":
    unittest.main()
