# imports
import file_header
import funnel_format
import serialize
import compress
import decompress
import deserialize
import driver
import unittest
import math

# Testing funnel format generation (where all incoming files can be split into the same format)
class TestFileHeader(unittest.TestCase):
    HEADER = ['chr','pos','ref','alt','af_cases_EUR','af_controls_EUR','beta_EUR','se_EUR','pval_EUR','low_confidence_EUR']
    TAB_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-tab.tsv'
    DATA = ['1','11063','T','G','4.213e-05','4.799e-05','-1.334e+00','9.999e+00','8.938e-01','true']
    BLOCK_SIZE = 5   
    CRRCT_FILE_HEADER = [10, 5]#, [], []]
    

    def test_make_file_header(self):
        self.assertEqual(file_header.make_file_header(self.TAB_FILE, self.BLOCK_SIZE), self.CRRCT_FILE_HEADER)
    
if __name__ == '__main__':
    unittest.main()
