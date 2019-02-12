import pytest
import os
from d3m_outputs.metrics import *
from d3m_outputs.transformations import *
import d3m_outputs.score
import numpy as np
import math
import pandas as pd


class TestNormalizations(object):
    def testNormalizations(self):
        for sc in np.arange(0, 2, 0.05):
            for bsc in np.arange(0.5, 1, 0.05):
                # put in a dummy target and metric to do testing
                score = d3m_outputs.score.Score("Hall_of_Fame", "f1Macro", sc, bsc)
                transformation_true = CenterizedNormalizedScoreTransformation(
                    0, 1, True
                )
                transformation_false = CenterizedNormalizedScoreTransformation(
                    0, 1, False
                )
                assert score._normalize(sc, bsc, transformation_true) == pytest.approx(
                    (bsc - sc) / abs(bsc), 1e-8
                )
                assert score._normalize(sc, bsc, transformation_false) == pytest.approx(
                    (sc - bsc) / abs(bsc), 1e-8
                )
        score_nan = d3m_outputs.score.Score("Hall_of_Fame", "f1Macro", 0.5, 0)
        assert score_nan._normalize(0.5, 0, False) is None
