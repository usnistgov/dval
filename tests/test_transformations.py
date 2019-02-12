import unittest

from d3m_outputs.transformations import (
    CenterizedNormalizedScoreTransformation,
    InfInfScoreTransformation,
    ZeroInfScoreTransformation,
)


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
        transformation = InfInfScoreTransformation(False)
        self.assertEqual(round(transformation.transform(-99), 2), 0.0)

        transformation = InfInfScoreTransformation(False)
        self.assertEqual(round(transformation.transform(99), 2), 1.0)

        transformation = InfInfScoreTransformation(True)
        self.assertEqual(round(transformation.transform(-99), 2), 1.0)

        transformation = InfInfScoreTransformation(True)
        self.assertEqual(round(transformation.transform(99), 2), 0.0)

        transformation = InfInfScoreTransformation(False)
        self.assertEqual(round(transformation.transform(0), 2), 0.5)

        transformation = InfInfScoreTransformation(True)
        self.assertEqual(round(transformation.transform(0), 2), 0.5)

        transformation = InfInfScoreTransformation(False)
        self.assertEqual(round(transformation.transform(5), 2), 0.99)

        transformation = InfInfScoreTransformation(True)
        self.assertEqual(round(transformation.transform(5), 2), 0.01)

        transformation = InfInfScoreTransformation(False)
        self.assertEqual(round(transformation.transform(1), 2), 0.73)

        transformation = InfInfScoreTransformation(True)
        self.assertEqual(round(transformation.transform(1), 2), 0.27)

        transformation = InfInfScoreTransformation(False)
        self.assertEqual(round(transformation.transform(-1), 2), 0.27)

        transformation = InfInfScoreTransformation(True)
        self.assertEqual(round(transformation.transform(-1), 2), 0.73)

    def testZeroInfScoreTransformation(self):
        transformation = ZeroInfScoreTransformation(False)
        self.assertEqual(round(transformation.transform(0), 2), 0.0)

        transformation = ZeroInfScoreTransformation(False)
        self.assertEqual(round(transformation.transform(99), 2), 1.0)

        transformation = ZeroInfScoreTransformation(True)
        self.assertEqual(round(transformation.transform(0), 2), 1.0)

        transformation = ZeroInfScoreTransformation(True)
        self.assertEqual(round(transformation.transform(99), 2), 0.0)

        transformation = ZeroInfScoreTransformation(False)
        self.assertEqual(round(transformation.transform(5), 2), 0.99)

        transformation = ZeroInfScoreTransformation(True)
        self.assertEqual(round(transformation.transform(5), 2), 0.01)

        transformation = ZeroInfScoreTransformation(False)
        self.assertEqual(round(transformation.transform(1), 2), 0.46)

        transformation = ZeroInfScoreTransformation(True)
        self.assertEqual(round(transformation.transform(1), 2), 0.54)


if __name__ == "__main__":
    unittest.main()
