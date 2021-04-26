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
        pyfastpfor_test_single.codecs_compression('BP32', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('BP32', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('BP32', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_copy(self):
        pyfastpfor_test_single.codecs_compression('copy', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('copy', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('copy', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_fastbinarypacking16(self):
        pyfastpfor_test_single.codecs_compression('fastbinarypacking16', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('fastbinarypacking16', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('fastbinarypacking16', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_fastbinarypacking32(self):
        pyfastpfor_test_single.codecs_compression('fastbinarypacking32', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('fastbinarypacking32', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('fastbinarypacking32', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_fastbinarypacking8(self):
        pyfastpfor_test_single.codecs_compression('fastbinarypacking8', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('fastbinarypacking8', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('fastbinarypacking8', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_fastpfor128(self):
        pyfastpfor_test_single.codecs_compression('fastpfor128', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('fastpfor128', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('fastpfor128', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_fastpfor256(self):
        pyfastpfor_test_single.codecs_compression('fastpfor256', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('fastpfor256', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('fastpfor256', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_maskedvbyte(self):
        pyfastpfor_test_single.codecs_compression('maskedvbyte', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('maskedvbyte', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('maskedvbyte', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_newpfor(self):
        pyfastpfor_test_single.codecs_compression('newpfor', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('newpfor', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('newpfor', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_optpfor(self):
        pyfastpfor_test_single.codecs_compression('optpfor', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('optpfor', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('optpfor', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_pfor(self):
        pyfastpfor_test_single.codecs_compression('pfor', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('pfor', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('pfor', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_pfor2008(self):
        pyfastpfor_test_single.codecs_compression('pfor2008', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('pfor2008', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('pfor2008', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_simdbinarypacking(self):
        pyfastpfor_test_single.codecs_compression('simdbinarypacking', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('simdbinarypacking', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('simdbinarypacking', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def simdfastpfor128(self):
        pyfastpfor_test_single.codecs_compression('simdfastpfor128', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('simdfastpfor128', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('simdfastpfor128', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_simdfastpfor256(self):
        pyfastpfor_test_single.codecs_compression('simdfastpfor256', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('simdfastpfor256', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('simdfastpfor256', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_simdgroupsimple(self):
        pyfastpfor_test_single.codecs_compression('simdgroupsimple', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('simdgroupsimple', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('simdgroupsimple', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_simdgroupsimple_ringbuf(self):
        pyfastpfor_test_single.codecs_compression('simdgroupsimple_ringbuf', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('simdgroupsimple_ringbuf', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('simdgroupsimple_ringbuf', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_simdnewpfor(self):
        pyfastpfor_test_single.codecs_compression('simdnewpfor', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('simdnewpfor', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('simdnewpfor', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_simdoptpfor(self):
        pyfastpfor_test_single.codecs_compression('simdoptpfor', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('simdoptpfor', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('simdoptpfor', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_simdpfor(self):
        pyfastpfor_test_single.codecs_compression('simdpfor', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('simdpfor', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('simdpfor', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_simdsimplepfor(self):
        pyfastpfor_test_single.codecs_compression('simdsimplepfor', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('simdsimplepfor', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('simdsimplepfor', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_simple16(self):
        pyfastpfor_test_single.codecs_compression('simple16', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('simple16', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('simple16', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_simple8b(self):
        pyfastpfor_test_single.codecs_compression('simple8b', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('simple8b', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('simple8b', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_simple8b_rle(self):
        pyfastpfor_test_single.codecs_compression('simple8b_rle', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('simple8b_rle', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('simple8b_rle', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_simple9(self):
        pyfastpfor_test_single.codecs_compression('simple9', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('simple9', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('simple9', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_simple9_rle(self):
        pyfastpfor_test_single.codecs_compression('simple9_rle', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('simple9_rle', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('simple9_rle', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_simplepfor(self):
        pyfastpfor_test_single.codecs_compression('simplepfor', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('simplepfor', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('simplepfor', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))

    def test_streamvbyte(self):
        pyfastpfor_test_single.codecs_compression('streamvbyte', self.short_arr, self.short_comp, self.short_decomp)
        assert(np.all(np.array(self.short_arr, dtype = np.uint32, order = 'C') == self.short_decomp))
        pyfastpfor_test_single.codecs_compression('streamvbyte', self.long_arr, self.long_comp, self.long_decomp)
        assert(np.all(np.array(self.long_arr, dtype = np.uint32, order = 'C') == self.long_decomp))
        pyfastpfor_test_single.codecs_compression('streamvbyte', self.large_arr, self.large_comp, self.large_decomp)
        assert(np.all(np.array(self.large_arr, dtype = np.uint32, order = 'C') == self.large_decomp))



if __name__ == '__main__':
    unittest.main()
