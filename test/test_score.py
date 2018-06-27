import unittest
from pathlib import Path

from d3m_outputs.score import Score, Scores


class TestScore(unittest.TestCase):
      
    def testJson(self):
        score = Score("Target", "F1_MACRO", 0.4, 0.6)
        expected_score = '{"target": "Target", "metric": "F1_MACRO", '
        expected_score += '"scorevalue": 0.4, "baseline_scorevalue": 0.6, ' 
        expected_score += '"transformed_scorevalue": "None", "transformed_baseline_scorevalue": "None", '
        expected_score += '"transformed_normalized_scorevalue": "None"}'
        self.assertEqual(str(score.json), expected_score)
        

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
        self.assertEqual(score.baseline_scorevalue, "None")
        self.assertEqual(score.transformed_scorevalue, "None")
        self.assertEqual(score.transformed_baseline_scorevalue, "None")
        self.assertEqual(score.transformed_normalized_scorevalue, "None")

class TestScores(unittest.TestCase):

    def testToJson(self):
        pass

        
if __name__ == '__main__':
    unittest.main()