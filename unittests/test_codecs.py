import unittest
import compress_array_data
import pyfastpfor_sandbox
import numpy as np

class TestCodecs(unittest.TestCase):

    #codecs_list = ['BP32', 'copy', 'fastbinarypacking16', 'fastbinarypacking32', 'fastbinarypacking8', 'fastpfor128', 'fastpfor256', 'maskedvbyte', 'newpfor', 'optpfor', 'pfor', 'pfor2008', 'simdbinarypacking', 'simdfastpfor128', 'simdfastpfor256', 'simdgroupsimple', 'simdgroupsimple_ringbuf', 'simdnewpfor', 'simdoptpfor', 'simdpfor', 'simdsimplepfor', 'simple16', 'simple8b', 'simple8b_rle', 'simple9', 'simple9_rle', 'simplepfor', 'streamvbyte', 'varint', 'varintg8iu', 'varintgb', 'vbyte', 'vsencoding']

    codecs_list = ['fastpfor128', 'fastpfor256']

    codec_dict = {codec: [0] for codec in codecs_list}
     
    #short_arr_size = 32*128
    codec_dict = {codec: [0] for codec in codecs_list}
     
    #short_arr_size = 32*128
    #long_arr_size = 32*2000
    #large_arr_size = 32*128
    
    short_arr = np.ones(5, dtype = np.uint32, order = 'C')
    long_arr = np.ones(50000, dtype = np.uint32, order = 'C')
    large_arr = np.array(np.random.randint(10000, 600000, 5), dtype = np.uint32, order = 'C')
   
    print('arrays: \n', short_arr, long_arr, large_arr)
        
    short_arr_size = short_arr.size
    long_arr_size = long_arr.size
    large_arr_size = large_arr.size 
    
    buffer_size = 1*32    

    def test_codecs_short_arr(self):
        for codec in self.codecs_list:
            # function prototype kristen(codec, arr, arr_size, buffer_size, codec_dict, block_i)
            short_decomp_size = pyfastpfor_sandbox.kristen(codec, 
                                                        self.short_arr, 
                                                        self.short_arr_size,
                                                        self.buffer_size*100,
                                                        self.codec_dict,
                                                        0)
            #print(short_decomp_size)
            self.assertEqual(self.short_arr_size, short_decomp_size)

    def test_codecs_long_arr(self):
        for codec in self.codecs_list:
            # function prototype kristen(codec, arr, arr_size, buffer_size, codec_dict, block_i)
            long_decomp_size = pyfastpfor_sandbox.kristen(codec, 
                                                        self.long_arr, 
                                                        self.long_arr_size,
                                                        self.buffer_size*100,
                                                        self.codec_dict,
                                                        0)
            #print(long_decomp_size)
            self.assertEqual(self.long_arr_size, long_decomp_size)

    def test_codecs_large_arr(self):
        for codec in self.codecs_list:
            # function prototype kristen(codec, arr, arr_size, buffer_size, codec_dict, block_i)
            large_decomp_size = pyfastpfor_sandbox.kristen(codec, 
                                                        self.large_arr, 
                                                        self.large_arr_size,
                                                        self.buffer_size*100,
                                                        self.codec_dict,
                                                        0)
            #print(short_decomp_size)
            self.assertEqual(self.large_arr_size, large_decomp_size)

if __name__ == '__main__':
    unittest.main()
