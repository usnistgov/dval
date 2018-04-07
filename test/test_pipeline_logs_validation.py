import logging
import unittest
from pathlib import Path

from d3m_outputs.pipeline_logs_validator import PipelineLog

logging.disable(logging.CRITICAL)


class TestPipelineLogsValidation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.testdir = Path(__file__).parent / 'pipelinelogs'
        cls.testcases = {
            'correct_pipeline': cls.testdir / 'correct_pipeline.json',
            'empty_primitive_set': cls.testdir / 'empty_primitive_set.json',
            'missing_name': cls.testdir / 'missing_name.json',
            'missing_pid': cls.testdir / 'missing_pid.json',
            'missing_rank': cls.testdir / 'missing_rank.json',
            'single_primitive_pipeline': cls.testdir / 'single_primitive_pipeline.json',
            'rank_is_not_integer': cls.testdir / 'rank_is_not_integer.json',
            'primitives_is_not_list': cls.testdir / 'primitives_is_not_list.json'
        }

    def testValid(self):
        p1 = PipelineLog(self.testcases['correct_pipeline'])
        self.assertTrue(p1.is_valid())

        p2 = PipelineLog(self.testcases['single_primitive_pipeline'])
        self.assertTrue(p2.is_valid())

    def testMissingPrimitiveSet(self):
        p = PipelineLog(self.testcases['empty_primitive_set'])
        self.assertFalse(p.is_valid())

    def testMissingName(self):
        p = PipelineLog(self.testcases['missing_name'])
        self.assertFalse(p.is_valid())

    def testMissingRank(self):
        p = PipelineLog(self.testcases['missing_rank'])
        self.assertFalse(p.is_valid())

    def testProblemId(self):
        p = PipelineLog(self.testcases['missing_pid'])
        self.assertFalse(p.is_valid())

    def testPrimitivesIsList(self):
        p = PipelineLog(self.testcases['primitives_is_not_list'])
        self.assertFalse(p.is_valid())

    def testRankIsInteger(self):
        p = PipelineLog(self.testcases['rank_is_not_integer'])
        self.assertFalse(p.is_valid())
