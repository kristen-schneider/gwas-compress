import unittest
import pyfastpfor_test_single

class TestCodecs(unittest.TestCase):

    codecs_list = ['BP32', 'copy', 'fastbinarypacking16', 'fastbinarypacking32', 'fastbinarypacking8', 'fastpfor128', 'fastpfor256', 'maskedvbyte', 'newpfor', 'optpfor', 'pfor', 'pfor2008', 'simdbinarypacking', 'simdfastpfor128', 'simdfastpfor256', 'simdgroupsimple', 'simdgroupsimple_ringbuf', 'simdnewpfor', 'simdoptpfor', 'simdpfor', 'simdsimplepfor', 'simple16', 'simple8b', 'simple8b_rle', 'simple9', 'simple9_rle', 'simplepfor', 'streamvbyte', 'varint', 'varintg8iu', 'varintgb', 'vbyte', 'vsencoding']
    
    short_arr = [1,1,1,1,1]
    long_arr = [1]*200
    large_values = [321489, 98172, 193012, 736280]

    def test_BP32(self):
        self.assertEqual(pyfastpfor_test_single.kristen('BP32', short_arr))


if __name__ == '__main__':
    unittest.main()
