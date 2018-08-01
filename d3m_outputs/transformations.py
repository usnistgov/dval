import abc
import math


class Transformation():
    __metaclass__ = abc.ABCMeta

    def __init__(self, left_interval, right_interval, isCost):
        self.left_interval = left_interval
        self.right_interval = right_interval
        self.isCost = isCost

    @abc.abstractmethod
    def transform(self, score):
        return

class CenterizedNormalizedScoreTransformation(Transformation):

    def __init__(self, left_interval, right_interval, isCost):
        super(CenterizedNormalizedScoreTransformation, self).__init__(left_interval, right_interval, isCost)

    def transform(self, score):
        t_score = (score - self.left_interval)/(self.right_interval - self.left_interval)
        if self.isCost:
            t_score = 1 - t_score
        return t_score

    
class InfInfScoreTransformation(Transformation):

    def __init__(self, left_interval, right_interval, isCost):
        super(InfInfScoreTransformation, self).__init__(left_interval, right_interval, isCost)

    def transform(self, score):
        if not self.isCost:
            return 1/(1+math.exp(-score))
        else:
            return 1 - 1/(1+math.exp(-score))


class ZeroInfScoreTransformation(Transformation):

    def __init__(self, left_interval, right_interval, isCost):
        super(ZeroInfScoreTransformation, self).__init__(left_interval, right_interval, isCost)

    def transform(self, score):
        if not self.isCost:
            return 2/(1+math.exp(-score)) - 1
        else:
            return 2 - 2/(1+math.exp(-score))


METRIC_RANGES_DICT = {
    'accuracy': CenterizedNormalizedScoreTransformation(0, 1, True),
    'f1': CenterizedNormalizedScoreTransformation(0, 1, False),
    'f1Micro': CenterizedNormalizedScoreTransformation(0, 1, False),
    'f1Macro': CenterizedNormalizedScoreTransformation(0, 1, False),
    'rocAuc': CenterizedNormalizedScoreTransformation(0, 1, False),
    'rocAucMicro': CenterizedNormalizedScoreTransformation(0, 1, False),
    'rocAucMacro': CenterizedNormalizedScoreTransformation(0, 1, False),
    'meanSquaredError': ZeroInfScoreTransformation(0, None, True),
    'rootMeanSquaredError': ZeroInfScoreTransformation(0, None, True),
    'rootMeanSquaredErrorAvg': ZeroInfScoreTransformation(0, None, True),
    'meanAbsoluteError': ZeroInfScoreTransformation(0, None, True),
    'rSquared': None,
    'normalizedMutualInformation': CenterizedNormalizedScoreTransformation(0, 1, False),
    'jaccardSimilarityScore': None,
    'precisionAtTopK': None,
    'objectDetectionAP': None,
    'object_detection_average_precision': None,
    'precision': CenterizedNormalizedScoreTransformation(0, 1, False),
    'recall': CenterizedNormalizedScoreTransformation(0, 1, False)
}

def apply_transformation(metric, *args, **kwargs):
    def transform_string(string):
        return string.lower().replace('_', '')

    reference = {transform_string(k): _ for k,_ in METRIC_RANGES_DICT.items()}
    return reference[transform_string(metric)]
