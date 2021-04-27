import unittest
import pyfastpfor_test_single
import numpy as np

class TestCodecs(unittest.TestCase):

    codecs_list = ['BP32', 'copy', 'fastbinarypacking16', 'fastbinarypacking32', 'fastbinarypacking8', 'fastpfor128', 'fastpfor256', 'maskedvbyte', 'newpfor', 'optpfor', 'pfor', 'pfor2008', 'simdbinarypacking', 'simdfastpfor128', 'simdfastpfor256', 'simdgroupsimple', 'simdgroupsimple_ringbuf', 'simdnewpfor', 'simdoptpfor', 'simdpfor', 'simdsimplepfor', 'simple16', 'simple8b', 'simple8b_rle', 'simple9', 'simple9_rle', 'simplepfor', 'streamvbyte', 'varint', 'varintg8iu', 'varintgb', 'vbyte', 'vsencoding']

    short_arr_size = 32*128
    long_arr_size = 32*2000
    large_decomp_size = 32*128
    
    short_arr = np.ones(short_arr_size, dtype = np.uint32, order = 'C')
    long_arr = np.ones(long_arr_size, dtype = np.uint32, order = 'C')
    large_arr = np.array(np.random.randint(10000, 600000, 128), dtype = np.uint32, order = 'C')
   
    buffer_size = 16    

    def test_BP32(self):
        codec = 'BP32'
        short_decomp_size = pyfastpfor_test_single.kristen(codec, self.short_arr, self.short_arr_size, self.buffer_size*100)        
        self.assertEqual(self.short_arr_size, short_decomp_size)
if __name__ == '__main__':
    unittest.main()
