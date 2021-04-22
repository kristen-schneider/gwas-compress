import unittest
import pyfastpfor_test_single
import numpy as np

class TestCodecs(unittest.TestCase):

    codecs_list = ['BP32', 'copy', 'fastbinarypacking16', 'fastbinarypacking32', 'fastbinarypacking8', 'fastpfor128', 'fastpfor256', 'maskedvbyte', 'newpfor', 'optpfor', 'pfor', 'pfor2008', 'simdbinarypacking', 'simdfastpfor128', 'simdfastpfor256', 'simdgroupsimple', 'simdgroupsimple_ringbuf', 'simdnewpfor', 'simdoptpfor', 'simdpfor', 'simdsimplepfor', 'simple16', 'simple8b', 'simple8b_rle', 'simple9', 'simple9_rle', 'simplepfor', 'streamvbyte', 'varint', 'varintg8iu', 'varintgb', 'vbyte', 'vsencoding']
    
    short_arr = [1,1,1,1,1]
    long_arr = [1]*200
    large_arr = [321489, 98172, 193012, 736280]

    def test_BP32(self):
        short_c = pyfastpfor_test_single.codecs_compression('BP32', self.short_arr)
        short_a = np.array(self.short_arr, dtype = np.uint32, order = 'C')
        long_c = pyfastpfor_test_single.codecs_compression('BP32', self.long_arr)
        long_a = np.array(self.long_arr, dtype = np.uint32, order = 'C')
        large_c = pyfastpfor_test_single.codecs_compression('BP32', self.large_arr)
        large_a = np.array(self.large_arr, dtype = np.uint32, order = 'C')
        assert(np.all(short_c == short_a))
        assert(np.all(long_c == long_a)) 
        assert(np.all(large_c == large_a))
    
    def test_copy(self):
        short_c = pyfastpfor_test_single.codecs_compression('copy', self.short_arr)
        short_a = np.array(self.short_arr, dtype = np.uint32, order = 'C')
        long_c = pyfastpfor_test_single.codecs_compression('copy', self.long_arr)
        long_a = np.array(self.long_arr, dtype = np.uint32, order = 'C')
        large_c = pyfastpfor_test_single.codecs_compression('copy', self.large_arr)
        large_a = np.array(self.large_arr, dtype = np.uint32, order = 'C')
        assert(np.all(short_c == short_a))
        assert(np.all(long_c == long_a)) 
        assert(np.all(large_c == large_a))
   
    def test_fastbinarypacking16(self):
        short_c = pyfastpfor_test_single.codecs_compression('fastbinarypacking16', self.short_arr)
        short_a = np.array(self.short_arr, dtype = np.uint32, order = 'C')
        long_c = pyfastpfor_test_single.codecs_compression('fastbinarypacking16', self.long_arr)
        long_a = np.array(self.long_arr, dtype = np.uint32, order = 'C')
        large_c = pyfastpfor_test_single.codecs_compression('fastbinarypacking16', self.large_arr)
        large_a = np.array(self.large_arr, dtype = np.uint32, order = 'C')
        assert(np.all(short_c == short_a))
        assert(np.all(long_c == long_a)) 
        assert(np.all(large_c == large_a))

if __name__ == '__main__':
    unittest.main()
