import decompress
import deserialize_header
import deserialize_body
import convert_from_int
import numpy as np
# from pyfastpfor import *

# when float data is NA, int data is [0,-999]
# when string data is NA, int data is -1

def decompress_single_column_standard(compression_method, c_bitstring, block_size, data_type, num_bytes, chrm, column_i):
    """
    decompresses a single column of data using gzip/zlib/bz2

    INPUT
        compressed_arr = numpy array of compressed data
        arr_size = size to allocate for decompressed data
        codec = compression method

    OUTPUT
        decompressed_column = decompressed data (np array)
    """
    dc_column = decompress.decompress_data(compression_method, c_bitstring)
    ds_column = deserialize_body.deserialize_list(dc_column, block_size, data_type, num_bytes, chrm, column_i)
    original_type_column = convert_from_int.convert_list_from_int(ds_column, data_type)
    return original_type_column


def decompress_single_column_pyfast(serialized_data, block_size, data_type, num_bytes, chrm, codec, column_i):
    """
    takes a serialized array and deserializes it and converts it to a numpy array of dtype=numpy.uint32
    usually intput data represents some kind of compressed numpy array we are trying to decompress

    INPUT:
        serialized_data: serialized data representing some array

    OUTPUT:
        np_array: numpy array of dtype=numpy.uint32
    """
    decomp_arr_size = 2 * block_size


    ds_data = deserialize_body.deserialize_list(serialized_data, block_size, data_type, num_bytes, chrm, column_i)
    try:
        comp_np_arr = np.array(ds_data, dtype=np.uint32, order='C')
    except ValueError:
        print('ds data: ', ds_data, data_type)
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
    decomp_np_arr = np.zeros(2 * np_arr_size, dtype=np.uint32, order='C')

    # decompress data
    codec_method = getCodec(codec)
    decomp_arr_size = codec_method.decodeArray(comp_np_arr, comp_np_arr_size, decomp_np_arr, np_arr_size)

    # print('decomp after: ', decomp_arr)
    return decomp_np_arr[0:np_arr_size]
