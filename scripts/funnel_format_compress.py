from datetime import datetime
import compress_serialized_data
#import compress_array_data
import type_handling
import serialize
import compress

def compress_all_blocks(data_type_code_book, data_type_byte_sizes,
                        compression_method_list, compression_method_code_book,
                        mtime, header_first_half, ff):
    """
    returns 3 pieces of data which summarize serialized, compressed data

    INPUT
        data_type_code_book: e.g. {int: 1, float: 2, str: 3, bytes:4}
        data_type_byte_sizes: from config file, assigns bytes to each data type, for compression
        compression_method_list: list of compression methods for all columns
        compression_method_code_book: e.g. {'gzip':1, 'zlib':2, 'bz2':3}
        mtime: for gzip.compress input
        header_first_half: data in first half of header
        ff: funnel format

    OUTPUT
        second half of header
        all serialized, compressed data from blocks (header and data)
        compression times for each column //this bit is not included in new version
    """
    magic_number = header_first_half[0]
    version = header_first_half[1]
    delimiter = header_first_half[2]
    column_labels = header_first_half[3]
    column_types = header_first_half[4]
    number_columns = header_first_half[5]
    gzip_header = header_first_half[6]

    block_header_ends = []
    block_ends = []
    block_sizes = []
    header_second_half = [[] for i in range(3)]  # last half of header
    compressed_content = b''

    block_header_end = 0
    block_end = 0
    all_column_compression_times = dict()

    # go through funnel format, and compress each block
    for block_i in range(len(ff)):
        # start timer for block
        # print('block ' + str(block_i))
        block_i_START = datetime.now()

        # current block from funnel format
        curr_block = ff[block_i]

        compressed_block_info = compress_single_block(all_column_compression_times, data_type_code_book,
                                                      data_type_byte_sizes, compression_method_list,
                                                      compression_method_code_book, mtime, column_types,
                                                      curr_block)
        compressed_block_header = compressed_block_info[0]
        compressed_block_bitstring = compressed_block_info[1]

        len_curr_block = len(compressed_block_header)+len(compressed_block_bitstring)
        block_header_end = (block_end+len(compressed_block_header))
        block_end += len_curr_block
        block_header_ends.append(block_header_end)
        block_ends.append(block_end)
        compressed_content += (compressed_block_header+compressed_block_bitstring)

        # # returns full_header_end and final compressed block
        # block_compression_info = old_compress_single_block(all_column_compression_times, data_type_code_book,
        #                                                data_type_byte_sizes, compression_method_list,
        #                                                compression_method_code_book, mtime, column_labels,
        #                                                column_types, header_second_half, block_end, curr_block)
        #
        # header_second_half = block_compression_info[0]
        # compressed_block = block_compression_info[1]
        # compressed_content += compressed_block
        # compressed_content += compressed_block_bitstring
        #
        # # block_end = header_second_half[1][-1]

        block_i_END = datetime.now()
        block_i_TIME = block_i_END - block_i_START
        print(str(block_i_TIME) + ' for block ' + str(block_i) + ' to compress...\n')

    # block_sizes = header_second_half[2]
    num_rows_first_block = len(ff[0][0])
    num_rows_last_block = len(ff[-1][0])
    block_sizes = [num_rows_first_block, num_rows_last_block]

    header_second_half = [block_header_ends, block_ends, block_sizes]

    return header_second_half, compressed_content, all_column_compression_times

def compress_single_block(all_column_compression_times, data_type_code_book, data_type_byte_sizes,
                          compression_method_list, compression_method_code_book,
                          mtime, column_types, block):
    """
    compresses a single block of data, includes a block header which is a list of end positions of all columns

    INPUT
        all_column_compression_times
        data_type_code_book = e.g. {int: 1, float: 2, str: 3, bytes:4}
        data_type_byte_sizes = from config file, assigns bytes to each data type, for compression
        compression_method_list = list of compression methods for all columns
        compression_method_code_book = e.g. {'gzip':1, 'zlib':2, 'bz2':3}
        mtime = for gzip.compress input
        column_types = data type for each column
        block = all columns are lists of strings, need to type

    OUTPUT
        compressed_block_header_bitstring = serialized, compressed bitstring for header of block (col end positions)
        compressed_block_bitstring = serialized, compressed bitstring for block data

    """
    compressed_block_bitstring = b''

    block_header_type = data_type_code_book[int]
    block_header_bytes = data_type_byte_sizes[block_header_type]
    block_header_compression_method = compression_method_code_book['gzip']

    compressed_column_ends_list = []
    compressed_column_end_pos = 0
    for column_i in range(len(block)):
        # column data
        column_compression_method = compression_method_code_book[compression_method_list[column_i]]
        column_data_type = column_types[column_i]
        column_bytes = data_type_byte_sizes[column_data_type]
        typed_column = type_handling.convert_to_type(block[column_i], column_data_type)

        
        # SPLIT ON COMPRESSION INPUT TYPES (serialized data vs array)
        print(column_compression_method)

        # If we need serialized data to compress (gzip = 1, zlib = 2, bz2 = 3)
        if column_compression_method <= 3:
            # compress column using compress serialized data methods
            compressed_column_info = compress_serialized_data.compress_single_column(typed_column, column_compression_method, column_data_type,
                                                   column_bytes, mtime)

            compressed_column_header_length = compressed_column_info[1] # length of header for compression type (e.g. 10 for gzip)
            compressed_column_bitstring = compressed_column_info[0][compressed_column_header_length:] # bitstring of compressed dataa
            compressed_block_bitstring += compressed_column_bitstring

            compressed_column_end_pos += len(compressed_column_bitstring)
            compressed_column_ends_list.append(compressed_column_end_pos)

        # If we need array data to compress (fastpfor128 = 4 and fastpfor256 = 5)
        elif column_compression_method == 4 or column_compression_method == 5:
            # match dictionary value to proper codec for pyfastpfor compression
            if column_compression_method == 4: codec = 'fastpfor128'
            elif column_compression_method == 5: codec == 'fastpfor256'
            numpy_compressed_column = compress_array_data.compress_single_column(typed_column, codec)     
            serialized_compressed_column = serialize.serialize_list(numpy_compressed_column, column_data_type, column_bytes)
            
            compressed_block_bitstring += serialized_compressed_column
            
            compressed_column_end_pos += len(serialized_compressed_column)
            compressed_column_ends_list.append(compressed_column_end_pos)
            #print(type(numpy_compressed_column), numpy_compressed_column)       
            #print(type(serialized_compressed_column), serialized_compressed_column)
            
        else:
            print('Unrecognized compression method. Value not found in compression method code book.')
            return -1
            
    serialized_block_header = serialize.serialize_list(compressed_column_ends_list, block_header_type, block_header_bytes)
    compressed_block_header_info = compress.compress_data(block_header_compression_method, serialized_block_header, mtime)
    compressed_block_header_compression_method_length = compressed_block_header_info[1]
    compressed_block_header_bitstring = compressed_block_header_info[0][compressed_block_header_compression_method_length:]

    return compressed_block_header_bitstring, compressed_block_bitstring

# def compress_single_column(typed_column, column_compression_method, column_type, column_bytes, mtime):
#     """
#     compresses a single column of data
#
#     INPUT
#         typed_column = column as proper type (list of ints, rather than strings)
#         column_compression_method = method of compression for given column
#         column_type = data type for given column
#         column_bytes = number of bytes used for compression
#         mtime = for gzip.compress input
#
#     OUTPUT
#         compressed_column_info = compressed data and length of header which would help decompress data
#     """
#     serialized_column = serialize.serialize_list(typed_column, column_type, column_bytes)
#     compressed_column_info = compress.compress_data(column_compression_method, serialized_column, mtime)
#     return compressed_column_info

# def old_compress_single_block(all_column_compression_times, data_type_code_book, data_type_byte_sizes,
#                           compression_method, compression_method_code_book,
#                           mtime, column_labels, column_types, header_end, block_end, block):
#     """
#     compresses a single block of data
#
#     INPUT
#         all_column_compression_times:
#         data_type_code_book:
#         data_type_byte_sizes:
#         compression_method:
#         compression_method_code_book,
#         mtime:
#         column_labels:
#         column_types:
#         header_end:
#         block_end:
#         block:
#
#     OUTPUT
#
#     """
#     compressed_block_header = b''
#     compressed_block = b''
#     compressed_block_final = b''
#
#     HEADER_block_header_ends = header_end[0]
#     HEADER_block_ends = header_end[1]
#     HEADER_block_num_rows = header_end[2]
#
#     block_header_compression_method = 'gzip'
#     block_header_compression_size = 10
#
#     num_cols_in_block = len(block)
#     num_rows_in_block = len(block[0])
#     # this should only be triggered for first block and last block.
#     if num_rows_in_block not in HEADER_block_num_rows:
#         HEADER_block_num_rows.append(num_rows_in_block)
#
#     # COLUMN COMPRESSION AND BLOCK HEADER INFO
#     block_col_ends = []
#     curr_compressed_col_end = 0
#     for column_i in range(len(block)):
#         column_i_START = datetime.now()
#
#         # get column info
#         curr_column = block[column_i]
#         column_type = column_types[column_i]
#         typed_column = type_handling.convert_to_type(curr_column, column_type)
#         column_bytes = data_type_byte_sizes[column_type]
#         column_compression_method = compression_method_code_book[compression_method[column_i]]
#
#         # serialize and compress a column
#         s_column = serialize.serialize_list(typed_column, column_type, column_bytes)
#         compressed_column_info = compress.compress_data(column_compression_method, s_column, 0)
#         compression_method_header_size = compressed_column_info[1]
#         s_c_column = compressed_column_info[0][compression_method_header_size:]  # remove the gzip header bit from the compressed data
#         compressed_block += s_c_column
#
#         # add length of this column to lengths of columns in this block
#         curr_compressed_col_end += len(s_c_column)
#         block_col_ends.append(curr_compressed_col_end)
#
#         column_i_END = datetime.now()
#         column_i_compression_time = column_i_END-column_i_START
#
#         try:
#             all_column_compression_times[column_labels[column_i]] += column_i_compression_time
#         except KeyError:
#             all_column_compression_times[column_labels[column_i]] = column_i_compression_time
#
#     # write the compressed block header and compressed block to the file
#     s_block_header = serialize.serialize_list(block_col_ends, data_type_code_book[type(block_col_ends[0])],
#                                               data_type_byte_sizes[1])
#
#     compressed_block_header_info = compress.compress_data(compression_method_code_book[block_header_compression_method],
#                                                           s_block_header, mtime)
#     compressed_block_header = compressed_block_header_info[0][block_header_compression_size:]
#
#     block_header_length = len(compressed_block_header)
#     block_header_end = (block_header_length + block_end)
#     HEADER_block_header_ends.append(block_header_end)
#
#     block_length = len(compressed_block)
#
#     block_end += (block_header_length + block_length)
#     HEADER_block_ends.append(block_end)
#
#     compressed_block_final += compressed_block_header
#     compressed_block_final += compressed_block
#
#     header_end = [HEADER_block_header_ends, HEADER_block_ends, HEADER_block_num_rows]
#
#     return header_end, compressed_block_final


