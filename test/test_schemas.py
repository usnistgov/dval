import unittest
from pathlib import Path

import schemas


class TestProblemSchema(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path = Path(__file__).parent / 'data/185_baseball/problem_TEST/problemDoc.json'
        cls.baseballProblemSchema = schemas.ProblemSchema(cls.path)

    def testInit(self):
        withStringPath = schemas.ProblemSchema(str(self.path))
        self.assertEqual(withStringPath, self.baseballProblemSchema)

    def testMetrics(self):
        self.assertEqual(self.baseballProblemSchema.metrics, ['f1Macro'])

    def testTargetNames(self):
        self.assertEqual(self.baseballProblemSchema.target_names, ['Hall_of_Fame'])


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

    def testInit(self):
        self.assertEqual(self.obj.problemschema.metrics, ['f1Macro'])
        self.assertEqual(self.obj.problemschema.metrics_wparams[0]['name'], 'f1Macro')
        self.assertEqual(self.obj.problemschema.metrics_wparams[0]['params'], dict())
        self.assertEqual(len(self.obj.problemschema.metrics), 1)
        self.assertEqual(len(self.obj.problemschema.metrics_wparams), 1)
        self.assertEqual(self.obj.dataschema.index_name, 'd3mIndex')

    def testGetAttr(self):
        self.assertEqual(self.obj.metrics, ['f1Macro'])
        self.assertEqual(self.obj.index_name, 'd3mIndex')
        self.assertEqual(self.obj.target_names, ['Hall_of_Fame'])

    def testTargetTypes(self):
        self.assertEqual(self.obj.target_types, {'Hall_of_Fame': 'categorical'})


if __name__ == '__main__':
    unittest.main()
