import unittest
import numpy as np

import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from decompression import search

class TestCodecs(unittest.TestCase):

    def test_find_blocks(self):
        self.assertEqual(search.find_blocks(10, 1, 0), [-1,-1])
        
        self.assertEqual(search.find_blocks(10, 0, 1), [0,0])
        self.assertEqual(search.find_blocks(10, 0, 9), [0,0])
        self.assertEqual(search.find_blocks(10, 0, 10), [0,1])
        self.assertEqual(search.find_blocks(10, 0, 19), [0,1])
        self.assertEqual(search.find_blocks(10, 0, 20), [0,2])

        self.assertEqual(search.find_blocks(10, 9, 19), [0,1])
        self.assertEqual(search.find_blocks(10, 10, 19), [1,1])
        self.assertEqual(search.find_blocks(10, 11, 19), [1,1])
        self.assertEqual(search.find_blocks(10, 20, 20), [2,2])
        self.assertEqual(search.find_blocks(10, 20, 200), [2,20])
        self.assertEqual(search.find_blocks(10, 20, 2000), [2,200])
        self.assertEqual(search.find_blocks(10, 32, 56), [3,5])
   
        self.assertEqual(search.find_blocks(7, 0, 222), [0, 31])
        self.assertEqual(search.find_blocks(7, 100, 222), [14, 31]) 


    def test_block_row_mapping(self):
        self.assertEqual(search.block_row_mapping([0,0],3,0,1), [0,1])
        self.assertEqual(search.block_row_mapping([0,0],3,0,2), [0,2])
        self.assertEqual(search.block_row_mapping([0,1],3,0,3), [0,0])
        self.assertEqual(search.block_row_mapping([0,1],3,0,4), [0,1])
        
        self.assertEqual(search.block_row_mapping([0,31],7,0,222), [0,5])
        self.assertEqual(search.block_row_mapping([14,31],7,100,222), [2,5])
        #self.assertEqual(search.block_row_mapping([0,1],3,0,3), [0,0])
        #self.assertEqual(search.block_row_mapping([0,1],3,0,4), [0,1])


if __name__ == '__main__':
    unittest.main()
