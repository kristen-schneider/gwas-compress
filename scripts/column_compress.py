import numpy as np
from datetime import datetime
import sys
# from pyfastpfor import *
def compress_block(num_columns, block_as_columns_ints, codecs_list):
    """

    """
    compressed_block = []
    for col_index in range(num_columns):
        column_codec = codecs_list[col_index]
        curr_column = block_as_columns_ints[col_index]

        # gzip, zlib, and bz2 codecs
        if column_codec == 'gzip' \
            or column_codec == 'zlib' \
            or column_codec == 'bz2':
            compressed_block.append(compress_with_other(curr_column, column_codec))

        # fastpfor codecs
        else:
            compressed_block.append(comress_with_fastpfor(curr_column, column_codec))



def compress_with_other(column, column_codec):
    """
    compress a column of integers with gzip, zlib, or bz2
    """
    compressed_column = b''
    column_i_START = datetime.now()
    column_i_BEFORE = sys.getsizeof(column)
    column_i_END = datetime.now()
    ### work ###

    ############
    column_i_TIME = column_i_END - column_i_START
    # print(column_i_TIME, 'for column with codec ', codec, ' to compress')
    column_i_AFTER = sys.getsizeof(compressed_column)
    column_i_RATIO = float(column_i_BEFORE / column_i_AFTER)



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
    return comp_arr