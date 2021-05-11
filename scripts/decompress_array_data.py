from pyfastpfor import *
import numpy as np

def decompress_single_column(compressed_array, arr_size):
    print('decompressing with pyfastpfor codec')
    """
    decompresses a single column of data using pyfastpfor codecs
    INPUT
        compressed_array = numpy array of compressed data
        arr_size = size to allocate for decompressed data
 
    OUTPUT
        decompressed_column = decompressed data (np array)
    """
    # allocate space for decompressed data
    decomp_arr = np.zeros(np_arr_size, dtype = np.uint32, order = 'C')
        
    decomp_arr_size = codec_method.decodeArray(comp_arr, comp_arr_size, decomp_arr, np_arr_size)

    return decomp_arr
