import unittest
from pathlib import Path

from d3m_outputs import schemas

F1MACRO = 'F1_MACRO'

class TestProblemSchema(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path = Path(__file__).parent / 'data/185_baseball/problem_TEST/problemDoc.json'
        cls.baseballProblemSchema = schemas.ProblemSchema(cls.path)

    def testMetrics(self):
        baseballmetrics = self.baseballProblemSchema.metrics
        self.assertEqual(len(baseballmetrics), 1)
        self.assertEqual(baseballmetrics[0].name, 'F1_MACRO')

    def testTargetNames(self):
        self.assertEqual(self.baseballProblemSchema.target_names, ['Hall_of_Fame'])

    def testMetricsWithParams(self):
        baseballmetrics = self.baseballProblemSchema.metrics_wparams
        self.assertEqual(len(baseballmetrics), 1)
        self.assertEqual(baseballmetrics[0]['metric'].name, 'F1_MACRO')
        self.assertEqual(baseballmetrics[0]['params'], dict() )

class TestDatasetSchema(unittest.TestCase):

    def testIndex(self):
        path = Path(__file__).parent / 'data/185_baseball/dataset_TEST/datasetDoc.json'
        baseball_dataset_schema = schemas.DatasetSchema(path)
        self.assertEqual(baseball_dataset_schema.index_name, 'd3mIndex')


class TestD3MDataStructure(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        data_dir = Path(__file__).parent / 'data/185_baseball'
        cls.obj = schemas.D3MDataStructure(root=data_dir)
        cls.metrics = cls.obj.problemschema.metrics
        cls.metrics_wp = cls.obj.problemschema.metrics_wparams

    def testInit(self):
        self.assertEqual([metric.name for metric in self.metrics], [F1MACRO])
        self.assertEqual(self.metrics_wp[0]['metric'], F1MACRO)
        self.assertEqual(self.metrics_wp[0]['params'], dict())
        self.assertEqual(len(self.metrics), 1)
        self.assertEqual(len(self.metrics_wp), 1)
        self.assertEqual(self.obj.dataschema.index_name, 'd3mIndex')

    def testGetAttr(self):
        self.assertEqual([metric.name for metric in self.obj.metrics], [F1MACRO])
        self.assertEqual(self.obj.index_name, 'd3mIndex')
        self.assertEqual(self.obj.target_names, ['Hall_of_Fame'])

    def testTargetTypes(self):
        self.assertEqual(self.obj.target_types, {'Hall_of_Fame': 'categorical'})


def test_params():
    data_dir = Path(__file__).parent / 'data'
    schema = schemas.ProblemSchema(data_dir / 'problemDoc_with0posLabel.json')
    assert len(schema.metrics) == 1
    assert len(schema.metrics_wparams) == 1
    main_metric = schema.metrics_wparams[0]
    assert 'params' in main_metric
    assert 'pos_label' in main_metric['params']

if __name__ == '__main__':
    unittest.main()
