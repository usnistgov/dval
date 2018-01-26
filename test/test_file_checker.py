import os
import unittest

import logging

from file_checker import FileChecker

logging.disable(logging.CRITICAL)


def setUpModule():
    global results_path
    results_path = os.path.join('test', 'results')


class TestFileChecker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.chmod(os.path.join(results_path, 'cant_read_results.csv'), 0o000)


    @classmethod
    def tearDownClass(cls):
        os.chmod(os.path.join(results_path, 'cant_read_results.csv'), 0o444)


    def testRaiseFileNotFound1(self):
        path = os.path.join(results_path, 'nonexistant_results.csv')

        with self.assertRaises(Exception):
            fc = FileChecker(path)
            fc.check_exists_read('result_path')


    def testRaiseOnNoReadAccess1(self):
        path = os.path.join(results_path, 'cant_read_results.csv')

        with self.assertRaises(Exception):
            fc = FileChecker(path)
            fc.check_exists_read('result_path')


    def testNoExceptionsAndTrueWhenExistsAndRead1(self):
        path = os.path.join(results_path, 'existant_results.csv')

        fc = FileChecker(path)

        self.assertTrue(fc.check_exists_read('dataset_schema_path'))


if __name__ == '__main__':
    unittest.main()
