from pyfastpfor import *
import deserialize
import numpy as np

def decompress_single_column(serialized_data, block_size, data_type, num_bytes, chrm, codec):
    """
    takes a serialized array and deserializes it and converts it to a numpy array of dtype=numpy.uint32
    usually intput data represents some kind of compressed numpy array we are trying to decompress

    INPUT:
        serialized_data: serialized data representing some array

    OUTPUT:
        np_array: numpy array of dtype=numpy.uint32
    """
    decomp_arr_size = 2*block_size
    
    ds_data = deserialize.deserialize_list(serialized_data, block_size, data_type, num_bytes, chrm)
    comp_np_arr = np.array(ds_data, dtype=np.uint32, order='C')

    decomp_np_arr = decompress_np_arr(comp_np_arr, decomp_arr_size, codec)
    return decomp_np_arr[0:block_size]

def decompress_np_arr(comp_np_arr, np_arr_size, codec):
    """
    decompresses a single column of data using pyfastpfor codecs
    
    INPUT
        compressed_arr = numpy array of compressed data
        arr_size = size to allocate for decompressed data
        codec = compression method

    OUTPUT
        decompressed_column = decompressed data (np array)
    """
    comp_np_arr_size = comp_np_arr.size
    
    # allocate space for decompressed data
    decomp_np_arr = np.zeros(2*np_arr_size, dtype = np.uint32, order = 'C')
    
    # decompress data
    codec_method = getCodec(codec)
    decomp_arr_size = codec_method.decodeArray(comp_np_arr, comp_np_arr_size, decomp_np_arr, np_arr_size)

    #print('decomp after: ', decomp_arr)
    return decomp_np_arr[0:np_arr_size]


# def decompress_single_column(compressed_arr, arr_size, codec):
#     print('decompressing with pyfastpfor codec')
#     """
#     decompresses a single column of data using pyfastpfor codecs
#     INPUT
#         compressed_arr = numpy array of compressed data
#         arr_size = size to allocate for decompressed data
#         codec = compression method
#
#     OUTPUT
#         decompressed_column = decompressed data (np array)
#     """
#     #print(compressed_arr, arr_size, codec)
#     compressed_arr_size = compressed_arr.size
#     # allocate space for decompressed data
#     decomp_arr = np.zeros(2*arr_size, dtype = np.uint32, order = 'C')
#     print('decomp before: ', decomp_arr)
#     # decompress data
#     codec_method = getCodec(codec)
#     decomp_arr_size = codec_method.decodeArray(compressed_arr, compressed_arr_size, decomp_arr, arr_size)
#
#     print('decomp after: ', decomp_arr)
#     return decomp_arr[0:arr_size]


