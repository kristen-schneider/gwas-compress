# python_scripts imports
from datetime import datetime
import numpy as np
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

# personal imports
from utils import type_handling
import compress_block


def compress_all_blocks(CODECS_LIST, INPUT_DATA_TYPE_LIST, DATA_TYPE_BYTE_SIZES,
                        header_first_half, funnel_format_data):
    """
    returns end of header: [end of block headers, end of blocks, sizes of blocks]

    INPUT
        CODECS_LIST: list of compression methods to use on columns
        INPUT_DATA_TYPE_LIST: list of data types to convert each column
        DATA_TYPE_BYTE_SIZES: byte sizes for each data type
        header_first_half: first half of header
        funnel_format_data: funnel format data (all data is in strings)

    OUTPUT
        compresses data and returns second half of header
    """

    # full header break down
    magic_number = header_first_half[0]
    version = header_first_half[1]
    delimiter = header_first_half[2]
    column_labels = header_first_half[3]
    column_types = header_first_half[4]
    number_columns = header_first_half[5]

    # ends of block headers
    # block header = [10, 20, 30, 40, ...] where each number is the end of a compressed column bitstring
    # block header ends = [10, 100, ...] where each number is the end of a bitstring which represents a block header
    block_header_ends = []
    # block ends = [90, 190, ...] where each number is the end of a bitstring which represents a full block
    # ends of blocks
    block_ends = []

    block_header_end = 0
    block_end = 0

    block_sizes = []
    # go through funnel format, and compress each block


    for block_i in range(len(funnel_format_data)):

        # current block from funnel format
        curr_block = funnel_format_data[block_i]

        # compress block
        block_header_and_data = compress_block.compress_block(curr_block,
                                                              CODECS_LIST,
                                                              column_types,
                                                              DATA_TYPE_BYTE_SIZES)
        compressed_block_header = block_header_and_data[0]
        compressed_block = block_header_and_data[1]
        # HEADER END DATA
        # add to block header ends
        try:
            block_header_end = (block_ends[block_i-1]+len(compressed_block_header))
        except IndexError:
            block_header_end += (0+len(compressed_block_header))    
        block_header_ends.append(block_header_end)
        
        # add to block ends
        try:
            block_end = (block_header_ends[block_i]+len(compressed_block))
        except IndexError:
            block_end += (block_header_end+len(compressed_block))
        block_ends.append(block_end)
        
        # block sizes
        curr_block_size = len(curr_block[0])
        if curr_block_size not in block_sizes: block_sizes.append(curr_block_size)
    


    if len(block_sizes) < 2: block_sizes.append(curr_block_size)


    
    header_second_half = [block_header_ends, block_ends, block_sizes]
    return header_second_half
#
# def compress_single_block(curr_block, codecs_list, column_types, data_type_byte_sizes):
#     """
#     compresses a single block of data, includes a block header which is a list of end positions of all columns
#
#     INPUT
#         all_column_compression_times = to track time of compression for each column
#         compression_method_list = list of compression methods for all columns
#         column_types = data type for each column
#         block = all columns are lists of strings, need to type
#
#     OUTPUT
#         compressed_block_header_bitstring = serialized, compressed bitstring for header of block (col end positions)
#         compressed_block = serialized, compressed bitstring for block data
#
#     """
#
#     compressed_block_serialized = b''
#     compressed_block = np.empty(0, dtype=np.uint32, order='C')
#     compressed_block_no_compression = []
#     block_header_compression_method = 'gzip'
#
#     block_header = []
#     compressed_column_end_pos = 0
#
#
#     for column_i in range(len(curr_block)):
#         # column data
#         column_codec = codecs_list[column_i]
#         column_data_type = column_types[column_i]
#         column_bytes = data_type_byte_sizes[column_data_type]
#         # typed_column = type_handling.convert_to_type(block[column_i], column_data_type)
#
#
#         to_int_START = datetime.now()
#         typed_column = type_handling.string_list_to_int(curr_block[column_i], column_data_type, column_i)
#
#         #print(typed_column)
#         to_int_END = datetime.now()
#         to_int_TIME = to_int_END - to_int_START
#
#         codec = codecs_list[0]
#         # SPLIT ON COMPRESSION INPUT TYPES (serialized data vs array)
#         # If we need serialized data to compress (gzip = 1, zlib = 2, bz2 = 3)
#         if column_codec == 'gzip' \
#                 or column_codec == 'zlib' \
#                 or column_codec == 'bz2':
#             # compress column using compress serialized data methods
#
#             compression_timer_start = datetime.now()
#             compressed_column = compress_column.compress_single_column_standard(typed_column,
#                                                                                 column_codec,
#                                                                                 1,
#                                                                                 data_type_byte_sizes[1])
#                                                                                 # column_i,
#                                                                                 # all_column_compression_times,
#                                                                                 # all_column_compression_size_ratios)
#             # print(column_i, datetime.now()-compression_timer_start)
#             compressed_block += compressed_column
#
#             compressed_column_end_pos += len(compressed_column)
#             block_header.append(compressed_column_end_pos)
#
#         else:
#             numpy_compressed_column = compress_column.compress_single_column_pyfast(typed_column,
#                                                                                     column_codec)
#                                                                                     # column_i,
#                                                                                     # all_column_compression_times,
#                                                                                     # all_column_compression_size_ratios)
#
#             serialized_compressed_column = numpy_compressed_column.tobytes(order='C')
#             compressed_block_no_compression.append(typed_column)
#             compressed_block_serialized += serialized_compressed_column
#             compressed_block = np.append(compressed_block, numpy_compressed_column)
#             compressed_column_end_pos += len(serialized_compressed_column)
#             block_header.append(compressed_column_end_pos)
#
#
#         #print('np compressed column: ', numpy_compressed_column.itemsize*numpy_compressed_column.size)
#     numpy_compressed_block_header = compress_column.compress_single_column_pyfast(block_header, codecs_list[-1])
#     serialized_compressed_block_header = numpy_compressed_block_header.tobytes(order='C')
#
#     #gzip_compressed_block_header = compress_column.compress_single_column_standard(block_header, 'gzip', 1, data_type_byte_sizes[1])
#     # serialized_compressed_block_header = numpy_compressed_block_header.tobytes(order='C')
#
#     # serialized_block_header = serialize_body.serialize_list(block_header, 1, 4)
#     # compressed_block_header = compress.compress_bitstring(block_header_compression_method, serialized_block_header)
#     #print(compressed_block.itemsize*compressed_block.size)
#     #print(compressed_block.tobytes(order='C'))
#     #print(compressed_block)
#     return numpy_compressed_block_header, compressed_block
