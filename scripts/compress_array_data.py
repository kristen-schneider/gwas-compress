from pyfastpfor import *
import numpy as np

def compress_single_column(typed_column, codec):
    print('compressing with pyfastpfor codec')
    """
    compresses a single column of data using pyfastpfor codecs
    INPUT
        typed_column = column as proper type (list of ints, rather than strings)
        codec = method of compression for given column (one of the 33 codecs)
    
    OUTPUT
        compressed_column = compressed data
    """
    #serialized_column = serialize.serialize_list(typed_column, column_type, column_bytes)
    #compressed_column_info = compress.compress_data(column_compression_method, serialized_column, mtime)
    
    

    # convert input array to numpy array
    np_arr = np.array(typed_column, dtype = np.uint32, order = 'C')
    np_arr_size = np_arr.size
    buffer_size = 1*32

    # allocate space for compressed data
    comp_arr = np.zeros(np_arr_size + buffer_size, dtype = np.uint32, order = 'C')

    # allocate space for decompressed data
    #decomp_arr = np.zeros(np_arr_size, dtype = np.uint32, order = 'C')
    
    # get codec method from pyfastpfor and use it for compression
    codec_method = getCodec(codec)
    comp_arr_size = codec_method.encodeArray(np_arr, np_arr_size, comp_arr, len(comp_arr))
    #decomp_arr_size = codec_method.decodeArray(comp_arr, comp_arr_size, decomp_arr, np_arr_size)
        
    # print statements for debug    
    #print('input: ', np_arr, np_arr_size)
    #print('comp: ', comp_arr, comp_arr_size)
    #print('decomp: ', decomp_arr)
    return comp_arr

#test = [1] * 5000
#compress_single_column(test, 'fastpfor128')

