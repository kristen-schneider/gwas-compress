# python imports
from datetime import datetime
import numpy as np

# personal imports
import compress_column
import type_handling
import serialize_body
import compress
import read_write_compression_times
import read_write_compression_ratios
import plot_bar

def compress_all_blocks(codecs_list, header_first_half, funnel_format_data, data_type_byte_sizes, out_dir):
    """
    returns end of header: [end of block headers, end of blocks, sizes of blocks]

    INPUT
        compression_method_list: list of compression methods for all columns
        header_first_half: data in first half of header
        ff: funnel format
        available_compression_methods: all possible compression methods integrated into workflow

    OUTPUT
        second half of header
    """
    f = open('./testing_write.txt', 'ab')
    f.truncate(0)
    f.close()

    # full header break down
    magic_number = header_first_half[0]
    version = header_first_half[1]
    delimiter = header_first_half[2]
    column_labels = header_first_half[3]
    column_types = header_first_half[4]
    number_columns = header_first_half[5]
    gzip_header = header_first_half[6]

    block_header_ends = []
    block_ends = []

    block_header_end = 0
    block_end = 0

    block_sizes = []
    # go through funnel format, and compress each block
    for block_i in range(len(funnel_format_data)):
        # current block from funnel format
        curr_block = funnel_format_data[block_i]

        curr_block_size = len(curr_block[0])
        if curr_block_size not in block_sizes: block_sizes.append(curr_block_size)

        # compress block
        block_header_and_data = compress_single_block(curr_block, codecs_list, column_types, data_type_byte_sizes)
        block_header = block_header_and_data[0]
        compressed_block = block_header_and_data[1]

        # add to block header ends
        block_header_end += len(block_header)
        block_header_ends.append(block_header_end)
        # add to block ends
        block_end += len(compressed_block)
        block_ends.append(block_end)

        # try:
        #     compressed_block_header = compressed_block_info[0]
        # except TypeError:
        #     print('bad compression of single block.')
        #     return -1
    #     try:
    #         compressed_block_bitstring = compressed_block_info[1]
    #     except TypeError:
    #         print('bad compression of single block.')
    #         return -1
    #     len_curr_block = len(compressed_block_header) + len(compressed_block_bitstring)
    #     block_header_end = (block_end + len(compressed_block_header))
    #     block_end += len_curr_block
    #     block_header_ends.append(block_header_end)
    #     block_ends.append(block_end)
    #
    #     ###
    #     f = open('./testing_write.txt', 'ab')
    #     f.write(compressed_block_header)
    #     f.write(compressed_block_bitstring)
    #     f.close()
    #     ###
    #     # compressed_content += (compressed_block_header + compressed_block_bitstring)
    #
    #     block_i_END = datetime.now()
    #     block_i_TIME = block_i_END - block_i_START
    #     #print(str(block_i_TIME) + ' for block ' + str(block_i + 1) + ' to compress...\n')
    #
    # # block_sizes = header_second_half[2]
    # num_rows_first_block = len(ff[0][0])
    # num_rows_last_block = len(ff[-1][0])
    # block_sizes = [num_rows_first_block, num_rows_last_block]
    if len(block_sizes) < 2: block_sizes.append(curr_block_size)

    header_second_half = [block_header_ends, block_ends, block_sizes]

    return header_second_half

def compress_single_block(curr_block, codecs_list, column_types, data_type_byte_sizes):
    """
    compresses a single block of data, includes a block header which is a list of end positions of all columns

    INPUT
        all_column_compression_times = to track time of compression for each column
        compression_method_list = list of compression methods for all columns
        column_types = data type for each column
        block = all columns are lists of strings, need to type

    OUTPUT
        compressed_block_header_bitstring = serialized, compressed bitstring for header of block (col end positions)
        compressed_block_bitstring = serialized, compressed bitstring for block data

    """
    compressed_block_bitstring = b''

    block_header_compression_method = 'gzip'

    compressed_column_ends_list = []
    compressed_column_end_pos = 0

    for column_i in range(len(curr_block)):
        # column data
        column_compression_method = codecs_list[column_i]
        column_data_type = column_types[column_i]
        column_bytes = data_type_byte_sizes[column_data_type]
        # typed_column = type_handling.convert_to_type(block[column_i], column_data_type)
        to_int_START = datetime.now()
        typed_column = type_handling.string_list_to_int(curr_block[column_i], column_data_type, column_i)
        to_int_END = datetime.now()
        to_int_TIME = to_int_END - to_int_START

        
        # SPLIT ON COMPRESSION INPUT TYPES (serialized data vs array)
        # If we need serialized data to compress (gzip = 1, zlib = 2, bz2 = 3)
        if column_compression_method == 'gzip' \
                or column_compression_method == 'zlib' \
                or column_compression_method == 'bz2':
            # compress column using compress serialized data methods

            compression_timer_start = datetime.now()
            compressed_column = compress_column.compress_single_column_standard(typed_column,
                                                                                column_compression_method,
                                                                                1,
                                                                                data_type_byte_sizes[1])
                                                                                # column_i,
                                                                                # all_column_compression_times,
                                                                                # all_column_compression_size_ratios)
            # print(column_i, datetime.now()-compression_timer_start)
            compressed_block_bitstring += compressed_column

            compressed_column_end_pos += len(compressed_column)
            compressed_column_ends_list.append(compressed_column_end_pos)

        # If we need array data to compress (fastpfor128 = 4 and fastpfor256 = 5)
        elif 'fastpfor' in column_compression_method:
            # match dictionary value to proper codec for pyfastpfor compression
            if column_compression_method == 'fastpfor128':
                codec = 'fastpfor128'
            elif column_compression_method == 'fastpfor256':
                codec = 'fastpfor256'
            else:
                print('Unrecognized compression method. Value not found in compression method code book.')
                return -1
            numpy_compressed_column = compress_column.compress_single_column_pyfast(typed_column,
                                                                                    codec)
                                                                                    # column_i,
                                                                                    # all_column_compression_times,
                                                                                    # all_column_compression_size_ratios)

            serialized_compressed_column = numpy_compressed_column.tobytes(order='C')
            compressed_block_bitstring += serialized_compressed_column

            compressed_column_end_pos += len(serialized_compressed_column)
            compressed_column_ends_list.append(compressed_column_end_pos)

        else:
            print('Unrecognized compression method. Value not found in compression method code book.')
            return -1


    serialized_block_header = serialize_body.serialize_list(compressed_column_ends_list, 1, 4)
    compressed_block_header = compress.compress_bitstring(block_header_compression_method, serialized_block_header)

    return compressed_block_header, compressed_block_bitstring
