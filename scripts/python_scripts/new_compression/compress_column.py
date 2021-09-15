import numpy as np
from datetime import datetime
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from utils import type_handling
from utils import calculate_size
from utils import encode_as_int
from utils import encode_as_float
import serialize_body
import compress


serialized_codecs = ['gzip', 'zlib', 'bz2']


def column_compression_main(column_i, column, column_codec,
                            curr_compression_data_type, curr_decompression_data_type,
                            column_data_type_byte_sizes,
                            config_file_name):

    column_i_START = datetime.now()
    column_i_STRING_SIZE = sys.getsizeof(column_i)
    m = calculate_size.get_ff_column_size(column)
    
    # 1. convert column to compression data type
    if curr_compression_data_type == 1:
        typed_column = encode_as_int.encode_column_as_int(column, curr_compression_data_type)
    elif curr_compression_data_type == 2:
        typed_column = encode_as_float.encode_column_as_float(column, curr_compression_data_type)
    elif curr_compression_data_type == 3:
        # funnel format data is read in as a string. all columns are strings by default.
        typed_column = column
    else:
        print('unrecognized input data type for type conversion: ', curr_compression_data_type)
    column_i_TYPED_SIZE = sys.getsizeof(typed_column)
    
    # 2. compress column according to compression method (serialized vs numpy)
    if column_codec in serialized_codecs:
        compressed_column_bitstring = compress_serialized(typed_column, column_codec, curr_compression_data_type, column_data_type_byte_sizes)
    else:
        compressed_column_bitstring = compress_numpy(typed_column, column_codec)
    column_i_END = datetime.now()
    column_i_TIME = column_i_END - column_i_START
    column_i_COMPRESSED_SIZE = sys.getsizeof(compressed_column_bitstring)
    n = calculate_size.get_bitstring_column_size(compressed_column_bitstring) 
    column_i_SIZE_RATIO = float(column_i_STRING_SIZE/column_i_COMPRESSED_SIZE)
    column_i_mn = float(m/n)
    print(config_file_name, "col"+str(column_i), 'compression_time', column_i_TIME)
    print(config_file_name, "col"+str(column_i), 'compression_ratio', column_i_mn)
    #print(column, typed_column, compressed_column_bitstring)
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
    serialized_column = serialize_body.serialize_list(typed_column, column_data_type, column_num_bytes)
    compressed_column = compress.compress_bitstring(serialized_column, column_codec)
    return compressed_column

def compress_numpy(typed_column, column_codec):
    """
    compresses a single column of data using methods that take in numpy data (e.g. pyfast)

    INPUT
        typed_column = column as proper type (list of whatever data type is specified by config file)
        column_codec = method of compression for given column

    OUTPUT
        compressed_column = compressed data in bitstring form
    """
    compressed_column = compress.compress_numpy_array(typed_column, column_codec)
    return compressed_column
