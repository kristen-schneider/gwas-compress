import numpy as np
from datetime import datetime
import sys
from pyfastpfor import *

import serialize_body
import compress

def compress_block(num_columns, block_as_columns_ints, codecs_list,
                   column_data_types, data_type_byte_sizes):
    """

    """
    compressed_block_bitstring = b'' # a bitstring of compressed columns (for gzip/zlib/bz2)
    compressed_block_list = []
    block_header = []
    col_end_bit = 0
    for col_index in range(num_columns):
        column_codec = codecs_list[col_index]
        curr_column = block_as_columns_ints[col_index]
        column_data_type = column_data_types[col_index]
        column_num_bytes = data_type_byte_sizes[column_data_type]

        # gzip, zlib, and bz2 codecs
        if column_codec == 'gzip' \
            or column_codec == 'zlib' \
            or column_codec == 'bz2':
            compressed_column_bitstring = compress_with_other(curr_column, column_codec, column_data_type, column_num_bytes)
            col_end_bit += len(compressed_column_bitstring)
            block_header.append(col_end_bit)
            compressed_block_bitstring += compressed_column_bitstring

        # fastpfor codecs
        else:
            compressed_column_np_array = comress_with_fastpfor(curr_column, column_codec)
            serialized_compressed_column = compressed_column_np_array.tobytes(order='C')
            col_end_bit += len(serialized_compressed_column)
            block_header.append(col_end_bit)
            compressed_block_bitstring += serialized_compressed_column
    
    if compressed_block_bitstring != b'':
        return block_header, compressed_block_bitstring
    # elif compressed_column_np_array != []:
    #     return block_header, compressed_block_list
    else:
        print('block compression is empty')
        return -1


def compress_with_other(column, column_codec, column_data_type, column_num_bytes):
    """
    compress a column of integers with gzip, zlib, or bz2

    :return compressed_column: compressed column excluding compression header
    """
    compressed_column = b''
    column_i_START = datetime.now()
    column_i_BEFORE = sys.getsizeof(column)
    column_i_END = datetime.now()
    ### work ###
    serialized_column = serialize_body.serialize_list(column, column_data_type, column_num_bytes)
    compressed_column = compress.compress_bitstring(column_codec, serialized_column)
    # print(compressed_column)
    ############
    column_i_TIME = column_i_END - column_i_START
    # print(column_i_TIME, 'for column with codec ', codec, ' to compress')
    column_i_AFTER = sys.getsizeof(compressed_column)
    column_i_RATIO = float(column_i_BEFORE / column_i_AFTER)

    return compressed_column

def comress_with_fastpfor(column, codec):
    """
    compress a column of integers with a codec from fastpfor codecs
    """
    column_i_START = datetime.now()
    column_i_BEFORE = sys.getsizeof(column)

    ### work ###
    # convert input array to numpy array
    np_arr = np.array(column, dtype=np.uint32, order='C')
    np_arr_size = np_arr.size
    buffer_size = 5 * 32
    # allocate space for compressed data
    comp_arr = np.zeros(np_arr_size + buffer_size, dtype=np.uint32, order='C')
    # get codec method from pyfastpfor and use it for compression
    codec_method = getCodec(codec)
    comp_arr_size = codec_method.encodeArray(np_arr, np_arr_size, comp_arr, len(comp_arr))
    ############

    column_i_END = datetime.now()
    column_i_TIME = column_i_END - column_i_START
    # print(column_i_TIME, 'for column with codec ', codec, ' to compress')
    column_i_AFTER = sys.getsizeof(comp_arr[0:comp_arr_size])
    column_i_RATIO = float(column_i_BEFORE / column_i_AFTER)

    #print('pyfast compression: ', column_i_TIME, column_i_RATIO)
    #print(comp_arr[0:comp_arr_size])
    return comp_arr[0:comp_arr_size]
