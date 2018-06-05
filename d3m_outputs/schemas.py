"""
Representations of v3 D3M schemas and data structures.
"""

import json
from pathlib import Path
import os

import pandas

from d3m.metadata.problem import parse_problem_description
from d3m.container.dataset import Dataset


class DatasetSchema:
    """
    Adapter class representing a v3 Dataset Schema
    """

    def __init__(self, filepath):
        # fullpath = 'file://{dataset_doc_path}'.format(dataset_doc_path=os.path.abspath(uri))
        # self.dataset = Dataset.load(fullpath)
        self.filepath = filepath
        with open(filepath) as schema:
            self.jdata = json.load(schema)

    @property
    def _learningDataColumns(self):
        for dr in self.jdata['dataResources']:
            if dr['resPath'] == 'tables/learningData.csv':
                return dr['columns']

    @property
    def index_name(self):
        """
        :return: the first index column found in the dataset schema
        """
        indexcolumns = (c['colName'] for c in self._learningDataColumns if 'index' in c['role'])
        # assuming one index
        return indexcolumns.__next__()

    def target_types(self, targets):
        """
        Search the dataset schema for the expected types of targets
        :param targets: target names
        :type targets: list(str)
        :return: a dict of {targetName: targetType}
        :rtype: dict
        """
        expected_fields = dict()

        target_colids = [t['column_index'] for t in targets]
        for c in self._learningDataColumns:
            if c['colIndex'] in target_colids:
                expected_fields[c['colName']] = c['colType']
        return expected_fields


class ProblemSchema:
    """
    Adapter class representing a v3 Problem Schema
    """

    def __init__(self, uri):
        self.filepath = uri
        self.problem = parse_problem_description(self.filepath)

    # TODO test
    @property
    def targets(self):
        """"
        :return: list of dictionaries describing the targets
        ONLY SUPPORTS one dataset and target, i.e. ['inputs']['data'] of length 1
        """
        return self.problem['inputs'][0]['targets']

    # TODO test
    @property
    def target_names(self):
        """
        :return: List of target names
        """
        return [t['column_name'] for t in self.targets]

    # TODO update
    @property
    def metrics(self):
        #todo mappirng
        return [l['metric'] for l in self.problem['problem']['performance_metrics']]

    # TODO test (metric instead of name)
    @property
    def metrics_wparams(self):
        """
        Produces a list of metrics with any (optional) parameters.

        If the only key in /inputs/performanceMetrics[i] is 'metrics', there are no paramaters
        and metrics_wparams[i]['params'] is an empty dict.
        Any other key than 'metrics' is treated as a parameter. This handles non-default K values, and
        any future additions.

        Use with metrics.apply_metric:

        >>> from d3m_outputs.metrics import apply_metric
        >>> apply_metric(metrics_wparams['metric'], **metrics_wparams['params'])

        :return: list of dictionaries { 'name': metric_name, 'params': dict_of_params }
        :rtype: list<dict>

        """
        return self.problem['problem']['performance_metrics']


class D3MDataStructure:
    """
    Class representing a (problem, dataset) pair with associated data files.
    """
    DATASETSCHEMA_ARG = 'dataschema'
    PROBLEMSCHEMA_ARG = 'problemschema'
    ROOT_TO_SCORE_ARG = 'root'

    RELATIVE_PATH_TO_DATASCHEMA = 'dataset_TEST/datasetDoc.json'
    RELATIVE_PATH_TO_PROBLEMSCHEMA = 'problem_TEST/problemDoc.json'
    RELATIVE_PATH_TO_TESTDATA = 'dataset_TEST/tables/learningData.csv'
    RELATIVE_PATH_TO_TARGETS = 'targets.csv'

    def __init__(self, **kwargs):

        self.root = Path(kwargs[self.ROOT_TO_SCORE_ARG])
        self.dataschema = DatasetSchema(self.root / self.RELATIVE_PATH_TO_DATASCHEMA)
        self.problemschema = ProblemSchema(self.root / self.RELATIVE_PATH_TO_PROBLEMSCHEMA)
        self.testdata_path = self.root / self.RELATIVE_PATH_TO_TESTDATA
        self.targets_path = self.root / self.RELATIVE_PATH_TO_TARGETS


    def __getattr__(self, item):
        """
        If the attribute `item` is not found in the class attributes, look up the attributes in:
        * the data schema object
        * the problem schema object
        :param item: the attribute being retrieved
        :return: the attribute's value
        :raises: AttributeError is the attribute cannot be found in the objects.
        """
        if hasattr(self.dataschema, item):
            return self.dataschema.__getattribute__(item)
        elif hasattr(self.problemschema, item):
            return self.problemschema.__getattribute__(item)
        else:
            raise AttributeError(f'{item} not found in class or class schemas')

    def load_targets(self, targets_path=None):
        if targets_path:
            self.targets_path = targets_path

        self.targets_df = pandas.read_csv(self.targets_path)
        self.targets_index = self.targets_df.index
        self.number_targets = len(self.targets_index)

    @property
    def target_types(self):
        """
        Constructs a dict of expected target types from the targets listed in the problem schema and
        the data field types in the data schema.
        :return:
        :rtype:
        """
        return self.dataschema.target_types(self.problemschema.targets)

    @property
    def expected_index(self):
        """
        Extracts the expected index from the test data tables/learningData.csv
        :return: expected index of the predictions file
        :rtype: pandas.Series
        """
        testdata_df = pandas.read_csv(self.testdata_path)
        return testdata_df.index

    @property
    def expected_header(self):
        """
        Constructs the expected header of the predictions file from the data schema's index name and the
        problem schema's target names.
        :return: expected header of the predictions file
        :rtype: list
        """
        header_with_index = [self.dataschema.index_name]
        header_with_index.extend(self.problemschema.target_names)
        return header_with_index
