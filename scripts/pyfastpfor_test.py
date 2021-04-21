from pyfastpfor import *
import numpy as np

def main():
    #dan()
    #arr = [1] * 20000
    kristen(arr)

def kristen(arr):
    # codecs list minus thee 4 codecs that generate an error
    codecs_list = ['BP32', 'copy', 'fastbinarypacking16', 'fastbinarypacking32', 'fastbinarypacking8', 'fastpfor128', 'fastpfor256', 'maskedvbyte', 'newpfor', 'optpfor', 'pfor', 'pfor2008', 'simdbinarypacking', 'simdfastpfor128', 'simdfastpfor256', 'simdgroupsimple', 'simdgroupsimple_ringbuf', 'simdnewpfor', 'simdoptpfor', 'simdpfor', 'simdsimplepfor', 'simple8b', 'simple8b_rle', 'simplepfor', 'streamvbyte', 'varint', 'varintg8iu', 'varintgb', 'vbyte']
    # full codecs list
    #codecs_list = ['BP32', 'copy', 'fastbinarypacking16', 'fastbinarypacking32', 'fastbinarypacking8', 'fastpfor128', 'fastpfor256', 'maskedvbyte', 'newpfor', 'optpfor', 'pfor', 'pfor2008', 'simdbinarypacking', 'simdfastpfor128', 'simdfastpfor256', 'simdgroupsimple', 'simdgroupsimple_ringbuf', 'simdnewpfor', 'simdoptpfor', 'simdpfor', 'simdsimplepfor', 'simple16', 'simple8b', 'simple8b_rle', 'simple9', 'simple9_rle', 'simplepfor', 'streamvbyte', 'varint', 'varintg8iu', 'varintgb', 'vbyte', 'vsencoding']
    
   
    # compression method
    for c in range(len(codecs_list)):
        # in array
        #arr = [1]*200#,1,1,1,1]
        arr_size = len(arr)
        np_arr = np.array(arr, dtype = np.uint32, order = 'C')
        
        # reserve space for compression and decompression
        comp = np.zeros(arr_size+1024, dtype = np.uint32, order = 'C')
        decomp = np.zeros(arr_size, dtype = np.uint32, order = 'C')
        
        # codec: compression type
        codec = getCodec(codecs_list[c])
    
        # compress data
        comp_size = codec.encodeArray(np_arr, arr_size, comp, len(comp))
        print(str(c) + '. ' + codecs_list[c] + ' compression ratio: %g' % (float(comp_size)/arr_size))
        #print(c + ': ', 'compression ratio: %g' % (float(comp_size)/arr_size))
    
        # decompress data
        #print('arr: ', np_arr)
        #print('comp: ', comp)
        #print('decomp: ', decomp)
        assert(arr_size == codec.decodeArray(comp, comp_size, decomp, arr_size))
        #print('arr: ', np_arr)
        #print('comp: ', comp)
        #print('decomp: ', decomp)
        assert(np.all(decomp == np_arr))
 
if __name__ == '__main__':
    main()
