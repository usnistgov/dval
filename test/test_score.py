import unittest
from pathlib import Path

from d3m_outputs.score import Score, Scores
from d3m_outputs.transformations import METRIC_RANGES_DICT


class TestScore(unittest.TestCase):
      
    def testJson(self):
        score = Score("Target", "F1_MACRO", 0.4, 0.6)
        expected_score = '{"target": "Target", "metric": "F1_MACRO", '
        expected_score += '"scorevalue": 0.4, "baseline_scorevalue": 0.6, ' 
        expected_score += '"transformed_scorevalue": null, "transformed_baseline_scorevalue": null, '
        expected_score += '"transformed_normalized_scorevalue": null}'
        self.assertEqual(str(score.json), expected_score)

    def testNormalizeScore(self):
        score = Score("Target", "F1_MACRO", 0.4, 0.6)
        normalized_score = score._normalize(0.4, 0.6, METRIC_RANGES_DICT['f1Macro'])

        self.assertEqual(round(normalized_score,2), -0.33)

    def testNormalizeCost(self):
        score = Score("Target", "MEAN_SQUARED_ERROR", 0.4, 0.6)
        normalized_score = score._normalize(0.4, 0.6, METRIC_RANGES_DICT['meanSquaredError'])

        self.assertEqual(round(normalized_score,2), 0.33)

    def testTransformNormalize(self):
        score = Score("Target", "F1_MACRO", 0.4, 0.6)
        score.transform_normalize()

        self.assertEqual(score.scorevalue, 0.4)
        self.assertEqual(score.baseline_scorevalue, 0.6)
        self.assertEqual(score.transformed_scorevalue, 0.4)
        self.assertEqual(score.transformed_baseline_scorevalue, 0.6)
        self.assertEqual(round(score.transformed_normalized_scorevalue, 2), -0.33)

    def testTransformNormalizeWithoutBaseline(self):
        score = Score("Target", "F1_MACRO", 0.4, "None")
        score.transform_normalize()

        self.assertEqual(score.scorevalue, 0.4)
        self.assertEqual(score.baseline_scorevalue, None)
        self.assertEqual(score.transformed_scorevalue, 0.4)
        self.assertEqual(score.transformed_baseline_scorevalue, None)
        self.assertEqual(score.transformed_normalized_scorevalue, None)

    def testTransformNormalizeUnknownMetricWithoutBaseline(self):
        score = Score("Target", "Unknown_Metric", 0.4, "None")
        score.transform_normalize()

        self.assertEqual(score.scorevalue, 0.4)
        self.assertEqual(score.baseline_scorevalue, None)
        self.assertEqual(score.transformed_scorevalue, None)
        self.assertEqual(score.transformed_baseline_scorevalue, None)

    def testTransformNormalizeUnknownTransformation(self):
        METRIC_RANGES_DICT['metric'] = None

        score = Score("Target", "METRIC", 0.4, 0.6)
        score.transform_normalize()

        self.assertEqual(score.scorevalue, 0.4)
        self.assertEqual(score.baseline_scorevalue, 0.6)
        self.assertEqual(score.transformed_scorevalue, None)
        self.assertEqual(score.transformed_baseline_scorevalue, None)
        self.assertEqual(score.transformed_normalized_scorevalue, None)

        del METRIC_RANGES_DICT['metric']

    def testTransformNormalizeUnknownTransformationWithoutBaseline(self):
        METRIC_RANGES_DICT['metric'] = None

        score = Score("Target", "metric", 0.4, "None")
        score.transform_normalize()

        self.assertEqual(score.scorevalue, 0.4)
        self.assertEqual(score.baseline_scorevalue, None)
        self.assertEqual(score.transformed_scorevalue, None)
        self.assertEqual(score.transformed_baseline_scorevalue, None)
        self.assertEqual(score.transformed_normalized_scorevalue, None)

        del METRIC_RANGES_DICT['metric']

    def testTransformNormalizeTransformedBaselineEqualsZero(self):
        score = Score("Target", "MEAN_SQUARED_ERROR", 6985715.52, 6985715.52)
        score.transform_normalize()

        self.assertEqual(score.scorevalue, 6985715.52)
        self.assertEqual(score.baseline_scorevalue, 6985715.52)
        self.assertEqual(score.transformed_scorevalue, 0.0)
        self.assertEqual(score.transformed_baseline_scorevalue, 0.0)
        self.assertEqual(score.transformed_normalized_scorevalue, None)

class TestScores(unittest.TestCase):

    def testToJson(self):
        pass

        
if __name__ == '__main__':
    unittest.main()