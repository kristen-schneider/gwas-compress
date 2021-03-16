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


class TestFunnelFormat(unittest.TestCase):
    HEADER = ['chr','pos','ref','alt','af_cases_EUR','af_controls_EUR','beta_EUR','se_EUR','pval_EUR','low_confidence_EUR']
    TAB_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-tab.tsv'
    TAB_FILE_75 = '/Users/kristen/Desktop/compression_sandbox/toy_data/75-lines-tab.tsv'
    COMMA_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-comma.csv'
    SPACE_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-space.ssv'
    BLOCK_SIZE = 5
    NUM_LINES_IN_FILE = 9 # not including header
    BLOCK_STRING = '1\t11063\tT\tG\t4.213e-05\t4.799e-05\t-1.334e+00\t9.999e+00\t8.938e-01\ttrue\n1\t13259\tG\tA\t2.984e-05\t2.786e-04\t-1.047e+00\t1.448e+00\t4.699e-01\ttruei\n'
    
    def test_determine_delimeter(self):
        self.assertEqual(funnel_format.determine_delimeter(self.TAB_FILE), '\t')
        self.assertEqual(funnel_format.determine_delimeter(self.COMMA_FILE), ',')
        self.assertEqual(funnel_format.determine_delimeter(self.SPACE_FILE), ' ')

    def test_get_header(self):
        self.assertEqual(type(funnel_format.get_header(self.TAB_FILE, '\t')), list)
        self.assertEqual(funnel_format.get_header(self.TAB_FILE, '\t'), self.HEADER)

    def test_get_chr_format(self):
        self.assertEqual(funnel_format.get_chr_format(self.TAB_FILE, self.HEADER, '\t'), 0) 

    def test_split_into_blocks(self):
        self.assertEqual(len(funnel_format.split_into_blocks(self.TAB_FILE, self.BLOCK_SIZE)), math.ceil(self.NUM_LINES_IN_FILE/self.BLOCK_SIZE))  
    def test_make_one_block(self):
        self.assertEqual(len(funnel_format.make_one_block(self.BLOCK_STRING, len(self.HEADER), self.BLOCK_SIZE, '\t')), len(self.HEADER)) 
    def test_make_all_blocks(self):
        self.assertEqual(len(funnel_format.make_all_blocks(self.TAB_FILE, self.BLOCK_SIZE, len(self.HEADER))), 2)
    
    
    
if __name__ == '__main__':
    unittest.main()
