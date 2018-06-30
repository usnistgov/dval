import unittest
from pathlib import Path
import sys
from d3m_outputs.cli import cli_parser, cmd_valid_pipeline
from d3m_outputs.predictions import is_predictions_file_valid

class TestValidateScores(unittest.TestCase):

    def test_bogus_column(self):
        sys.argv[1:] = ['valid_predictions', '-d', 'test/data/1491_one_hundred_plants_margin', 'test/bad_data_input/mitll_predictions_column_error(bogus_column).csv']
        with self.assertRaises(SystemExit):
            cli_parser()

    def test_class_col_misnamed(self):
        sys.argv[1:] = ['valid_predictions', '-d', 'test/data/1491_one_hundred_plants_margin', 'test/bad_data_input/mitll_predictions_column_error(class_col_misnamed).csv']
        with self.assertRaises(SystemExit):
            cli_parser()

    def test_index_col_misnamed(self):
        sys.argv[1:] = ['valid_predictions', '-d', 'test/data/1491_one_hundred_plants_margin', 'test/bad_data_input/mitll_predictions_column_error(index_col_misnamed).csv']
        with self.assertRaises(SystemExit):
            cli_parser()

    def test_missing_class_col(self):
        sys.argv[1:] = ['valid_predictions', '-d', 'test/data/1491_one_hundred_plants_margin', 'test/bad_data_input/mitll_predictions_column_error(missing_class_col).csv']
        with self.assertRaises(SystemExit):
            cli_parser()

    def test_missing_class_data(self):
        sys.argv[1:] = ['valid_predictions', '-d', 'test/data/1491_one_hundred_plants_margin', 'test/bad_data_input/mitll_predictions_column_error(missing_class_data).csv']
        with self.assertRaises(SystemExit):
            cli_parser()

    def test_missing_index_col(self):
        sys.argv[1:] = ['valid_predictions', '-d', 'test/data/1491_one_hundred_plants_margin', 'test/bad_data_input/mitll_predictions_column_error(missing_index_col).csv']
        with self.assertRaises(SystemExit):
            cli_parser()

    def test_missing_index_data(self):
        sys.argv[1:] = ['valid_predictions', '-d', 'test/data/1491_one_hundred_plants_margin', 'test/bad_data_input/mitll_predictions_column_error(missing_index_data).csv']
        with self.assertRaises(SystemExit):
            cli_parser()

    def test_swapped_columns(self):
        sys.argv[1:] = ['valid_predictions', '-d', 'test/data/1491_one_hundred_plants_margin', 'test/bad_data_input/mitll_predictions_column_error(swapped_columns).csv']
        with self.assertRaises(SystemExit):
            cli_parser()




if __name__ == '__main__':
    unittest.main()
