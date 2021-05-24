import serialize
import compress
import numpy as np
from datetime import datetime
import sys
# from pyfastpfor import *

def compress_single_column_reg(typed_column, column_compression_method, column_type, column_bytes,
                               column_i, all_column_compression_times, all_column_compression_size_ratios):
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

    column_i_START = datetime.now()
    column_i_BEFORE = sys.getsizeof(typed_column)
    ### work ###
    serialized_column = serialize.serialize_list(typed_column, column_type, column_bytes)
    compressed_column_info = compress.compress_bitstring(column_compression_method, serialized_column)
    ############

    column_i_END = datetime.now()
    column_i_TIME = column_i_END - column_i_START
    column_i_AFTER = sys.getsizeof(compressed_column_info[0])
    column_i_RATIO = float(column_i_BEFORE/column_i_AFTER)
    
    # adding to time dict
    try:
        all_column_compression_times[column_i][column_compression_method].append(column_i_TIME)
    except KeyError:
        all_column_compression_times[column_i] = {column_compression_method: [column_i_TIME]}

    # adding to size ratio dict
    try:
        all_column_compression_size_ratios[column_i][column_compression_method].append(column_i_RATIO)
    except KeyError:
        all_column_compression_size_ratios[column_i] = {column_compression_method: [column_i_RATIO]}

    return compressed_column_info


def compress_single_column_pyfast(typed_column, codec,
                                  column_i, all_column_compression_times,
                                  all_column_compression_size_ratios):
    # print('compressing with pyfastpfor codec')
    """
    compresses a single column of data using pyfastpfor codecs
    INPUT
        typed_column = column as proper type (list of ints, rather than strings)
        codec = method of compression for given column (one of the 33 codecs)

    OUTPUT
        compressed_column = compressed data
    """

    column_i_START = datetime.now()
    column_i_BEFORE = sys.getsizeof(typed_column)
    ### work ###
    # convert input array to numpy array
    np_arr = np.array(typed_column, dtype=np.uint32, order='C')
    np_arr_size = np_arr.size
    buffer_size = 1 * 32

    # allocate space for compressed data
    comp_arr = np.zeros(np_arr_size + buffer_size, dtype=np.uint32, order='C')

    # get codec method from pyfastpfor and use it for compression
    codec_method = getCodec(codec)
    comp_arr_size = codec_method.encodeArray(np_arr, np_arr_size, comp_arr, len(comp_arr))
    
    ############
    column_i_END = datetime.now()
    column_i_TIME = column_i_END - column_i_START
    column_i_AFTER = sys.getsizeof(comp_arr[0:comp_arr_size])
    column_i_RATIO = float(column_i_BEFORE/column_i_AFTER)

    
    #print(column_i_BEFORE, column_i_AFTER)
    # adding to time dict
    try:
        all_column_compression_times[column_i][codec].append(column_i_TIME)
    except KeyError:
        all_column_compression_times[column_i] = {codec: [column_i_TIME]}

    # adding to size ratio dict
    try:
        all_column_compression_size_ratios[column_i][codec].append(column_i_RATIO)
    except KeyError:
        all_column_compression_size_ratios[column_i] = {codec: [column_i_RATIO]}

    return comp_arr[0:comp_arr_size]
