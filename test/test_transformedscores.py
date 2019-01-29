import pytest
import os
from d3m_outputs.metrics import *
from d3m_outputs.transformations import *
import numpy as np
import d3m_outputs.score
import pandas as pd

GROUND_TRUTH_MC = ['a', 'b', 'a', 'b', 'c', 'a', 'a', 'b', 'a', 'c', 'c', 'b']
PREDICTED_BEST_MC = ['a', 'b', 'a', 'b', 'c', 'a', 'a', 'b', 'a', 'c', 'c', 'b']
PREDICTED_OK_MC = ['a', 'b', 'a', 'c', 'a', 'a', 'a', 'b', 'b', 'c', 'c', 'b']
PREDICTED_BAD_MC = ['b', 'c', 'b', 'c', 'a', 'b', 'b', 'c', 'b', 'a', 'a', 'c']

GROUND_TRUTH_BC = [1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1]
GROUND_TRUTH_LABEL_BC = ['a', 'a', 'b', 'a', 'a', 'b', 'b', 'b', 'a', 'b', 'a', 'a']

PREDICTED_BEST_BC = [1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1]
PREDICTED_BEST_LABEL_BC = ['a', 'a', 'b', 'a', 'a', 'b', 'b', 'b', 'a', 'b', 'a', 'a']

PREDICTED_OK_BC = [1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0]
PREDICTED_OK_LABEL = ['a', 'a', 'a', 'b', 'a', 'b', 'a', 'a', 'b', 'b', 'a', 'b']

PREDICTED_OK_BC_B = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
PREDICTED_OK_BC_B_LABEL = ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a']

PREDICTED_BAD_BC = [0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0]
PREDICTED_BAD_LABEL_BC = ['b', 'b', 'a', 'b', 'b', 'a', 'a', 'a', 'b', 'a', 'b', 'b']

GROUND_TRUTH_RG = [0.5, 6, 2, 5.6]
PREDICTED_BEST_RG = [0.5, 6, 2, 5.6]
PREDICTED_OK_RG = [0.0, 7.2, 2.1, 4.7]
PREDICTED_BAD_RG = [5435, -45, 45646, 34]

class TestBinaryClass(object):
    """Test transformedscore for Binary Classification"""

    def testOK_accuracy(self):
        accuracy_score = accuracy(GROUND_TRUTH_BC, PREDICTED_OK_BC)
        assert accuracy_score == pytest.approx(0.5)
        assert find_metric("accuracy")(GROUND_TRUTH_BC, PREDICTED_OK_BC) == 0.5
        acc_transformation = apply_transformation("accuracy")
        assert acc_transformation.transform(accuracy_score) == 0.5

    def testOKB_accuracy(self):
        accuracy_score = accuracy(GROUND_TRUTH_BC, PREDICTED_OK_BC_B)
        assert accuracy_score == pytest.approx(7/12)
        assert find_metric("accuracy")(GROUND_TRUTH_BC, PREDICTED_OK_BC_B) == pytest.approx(7/12)
        acc_transformation = apply_transformation("accuracy")
        assert acc_transformation.transform(accuracy_score) == pytest.approx(7/12)

    def testBest_f1(self):
        """ Compute transformed score for f1"""
        f1_score = f1(GROUND_TRUTH_BC, PREDICTED_BEST_BC)
        assert f1_score == 1.0
        assert find_metric("f1")(GROUND_TRUTH_BC, PREDICTED_BEST_BC) == 1.0
        f1_transformation = apply_transformation("f1")
        assert f1_transformation.transform(f1_score) == 1

    def testOk_f1(self):
        f1_score = f1(GROUND_TRUTH_BC, PREDICTED_OK_BC)
        assert f1_score == pytest.approx(0.571428571428, 1e-10)
        f1_transformation = apply_transformation("f1")
        assert f1_transformation.transform(f1_score) == pytest.approx(0.571428571428, 1e-10)

    def testOk_precision(self):
        precision_score = precision(GROUND_TRUTH_BC, PREDICTED_OK_BC)
        assert precision_score == pytest.approx(0.57142857142857, 1e-10)
        precision_transformation = apply_transformation("precision")
        assert precision_transformation.transform(precision_score) == pytest.approx(0.57142857142857, 1e-10)

    def testOk_recall(self):
        recall_score = recall(GROUND_TRUTH_BC, PREDICTED_OK_BC)
        assert recall_score == pytest.approx(0.57142857142857, 1e-10)
        recall_transformation = apply_transformation("recall")
        assert recall_transformation.transform(recall_score) == pytest.approx(0.57142857142857, 1e-10)

    def testWrongInputs(self):
        with pytest.raises(ValueError):
            assert f1(GROUND_TRUTH_MC, PREDICTED_BEST_MC) == 1.0

class TestMultiClass(object):
    """ Test transformedscore for Multiclass Classification"""


class TestRegressionClass(object):
    """Test transformed score for """

    def testOk_mae(self):
        """Test transformed MAE"""
        mae_score = r2(GROUND_TRUTH_RG, PREDICTED_OK_RG)
        assert mae_score == pytest.approx(0.88542736505762865, 1e-10)
        mae_transformation = apply_transformation("meanAbsoluteError")
        assert mae_transformation.transform(mae_score) == pytest.approx(0.5841087186362,1e-10)

    def testMSE_1(self):
        mse_score_list = [9.528162521, 8.145583091, 8.145583091, 595.2379125, 13.96893799,
                          18.66023933, 29.57031075, 8.679340484, 45.30667017, 13.67148759,
                          608, 13.67148759, 9.726554, 9.726554, 7.757945897, 0.117305083,
                          0.117305083]
        expected_transformed_list = [1.455358e-04, 5.798588e-04, 5.798588e-04, 0.000000e+00, 1.715525e-06,
                                     1.573950e-08, 2.877698e-13, 3.400685e-04, 0.000000e+00, 2.309819e-06,
                                     0.000000e+00, 2.309819e-06, 1.193481e-04, 1.193481e-04, 8.543019e-04,
                                     9.414146e-01]
        for (mse_score, expected_score) in zip(mse_score_list, expected_transformed_list):
            computed_score = apply_transformation("meanSquaredError").transform(mse_score)
            assert computed_score == pytest.approx(expected_score, 1e-6)

    def testRMSE_1(self):
        rmse_score_list = [0.730243702, 0.368069081, 0.452083591, 1.40265164, 0.710223846,
                           0.368069081, 1.40265164, 0.368134653, 0.389765103, 0.743558301,
                           0.056568865, 0.37111655, 0.022074072]
        expected_transformed_list = [6.502825e-01, 8.180154e-01, 7.777310e-01, 3.947913e-01, 6.590988e-01,
                                     8.180154e-01, 3.947913e-01, 8.179837e-01, 8.075477e-01, 6.444531e-01,
                                     9.717231e-01, 8.165425e-01, 9.889634e-01]
        for (rmse_score, expected_score) in zip(rmse_score_list, expected_transformed_list):
            computed_score = apply_transformation("rootMeanSquaredError").transform(rmse_score)
            assert computed_score == pytest.approx(expected_score, 1e-6)

    def testMissingAndInfiniteScores(self):
        # This test may not be expected behavior and may need to be modified
        score_list = [float("-inf"), float('nan'), math.nan]
        expected_transformed_list = [0, 0, 0]
        for (score, expected_score) in zip(score_list, expected_transformed_list):
            computed_score = apply_transformation("rootMeanSquaredError").transform(score)
            assert computed_score == pytest.approx(expected_score, 1e-6)

class TestTransformations(object):
    """Test transformedscore transformations directly"""

    def testTransformedScore0_1Range(self):
        for i in np.arange(0, 1, 0.01):
            # put in a dummy target, metric, and baseline score to do testing
            score = d3m_outputs.score.Score('Hall_of_Fame', 'f1Macro', i, 0.5)
            transformation_true = CenterizedNormalizedScoreTransformation(0, 1, True)
            transformation_false = CenterizedNormalizedScoreTransformation(0, 1, False)
            assert score._transform(i, transformation_false) == pytest.approx(i, 1e-8)
            assert score._transform(i, transformation_true) == pytest.approx(1-i, 1e-8)


    def testTransformedScoreFiniteRange(self):
        a_vec = np.arange(-12, 6, 1.5)
        for a in a_vec:
            b_vec = np.arange(a+1, a+37, 9)
            for b in b_vec:
                for i in np.arange(a, b, 4):
                    # put in a dummy target, metric, and baseline score to do testing
                    score = d3m_outputs.score.Score('Hall_of_Fame', 'f1Macro', i, 0.5)
                    transformation_true = CenterizedNormalizedScoreTransformation(a, b, True)
                    transformation_false = CenterizedNormalizedScoreTransformation(a, b, False)
                    assert score._transform(i, transformation_false) == pytest.approx((i - a) / (b - a), 1e-8)
                    assert score._transform(i, transformation_true) == pytest.approx(1-((i - a) / (b - a)), 1e-8)



    def testTransformedScoreAEqualsB(self):
        # put in a dummy target, metric, and baseline score to do testing
        score = d3m_outputs.score.Score('Hall_of_Fame', 'f1Macro', 0.5, 1)
        transformation_false = CenterizedNormalizedScoreTransformation(1, 1, False)
        assert score._transform(0.5, transformation_false) == 1

    def testTransformedScoreAExceedsB(self):
        # put in a dummy target, metric, and baseline score to do testing
        score = d3m_outputs.score.Score('Hall_of_Fame', 'f1Macro', 0.5, 1)
        transformation_false = CenterizedNormalizedScoreTransformation(2, 1, False)
        assert pd.isnull(score._transform(0.5, transformation_false))

    def testTransformedScoreInfInf(self):
        for i in np.arange(-50, 50, 0.5):
            # put in a dummy target, metric, and baseline score to do testing
            score = d3m_outputs.score.Score('class', 'meanSquaredError', i, 0.5)
            transformation_true = InfInfScoreTransformation(None, None, True)
            transformation_false = InfInfScoreTransformation(None, None, False)
            assert score._transform(i, transformation_false) == pytest.approx((1 / (1 + math.exp(-i))), 1e-8)
            assert score._transform(i, transformation_true) == pytest.approx(1 - 1 / (1 + math.exp(-i)), 1e-8)

    def testTransformedScore0Inf(self):
        for i in np.arange(-50, 50, 0.5):
            score = d3m_outputs.score.Score('class', 'meanSquaredError', i, 0.5)
            transformation_true = ZeroInfScoreTransformation(None, None, True)
            transformation_false = ZeroInfScoreTransformation(None, None, False)
            assert score._transform(i, transformation_false) == pytest.approx(-1 + (2 / (1 + math.exp(-i))), 1e-8)
            assert score._transform(i, transformation_true) == pytest.approx(2 - 2 / (1 + math.exp(-i)), 1e-8)
