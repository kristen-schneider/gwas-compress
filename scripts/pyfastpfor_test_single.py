from pyfastpfor import *
import numpy as np

def main():
    #dan()
    codec = 'BP32'
    arr = [1,1,1,1,1]
    r = codecs_compression(codec, arr)
    for i in r: print(i)

def codecs_compression(codec,arr):
    # array to numpy array
    arr_size = len(arr)
    np_arr = np.array(arr, dtype = np.uint32, order = 'C')
    
    # reserve space for compression and decompression
    comp = np.zeros(arr_size*2, dtype = np.uint32, order = 'C')
    decomp = np.zeros(arr_size, dtype = np.uint32, order = 'C')
    
    # codec: compression type
    codec_method = getCodec(codec)

    # compression
    comp_size = codec_method.encodeArray(np_arr, arr_size, comp, len(comp))
    
    # decompression
    codec_method.decodeArray(comp, comp_size, decomp, arr_size)

    return decomp

def compress():
    #print('arr: ', np_arr)
    #print('comp: ', comp)
    #print('decomp: ', decomp)
    #assert(arr_size == codec.decodeArray(comp, comp_size, decomp, arr_size))
    comp_size = codec.encodeArray(np_arr, arr_size, comp, len(comp))

def decompress():
    codec.decodeArray(comp, comp_size, decomp, arr_size)
    #print('arr: ', np_arr)
    #print('comp: ', comp)
    #print('decomp: ', decomp)
    assert(np.all(decomp == np_arr))


def trash():
    #print(arr)
    # codecs list minus thee 4 codecs that generate an error
    #codecs_list = ['BP32', 'copy', 'fastbinarypacking16', 'fastbinarypacking32', 'fastbinarypacking8', 'fastpfor128', 'fastpfor256', 'maskedvbyte', 'newpfor', 'optpfor', 'pfor', 'pfor2008', 'simdbinarypacking', 'simdfastpfor128', 'simdfastpfor256', 'simdgroupsimple', 'simdgroupsimple_ringbuf', 'simdnewpfor', 'simdoptpfor', 'simdpfor', 'simdsimplepfor', 'simple8b', 'simple8b_rle', 'simplepfor', 'streamvbyte', 'varint', 'varintg8iu', 'varintgb', 'vbyte']
    # full codecs list
    #codecs_list = ['BP32', 'copy', 'fastbinarypacking16', 'fastbinarypacking32', 'fastbinarypacking8', 'fastpfor128', 'fastpfor256', 'maskedvbyte', 'newpfor', 'optpfor', 'pfor', 'pfor2008', 'simdbinarypacking', 'simdfastpfor128', 'simdfastpfor256', 'simdgroupsimple', 'simdgroupsimple_ringbuf', 'simdnewpfor', 'simdoptpfor', 'simdpfor', 'simdsimplepfor', 'simple16', 'simple8b', 'simple8b_rle', 'simple9', 'simple9_rle', 'simplepfor', 'streamvbyte', 'varint', 'varintg8iu', 'varintgb', 'vbyte', 'vsencoding']
    
    #performance_file = open(out_f+'codecs_performance-' + str(col_num) + '.tsv', 'w')
    #performance_file.truncate()
    #print(col_num, arr, out_f)
    
    # in array
    #arr = [1]*200#,1,1,1,1]
    arr_size = len(arr)
    np_arr = np.array(arr, dtype = np.uint32, order = 'C')
        
    # reserve space for compression and decompression
    comp = np.zeros(arr_size*2, dtype = np.uint32, order = 'C')
    decomp = np.zeros(arr_size, dtype = np.uint32, order = 'C')
        
    # codec: compression type
    c = 'simple9'
    codec = getCodec(c)
        
    # compress data
    comp_size = codec.encodeArray(np_arr, arr_size, comp, len(comp))
    print(c + ': ', 'compression ratio: %g' % (float(comp_size)/arr_size))
    
    # decompress data
    #print('arr: ', np_arr)
    #print('comp: ', comp)
    #print('decomp: ', decomp)
    #assert(arr_size == codec.decodeArray(comp, comp_size, decomp, arr_size))
    codec.decodeArray(comp, comp_size, decomp, arr_size)
    #print('arr: ', np_arr)
    #print('comp: ', comp)
    #print('decomp: ', decomp)
    assert(np.all(decomp == np_arr))
 
if __name__ == '__main__':
    main()
