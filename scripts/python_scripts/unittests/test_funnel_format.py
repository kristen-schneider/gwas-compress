# imports
import unittest
import math

import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import file_header
from new_compression import generate_funnel_format
from new_compression import serialize_body
from new_compression import compress
from decompression import decompress
from decompression import deserialize


class TestFunnelFormat(unittest.TestCase):
    TAB_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-tab.tsv'
    BLOCK_SIZE = 5
    NUM_LINES_IN_FILE = 9 # not including header
    BLOCK_STRING = '1\t11063\tT\tG\t4.213e-05\t4.799e-05\t-1.334e+00\t9.999e+00\t8.938e-01\ttrue\n1\t13259\tG\tA\t2.984e-05\t2.786e-04\t-1.047e+00\t1.448e+00\t4.699e-01\ttruei\n'
    
    def test_get_chr_format(self):
        self.assertEqual(generate_funnel_format.get_chr_format(self.TAB_FILE, self.HEADER, '\t'), 0)
    def test_split_into_blocks(self):
        self.assertEqual(len(generate_funnel_format.split_into_blocks(self.TAB_FILE, self.BLOCK_SIZE)), math.ceil(self.NUM_LINES_IN_FILE / self.BLOCK_SIZE))
    def test_make_one_block(self):
        self.assertEqual(len(generate_funnel_format.make_one_block(self.BLOCK_STRING, len(self.HEADER), self.BLOCK_SIZE, '\t')), len(self.HEADER))
    def test_make_all_blocks(self):
        self.assertEqual(len(generate_funnel_format.make_all_blocks(self.TAB_FILE, self.BLOCK_SIZE, len(self.HEADER))), 2)
    
    
    
if __name__ == '__main__':
    unittest.main()
