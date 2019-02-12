import os
import unittest
from glob import glob

from d3m_outputs import generated_problems


class TestGenProblems(unittest.TestCase):
    def setUp(self):
        current_path = os.path.abspath(__file__)
        test_dir_path = os.path.dirname(current_path)

        self.generated_problems_path = os.path.join(test_dir_path, "generated_problems")

    def test_valid_submissions(self):
        subdirs = glob(os.path.join(self.generated_problems_path, "correct*"))

        assert len(subdirs) > 0
        for subdir in subdirs:
            correct_result = os.path.join(
                self.generated_problems_path,
                "result_generated_problems_" + os.path.basename(subdir) + ".csv",
            )
            assert (
                generated_problems.check_generated_problems_directory(
                    subdir, correct_result
                )
                == True
            )

    def test_invalid_submissions(self):
        subdirs = glob(os.path.join(self.generated_problems_path, "wrong*"))
        subdirs.extend(glob(os.path.join(self.generated_problems_path, "missing*")))

        assert len(subdirs) > 0
        for subdir in subdirs:
            wrong_result = os.path.join(
                self.generated_problems_path,
                "result_generated_problems_" + os.path.basename(subdir) + ".csv",
            )
            assert (
                generated_problems.check_generated_problems_directory(
                    subdir, wrong_result
                )
                == False
            )

    def test_warning_submissions(self):
        subdirs = glob(os.path.join(self.generated_problems_path, "warning*"))

        assert len(subdirs) > 0
        for subdir in subdirs:
            wrong_result = os.path.join(
                self.generated_problems_path,
                "result_generated_problems_" + os.path.basename(subdir) + ".csv",
            )
            assert (
                generated_problems.check_generated_problems_directory(
                    subdir, wrong_result
                )
                == True
            )

    def tearDown(self):
        subdirs = glob(
            os.path.join(self.generated_problems_path, "result_generated_problems_*")
        )
        for file in subdirs:
            os.remove(file)


if __name__ == "__main__":
    unittest.main()
