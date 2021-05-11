from pyfastpfor import *
import numpy as np

def decompress_single_column(compressed_arr, arr_size, codec):
    print('decompressing with pyfastpfor codec')
    """
    decompresses a single column of data using pyfastpfor codecs
    INPUT
        compressed_arr = numpy array of compressed data
        arr_size = size to allocate for decompressed data
        codec = compression method
 
    OUTPUT
        decompressed_column = decompressed data (np array)
    """
    #print(compressed_arr, arr_size, codec)
    compressed_arr_size = compressed_arr.size
    # allocate space for decompressed data
    decomp_arr = np.zeros(2*arr_size, dtype = np.uint32, order = 'C')
    print('decomp before: ', decomp_arr)
    # decompress data
    codec_method = getCodec(codec)
    decomp_arr_size = codec_method.decodeArray(compressed_arr, compressed_arr_size, decomp_arr, arr_size)
    
    print('decomp after: ', decomp_arr)
    return decomp_arr[0:arr_size]
