import unittest
import pyfastpfor_test_single
import numpy as np

class TestCodecs(unittest.TestCase):

    codecs_list = ['BP32', 'copy', 'fastbinarypacking16', 'fastbinarypacking32', 'fastbinarypacking8', 'fastpfor128', 'fastpfor256', 'maskedvbyte', 'newpfor', 'optpfor', 'pfor', 'pfor2008', 'simdbinarypacking', 'simdfastpfor128', 'simdfastpfor256', 'simdgroupsimple', 'simdgroupsimple_ringbuf', 'simdnewpfor', 'simdoptpfor', 'simdpfor', 'simdsimplepfor', 'simple16', 'simple8b', 'simple8b_rle', 'simple9', 'simple9_rle', 'simplepfor', 'streamvbyte', 'varint', 'varintg8iu', 'varintgb', 'vbyte', 'vsencoding']
    short_arr = [1]*128
    short_comp = np.zeros(len(short_arr)+(16*10), dtype = np.uint32, order = 'C')
    short_decomp = np.zeros(len(short_arr), dtype = np.uint32, order = 'C')    
    long_arr = [1]*20000
    long_comp = np.zeros(len(long_arr)+(16*10), dtype = np.uint32, order = 'C')
    long_decomp = np.zeros(len(long_arr), dtype = np.uint32, order = 'C')    
    large_arr = np.array(np.random.randint(10000, 600000, 128), dtype = np.uint32, order = 'C')
    large_comp = np.zeros(len(large_arr)+(16*10), dtype = np.uint32, order = 'C')
    large_decomp = np.zeros(len(large_arr), dtype = np.uint32, order = 'C')    

    def test_BP32(self):
        #pyfastpfor_test_single.codecs_compression('BP32', self.short_arr)
        pyfastpfor_test_single.codecs_compression('BP32', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('BP32', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('BP32', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

if __name__ == '__main__':
    unittest.main()
