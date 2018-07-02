    
    
import os 

import unittest

from glob import glob
from d3m_outputs import generated_problems 

class TestGenProblems(unittest.TestCase):

    def setUp(self):
        current_path = os.path.abspath(__file__)
        test_dir_path = os.path.dirname(current_path)

        self.generated_problems_path = os.path.join(test_dir_path, 'generated_problems')

    def test_valid_submissions(self):
        subdirs = glob(os.path.join(self.generated_problems_path, 'correct*'))
        print(subdirs)

        assert len(subdirs) > 0
        for subdir in subdirs:
            assert generated_problems.check_generated_problems_directory(subdir) == True


    def test_invalid_submissions(self):
        subdirs = glob(os.path.join(self.generated_problems_path, 'wrong*'))
        subdirs.extend(glob(os.path.join(self.generated_problems_path, 'missing*')))
        print(subdirs)
        
        assert len(subdirs) > 0
        for subdir in subdirs:
            print(subdir)
            assert generated_problems.check_generated_problems_directory(subdir) == False

if __name__ == '__main__':
    unittest.main()