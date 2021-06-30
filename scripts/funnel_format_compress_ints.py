# python imports
from datetime import datetime
import sys

# personal imports
import type_handling
import compress
import compress_column
import serialize_body


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
    f = open('testing_write.txt', 'ab')
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

        # compress block
        block_header_and_data = compress_single_block(curr_block, codecs_list, column_types, data_type_byte_sizes)
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

        # WRITE DATA
        f = open('testing_write.txt', 'ab')
        f.write(compressed_block_header)
        #print(compressed_block_header)
        f.write(compressed_block)
        #print(compressed_block)
        f.close()

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
        compressed_block = serialized, compressed bitstring for block data

    """
    compressed_block = b''

    block_header_compression_method = 'gzip'

    block_header = []
    compressed_column_end_pos = 0

    for column_i in range(len(curr_block)):
        # column data
        column_codec = codecs_list[column_i]
        column_data_type = column_types[column_i]
        column_bytes = data_type_byte_sizes[column_data_type]
        # typed_column = type_handling.convert_to_type(block[column_i], column_data_type)

        before_int_size = sys.getsizeof(curr_block[column_i])
        to_int_START = datetime.now()
        typed_column = type_handling.string_list_to_int(curr_block[column_i], column_data_type, column_i)

        #print(typed_column)
        to_int_END = datetime.now()
        to_int_TIME = to_int_END - to_int_START
        after_int_size = sys.getsizeof(typed_column)
        print(before_int_size, after_int_size)

        # codec = codecs_list[0]
        # # SPLIT ON COMPRESSION INPUT TYPES (serialized data vs array)
        # # If we need serialized data to compress (gzip = 1, zlib = 2, bz2 = 3)
        # if column_codec == 'gzip' \
        #         or column_codec == 'zlib' \
        #         or column_codec == 'bz2':
        #     # compress column using compress serialized data methods
        #
        #     compression_timer_start = datetime.now()
        #     compressed_column = compress_column.compress_single_column_standard(typed_column,
        #                                                                         column_codec,
        #                                                                         1,
        #                                                                         data_type_byte_sizes[1])
        #                                                                         # column_i,
        #                                                                         # all_column_compression_times,
        #                                                                         # all_column_compression_size_ratios)
        #     # print(column_i, datetime.now()-compression_timer_start)
        #     compressed_block += compressed_column
        #
        #     compressed_column_end_pos += len(compressed_column)
        #     block_header.append(compressed_column_end_pos)
        #
        # else:
        #     numpy_compressed_column = compress_column.compress_single_column_pyfast(typed_column,
        #                                                                             column_codec)
        #                                                                             # column_i,
        #                                                                             # all_column_compression_times,
        #                                                                             # all_column_compression_size_ratios)
        #
        #     serialized_compressed_column = numpy_compressed_column.tobytes(order='C')
        #     compressed_block += serialized_compressed_column
        #
        #     compressed_column_end_pos += len(serialized_compressed_column)
        #     block_header.append(compressed_column_end_pos)


    # numpy_compressed_block_header = compress_column.compress_single_column_pyfast(block_header, codecs_list[-1])
    # serialized_compressed_block_header = numpy_compressed_block_header.tobytes(order='C')
    gzip_compressed_block_header = compress_column.compress_single_column_standard(block_header, 'gzip',
                                                                                    1, data_type_byte_sizes[1])
    # serialized_compressed_block_header = numpy_compressed_block_header.tobytes(order='C')

    # serialized_block_header = serialize_body.serialize_list(block_header, 1, 4)
    # compressed_block_header = compress.compress_bitstring(block_header_compression_method, serialized_block_header)

    return gzip_compressed_block_header, compressed_block
