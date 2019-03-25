import unittest

import numpy as np

from dval.metrics import apply_metric

GROUND_TRUTH = [
    ["img_00285.png", 500, 450, 550, 500],  # square, len 50
    ["img_00225.png", 100, 200, 300, 300],  # rectangle, w200 x h100
    ["img_00225.png", 100, 200, 50, 100],  # rectangle, w50 x h100
]

PREDICTED_BEST = [
    ["img_00285.png", 500, 450, 550, 500],  # square, len 50
    ["img_00225.png", 100, 200, 300, 300],  # rectangle, w200 x h100
    ["img_00225.png", 100, 200, 50, 100],  # rectangle, w50 x h100
]

PREDICTED_OK = [
    ["img_00285.png", 500, 450, 550, 500],  # square, len 50 p: 1, r: 1
    ["img_00225.png", 200, 200, 300, 300],  # square, len 100 p:1, r: 0.5
    ["img_00225.png", 125, 200, 75, 100],  # gt rectangle shifted x +25 p: 0.5, r: 0.5
]

PREDICTED_BAD = [
    ["img_00285.png", 0, 100, 300, 250],  # Non ovelapping
    ["img_00285.png", 0, 100, 300, 250],  # Non ovelapping
    ["img_00225.png", 0, 100, 300, 250],  # Non ovelapping
    ["img_00225.png", 0, 100, 300, 250],  # Non ovelapping
]

GROUND_TRUTH_STR = [
    ["img_00285.png", "500, 450, 550, 500"],  # square, len 50
    ["img_00225.png", "100, 200, 300, 300"],  # rectangle, w200 x h100
    ["img_00225.png", "100, 200, 50, 100"],  # rectangle, w50 x h100
]
PREDICTED_OK_STR = [
    ["img_00285.png", "500, 450, 550, 500"],  # square, len 50 p: 1, r: 1
    ["img_00225.png", "200, 200, 300, 300"],  # square, len 100 p:1, r: 0.5
    ["img_00225.png", "125, 200, 75, 100"],  # gt rectangle shifted x +25 p: 0.5, r: 0.5
]


class TestObjDetAvgP(unittest.TestCase):
    def runTest(self):
        self.testBest()
        self.testOk()
        self.testBad()

    def testBest(self):
        recall_array = np.array([1 / 3, 2 / 3, 2 / 3])
        precision_array = np.array([1 / 3, 2 / 3, 2 / 3])
        average_precision = 1.0

        computed_res = apply_metric("objectDetectionAP", PREDICTED_BEST, GROUND_TRUTH)

        computed_recall = computed_res[0]
        computed_precision = computed_res[1]
        computed_avg_precision = computed_res[2]

        np.testing.assert_array_almost_equal(
            recall_array, computed_recall, decimal=3, err_msg="Recalls don't match"
        )
        np.testing.assert_array_almost_equal(
            precision_array,
            computed_recall,
            decimal=3,
            err_msg="Precisions don't match",
        )
        np.testing.assert_array_almost_equal(
            recall_array,
            computed_recall,
            decimal=3,
            err_msg="AVG precisions don't match",
        )

    def testOk(self):
        recall_array = np.array([1 / 3, 2 / 3, 2 / 3])
        precision_array = np.array([1 / 3, 2 / 3, 2 / 3])
        average_precision = 2 / 3

        computed_res = apply_metric("objectDetectionAP", PREDICTED_OK, GROUND_TRUTH)
        computed_recall = computed_res[0]
        computed_precision = computed_res[1]
        computed_avg_precision = computed_res[2]

        np.testing.assert_array_almost_equal(
            recall_array, computed_recall, decimal=3, err_msg="Recalls don't match"
        )
        np.testing.assert_array_almost_equal(
            precision_array,
            computed_recall,
            decimal=3,
            err_msg="Precisions don't match",
        )
        np.testing.assert_array_almost_equal(
            recall_array,
            computed_recall,
            decimal=3,
            err_msg="AVG precisions don't match",
        )

    def testOkStr(self):
        recall_array = np.array([1 / 3, 2 / 3, 2 / 3])
        precision_array = np.array([1 / 3, 2 / 3, 2 / 3])
        average_precision = 2 / 3

        computed_res = apply_metric("objectDetectionAP", PREDICTED_OK_STR, GROUND_TRUTH)
        computed_recall = computed_res[0]
        computed_precision = computed_res[1]
        computed_avg_precision = computed_res[2]

        np.testing.assert_array_almost_equal(
            recall_array, computed_recall, decimal=3, err_msg="Recalls don't match"
        )
        np.testing.assert_array_almost_equal(
            precision_array,
            computed_recall,
            decimal=3,
            err_msg="Precisions don't match",
        )
        np.testing.assert_array_almost_equal(
            recall_array,
            computed_recall,
            decimal=3,
            err_msg="AVG precisions don't match",
        )

        computed_res = apply_metric("objectDetectionAP", PREDICTED_OK, GROUND_TRUTH_STR)
        computed_recall = computed_res[0]
        computed_precision = computed_res[1]
        computed_avg_precision = computed_res[2]

        np.testing.assert_array_almost_equal(
            recall_array, computed_recall, decimal=3, err_msg="Recalls don't match"
        )
        np.testing.assert_array_almost_equal(
            precision_array,
            computed_recall,
            decimal=3,
            err_msg="Precisions don't match",
        )
        np.testing.assert_array_almost_equal(
            recall_array,
            computed_recall,
            decimal=3,
            err_msg="AVG precisions don't match",
        )

    def testBad(self):
        recall_array = np.array([0.0, 0.0, 0.0, 0.0])
        precision_array = np.array([0.0, 0.0, 0.0, 0.0])
        average_precision = 0.0

        computed_res = apply_metric("objectDetectionAP", PREDICTED_BAD, GROUND_TRUTH)

        computed_recall = computed_res[0]
        computed_precision = computed_res[1]
        computed_avg_precision = computed_res[2]

        np.testing.assert_array_almost_equal(
            recall_array, computed_recall, decimal=3, err_msg="Recalls don't match"
        )
        np.testing.assert_array_almost_equal(
            precision_array,
            computed_recall,
            decimal=3,
            err_msg="Precisions don't match",
        )
        np.testing.assert_array_almost_equal(
            recall_array,
            computed_recall,
            decimal=3,
            err_msg="AVG precisions don't match",
        )


if __name__ == "__main__":
    unittest.main()
