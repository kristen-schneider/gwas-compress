from datetime import datetime
import compress_column
import type_handling
import serialize
import compress
import write_compression_times

def compress_all_blocks(data_type_code_book,
                        data_type_byte_sizes,
                        compression_method_list,
                        header_first_half, ff,
                        compression_times_file):
    """
    returns 3 pieces of data which summarize serialized, compressed data

    INPUT
        data_type_code_book: e.g. {int: 1, float: 2, str: 3, bytes:4}
        data_type_byte_sizes: from config file, assigns bytes to each data type, for compression
        compression_method_list: list of compression methods for all columns
        header_first_half: data in first half of header
        ff: funnel format

    OUTPUT
        second half of header
        all serialized, compressed data from blocks (header and data)
        compression times for each column //this bit is not included in new version
    """
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
    compressed_content = b''

    block_header_end = 0
    block_end = 0

    # to track times of compression:
    # dictionary: [column1: [block1, block2, ..., blockn]]
    num_blocks = len(block_ends)
    all_column_compression_times = {}
    for col in range(number_columns):
        all_column_compression_times[col] = []

    # go through funnel format, and compress each block
    for block_i in range(len(ff)):
        # start timer for block
        # print('block ' + str(block_i))
        block_i_START = datetime.now()

        # current block from funnel format
        curr_block = ff[block_i]

        compressed_block_info = compress_single_block(all_column_compression_times, data_type_code_book,
                                                      data_type_byte_sizes, compression_method_list,
                                                      column_types, curr_block)
        compressed_block_header = compressed_block_info[0]
        compressed_block_bitstring = compressed_block_info[1]

        len_curr_block = len(compressed_block_header)+len(compressed_block_bitstring)
        block_header_end = (block_end+len(compressed_block_header))
        block_end += len_curr_block
        block_header_ends.append(block_header_end)
        block_ends.append(block_end)
        compressed_content += (compressed_block_header+compressed_block_bitstring)

        block_i_END = datetime.now()
        block_i_TIME = block_i_END - block_i_START
        print(str(block_i_TIME) + ' for block ' + str(block_i+1) + ' to compress...\n')

    # block_sizes = header_second_half[2]
    num_rows_first_block = len(ff[0][0])
    num_rows_last_block = len(ff[-1][0])
    block_sizes = [num_rows_first_block, num_rows_last_block]

    header_second_half = [block_header_ends, block_ends, block_sizes]

    write_compression_times.write_times(all_column_compression_times, compression_times_file)

    return header_second_half, compressed_content

def compress_single_block(all_column_compression_times, data_type_code_book, data_type_byte_sizes,
                          compression_method_list, column_types, block):
    """
    compresses a single block of data, includes a block header which is a list of end positions of all columns

    INPUT
        all_column_compression_times = to track time of compression for each column
        data_type_code_book = e.g. {int: 1, float: 2, str: 3, bytes:4}
        data_type_byte_sizes = from config file, assigns bytes to each data type, for compression
        compression_method_list = list of compression methods for all columns
        column_types = data type for each column
        block = all columns are lists of strings, need to type

    OUTPUT
        compressed_block_header_bitstring = serialized, compressed bitstring for header of block (col end positions)
        compressed_block_bitstring = serialized, compressed bitstring for block data

    """
    compressed_block_bitstring = b''

    block_header_type = data_type_code_book[int]
    block_header_bytes = data_type_byte_sizes[block_header_type]
    block_header_compression_method = 'gzip'

    compressed_column_ends_list = []
    compressed_column_end_pos = 0
    for column_i in range(len(block)):
        # column data
        column_compression_method = compression_method_list[column_i]
        column_data_type = column_types[column_i]
        column_bytes = data_type_byte_sizes[column_data_type]
        typed_column = type_handling.convert_to_type(block[column_i], column_data_type)

        
        # SPLIT ON COMPRESSION INPUT TYPES (serialized data vs array)
        #print(column_compression_method)
        # If we need serialized data to compress (gzip = 1, zlib = 2, bz2 = 3)
        if column_compression_method == 'gzip' \
                or column_compression_method == 'zlib' \
                or column_compression_method == 'bz2':
            # compress column using compress serialized data methods
            compressed_column_info = compress_column.compress_single_column_reg(typed_column,
                                                                                column_compression_method,
                                                                                column_data_type,
                                                                                column_bytes,
                                                                                column_i,
                                                                                all_column_compression_times)

            compressed_column_header_length = compressed_column_info[0][1] # length of header for compression type (e.g. 10 for gzip)
            compressed_column_bitstring = compressed_column_info[0][0][compressed_column_header_length:] # bitstring of compressed dataa
            compressed_block_bitstring += compressed_column_bitstring

            compress_column_times = compressed_column_info[1]

            compressed_column_end_pos += len(compressed_column_bitstring)
            compressed_column_ends_list.append(compressed_column_end_pos)

        # If we need array data to compress (fastpfor128 = 4 and fastpfor256 = 5)
        elif 'fastpfor' in column_compression_method:
            # match dictionary value to proper codec for pyfastpfor compression
            if column_compression_method == 'fastpfor128': codec = 'fastpfor128'
            elif column_compression_method == 'fastpfor256': codec == 'fastpfor256'
            numpy_compressed_column = compress_column.compress_single_column_pyfast(typed_column,
                                                                                    codec,
                                                                                    column_i,
                                                                                    all_column_compression_times)
            # must serialize a numpy column in order for the column to be properly written to our output file
            serialized_compressed_column = serialize.serialize_list(numpy_compressed_column, column_data_type, column_bytes)
            
            compressed_block_bitstring += serialized_compressed_column

            compress_column_times = compressed_column_info[1]
            
            compressed_column_end_pos += len(serialized_compressed_column)
            compressed_column_ends_list.append(compressed_column_end_pos)

        else:
            print('Unrecognized compression method. Value not found in compression method code book.')
            return -1
            
    serialized_block_header = serialize.serialize_list(compressed_column_ends_list, block_header_type, block_header_bytes)
    compressed_block_header_info = compress.compress_bitstring(block_header_compression_method, serialized_block_header)
    compressed_block_header_compression_method_length = compressed_block_header_info[1]
    compressed_block_header_bitstring = compressed_block_header_info[0][compressed_block_header_compression_method_length:]

    return compressed_block_header_bitstring, compressed_block_bitstring


