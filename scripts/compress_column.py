import serialize
import compress
import numpy as np
#from pyfastpfor import *

def compress_single_column_reg(typed_column, column_compression_method, column_type, column_bytes):
    """
    compresses a single column of data using methods that take in serialized data (e.g. gzip, zlib, bz2)

    INPUT
        typed_column = column as proper type (list of ints, rather than strings)
        column_compression_method = method of compression for given column
        column_type = data type for given column
        column_bytes = number of bytes used for compression

    OUTPUT
        compressed_column_info = compressed data and length of header which would help decompress data
    """
    serialized_column = serialize.serialize_list(typed_column, column_type, column_bytes)
    compressed_column_info = compress.compress_bitstring(column_compression_method, serialized_column)
    return compressed_column_info


def compress_single_column_pyfast(typed_column, codec):
    # print('compressing with pyfastpfor codec')
    """
    compresses a single column of data using pyfastpfor codecs
    INPUT
        typed_column = column as proper type (list of ints, rather than strings)
        codec = method of compression for given column (one of the 33 codecs)

    OUTPUT
        compressed_column = compressed data
    """

    # convert input array to numpy array
    np_arr = np.array(typed_column, dtype=np.uint32, order='C')
    np_arr_size = np_arr.size
    buffer_size = 1 * 32

    # allocate space for compressed data
    comp_arr = np.zeros(np_arr_size + buffer_size, dtype=np.uint32, order='C')

    # get codec method from pyfastpfor and use it for compression
    codec_method = getCodec(codec)
    comp_arr_size = codec_method.encodeArray(np_arr, np_arr_size, comp_arr, len(comp_arr))

    return comp_arr