import unittest
from pathlib import Path

from d3m_outputs.transformations import CenterizedNormalizedScoreTransformation, \
InfInfScoreTransformation, ZeroInfScoreTransformation


class TestTransformation(unittest.TestCase):
      
    def testCenterizedNormalizedScoreTransformation(self):
        transformation = CenterizedNormalizedScoreTransformation(0, 1, False)
        self.assertEqual(transformation.transform(0.4), 0.4)

        transformation = CenterizedNormalizedScoreTransformation(0, 1, True)
        self.assertEqual(transformation.transform(0.4), 0.6)

        transformation = CenterizedNormalizedScoreTransformation(-3, 7, False)
        self.assertAlmostEqual(transformation.transform(0.4), 0.34)

        transformation = CenterizedNormalizedScoreTransformation(-3, 7, True)
        self.assertEqual(transformation.transform(0.4), 0.66)
        

    def testInfInfScoreTransformation(self):
        transformation = InfInfScoreTransformation(None, None, False)
        self.assertEqual(round(transformation.transform(-99), 2), 0.0)

        transformation = InfInfScoreTransformation(None, None, False)
        self.assertEqual(round(transformation.transform(99),2), 1.0)

        transformation = InfInfScoreTransformation(None, None, True)
        self.assertEqual(round(transformation.transform(-99),2), 1.0)

        transformation = InfInfScoreTransformation(None, None, True)
        self.assertEqual(round(transformation.transform(99),2), 0.0)

        transformation = InfInfScoreTransformation(None, None, False)
        self.assertEqual(round(transformation.transform(0),2), 0.5)

        transformation = InfInfScoreTransformation(None, None, True)
        self.assertEqual(round(transformation.transform(0),2), 0.5)

    def testZeroInfScoreTransformation(self):
        transformation = ZeroInfScoreTransformation(None, None, False)
        self.assertEqual(round(transformation.transform(0), 2), 0.0)

        transformation = ZeroInfScoreTransformation(None, None, False)
        self.assertEqual(round(transformation.transform(99),2), 1.0)

        transformation = ZeroInfScoreTransformation(None, None, True)
        self.assertEqual(round(transformation.transform(0),2), 1.0)

        transformation = ZeroInfScoreTransformation(None, None, True)
        self.assertEqual(round(transformation.transform(99),2), 0.0)
        


if __name__ == '__main__':
    unittest.main()