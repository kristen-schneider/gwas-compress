# imports
import file_header
import basics
import funnel_format
import serialize
import compress
import decompress
import deserialize
import driver
import unittest

# Testing funnel format generation (where all incoming files can be split into the same format)
class TestFileHeader(unittest.TestCase):
    TAB_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-tab.tsv'
    COL_NAMES = ['chr','pos','ref','alt','af_cases_EUR','af_controls_EUR','beta_EUR','se_EUR','pval_EUR','low_confidence_EUR']
    COL_TYPES = [int, int, str, str, float, float, float, float, float, bool]
    DATA = ['1','11063','T','G','4.213e-05','4.799e-05','-1.334e+00','9.999e+00','8.938e-01','true']
    
    BLOCK_SIZE = 5   
    CRRCT_FILE_HEADER = [10, 5]#, [], []]
    

    def test_get_column_names(self):
        self.assertEqual(file_header.get_column_names(self.TAB_FILE), self.COL_NAMES)
   
    def test_get_column_types(self):
        self.assertEqual(file_header.get_column_types(self.TAB_FILE), self.COL_TYPES) 
if __name__ == '__main__':
    unittest.main()
