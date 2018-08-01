import pytest
import os
from d3m_outputs.metrics import *
from d3m_outputs.transformations import *

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

PREDICTED_BAD_BC = [0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0]
PREDICTED_BAD_LABEL_BC = ['b', 'b', 'a', 'b', 'b', 'a', 'a', 'a', 'b', 'a', 'b', 'b']

GROUND_TRUTH_RG = [0.5, 6, 2, 5.6]
PREDICTED_BEST_RG = [0.5, 6, 2, 5.6]
PREDICTED_OK_RG = [0.0, 7.2, 2.1, 4.7]
PREDICTED_BAD_RG = [5435, -45, 45646, 34]

class TestBinaryClass(object):
    """Test transformedscore for Binary Classification"""

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
