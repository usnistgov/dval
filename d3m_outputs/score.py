import math
import json
from enum import Enum, auto
from collections import OrderedDict
from collections.abc import Collection

from .transformations import apply_transformation


class Score():
    """ Represents the score: according to a metric or transformed and normalized 
    """

    def __init__(self, target, metric, scorevalue, baseline_scorevalue):
        self.target = target
        self.metric = metric
        
        self.scorevalue = scorevalue
        self.baseline_scorevalue = baseline_scorevalue

        self.transformed_scorevalue = "None"
        self.transformed_baseline_scorevalue = "None"

        self.transformed_normalized_scorevalue = "None"

    @property
    def json(self):
        """ 
        :return: a Score instance Json formatted
        """
        return json.dumps(self.__dict__)

    def _transform(self, score, transformation):
        """ Transform any score to fit between [0,1]

        :return: transformed score
        """
        return transformation.transform(score)

    def _normalize(self, score, baseline_score, transformation):
        """ Normalize a score according to the baseline

        :param baseline_score: baseline score
        :type baseline_score: float
        """
        if not transformation.isCost:
            return (score - baseline_score) / abs(baseline_score)
        else:
            return (baseline_score - score) / abs(baseline_score)

    def transform_normalize(self):
        """ Transform and normalize the score to allow cross comparison
        """
        if self.baseline_scorevalue != 'None':
            transformation = apply_transformation(self.metric)
            if transformation:
                self.transformed_baseline_scorevalue = self._transform(self.baseline_scorevalue, transformation)
                self.transformed_scorevalue = self._transform(self.scorevalue, transformation)
                self.transformed_normalized_scorevalue = self._normalize(self.transformed_scorevalue, 
                    self.transformed_baseline_scorevalue, transformation)


class Scores(Collection):
    def __init__(self, scores):
        super().__init__()
        self.scores = scores

    def __iter__(self):
        return iter(self.scores)

    def __contains__(self, score):
        return score in self.scores

    def __len__(self):
        return len(self.scores)

    def __repr__(self):
        return self.scores.__repr__()

    def to_json(self, fileobject=None):
        scores_to_json = [score.__dict__ for score in self.scores]
        if fileobject is not None:
            json.dump(scores_to_json, fileobject, sort_keys=True, indent=4)
        return json.dumps(scores_to_json, sort_keys=True, indent=4)


