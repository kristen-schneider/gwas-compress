import numpy as np
from datetime import datetime
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from utils import type_handling
from utils import encode_as_int
import serialize_body
import compress



serialized_codecs = ['gzip', 'zlib', 'bz2']


def column_compression_main(column, column_codec, column_data_type,
                            curr_compression_data_type, column_data_type_byte_sizes):
    # 1. type column according to desired input type
    if curr_compression_data_type == 1:
        typed_column = encode_as_int.encode_column_as_int(column, column_data_type)

    # 2. compress column according to compression method (serialized vs numpy)
    if column_codec in serialized_codecs:
        compressed_column_bitstring = compress_serialized(column, column_codec, column_data_type, column_data_type_byte_sizes)
    else:
        compressed_column_bitstring = compress_numpy(typed_column, column_codec)
    return compressed_column_bitstring

def compress_serialized(typed_column, column_codec, column_data_type, column_num_bytes):
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
    serialized_column = serialize_body.serialize_list(typed_column, column_data_type, column_num_bytes)
    compressed_column = compress.compress_bitstring(column_codec, serialized_column)
    #
    # column_i_END = datetime.now()
    # column_i_TIME = column_i_END - column_i_START
    # #print(column_i_TIME, 'for column with compression method ', column_compression_method, ' to compress')
    # column_i_AFTER = sys.getsizeof(compressed_column_info[0])
    # column_i_RATIO = float(column_i_BEFORE/column_i_AFTER)

    return compressed_column

def compress_numpy(typed_column, column_codec):
    compressed_column = compress.compress_numpy_array(typed_column, column_codec)
    return compressed_column
