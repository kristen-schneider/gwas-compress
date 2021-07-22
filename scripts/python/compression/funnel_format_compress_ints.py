# python imports
from datetime import datetime
import numpy as np

# personal imports
from scripts.python.utils import type_handling
import compress_column


def compress_all_blocks(codecs_list, header_first_half, funnel_format_data, data_type_byte_sizes):
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


    # to track compression sizes (bytes)
    string_block_storage = {column_list: [] for column_list in range(number_columns)}
    int_block_storage = {column_list: [] for column_list in range(number_columns)}
    compressed_block_storage = {column_list: [] for column_list in range(number_columns)}


    for block_i in range(len(funnel_format_data)):
        #print(block_i)
        # current block from funnel format
        curr_block = funnel_format_data[block_i]

        # compress block
        block_header_and_data = compress_single_block(curr_block,
                                                      codecs_list,
                                                      column_types,
                                                      data_type_byte_sizes,
                                                      string_block_storage,
                                                      int_block_storage,
                                                      compressed_block_storage)
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


    print(string_block_storage)
    print(int_block_storage)
    print(compressed_block_storage)
    
    
    header_second_half = [block_header_ends, block_ends, block_sizes]
    col_byte_info = [string_block_storage, int_block_storage, compressed_block_storage]
    return header_second_half, col_byte_info

def compress_single_block(curr_block, codecs_list, column_types, data_type_byte_sizes, string_block_storage, int_block_storage, compressed_block_storage):
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
    
    compressed_block_serialized = b''
    compressed_block = np.empty(0, dtype=np.uint32, order='C')    
    compressed_block_no_compression = []
    block_header_compression_method = 'gzip'

    block_header = []
    compressed_column_end_pos = 0


    for column_i in range(len(curr_block)):
        # column data
        column_codec = codecs_list[column_i]
        column_data_type = column_types[column_i]
        column_bytes = data_type_byte_sizes[column_data_type]
        # typed_column = type_handling.convert_to_type(block[column_i], column_data_type)
        
        # fill size of string block (bytes)
        # string = 1 byte per character = 1 x len(string)
        #string_byte_storage = sys.getsizeof([])
        string_byte_storage = 0
        for data in curr_block[column_i]:
            string_byte_storage += len(data)
            #string_byte_storage += sys.getsizeof(data)
        string_block_storage[column_i].append(string_byte_storage)

        to_int_START = datetime.now()
        typed_column = type_handling.string_list_to_int(curr_block[column_i], column_data_type, column_i)
        
        # fill size of typed block (bytes)
        # int is 4 bytes
        int_byte_storage = 0
        for data in typed_column:
            int_byte_storage += 4
            #int_byte_storage += len(data.encode("utf8"))
        int_block_storage[column_i].append(int_byte_storage)

        to_int_START = datetime.now()
        typed_column = type_handling.string_list_to_int(curr_block[column_i], column_data_type, column_i)

        #print(typed_column)
        to_int_END = datetime.now()
        to_int_TIME = to_int_END - to_int_START

        codec = codecs_list[0]
        # SPLIT ON COMPRESSION INPUT TYPES (serialized data vs array)
        # If we need serialized data to compress (gzip = 1, zlib = 2, bz2 = 3)
        if column_codec == 'gzip' \
                or column_codec == 'zlib' \
                or column_codec == 'bz2':
            # compress column using compress serialized data methods

            compression_timer_start = datetime.now()
            compressed_column = compress_column.compress_single_column_standard(typed_column,
                                                                                column_codec,
                                                                                1,
                                                                                data_type_byte_sizes[1])
                                                                                # column_i,
                                                                                # all_column_compression_times,
                                                                                # all_column_compression_size_ratios)
            # print(column_i, datetime.now()-compression_timer_start)
            compressed_block += compressed_column

            compressed_column_end_pos += len(compressed_column)
            block_header.append(compressed_column_end_pos)

        else:
            numpy_compressed_column = compress_column.compress_single_column_pyfast(typed_column,
                                                                                    column_codec)
                                                                                    # column_i,
                                                                                    # all_column_compression_times,
                                                                                    # all_column_compression_size_ratios)

            serialized_compressed_column = numpy_compressed_column.tobytes(order='C')
            compressed_block_no_compression.append(typed_column)
            compressed_block_serialized += serialized_compressed_column
            compressed_block = np.append(compressed_block, numpy_compressed_column)
            compressed_column_end_pos += len(serialized_compressed_column)
            block_header.append(compressed_column_end_pos)

            # fill size of compressed block (bytes)
            compressed_byte_storage = 0
            for data in numpy_compressed_column:
                compressed_byte_storage += 4
                #compressed_byte_storage += len(data.encode("utf8"))
            compressed_block_storage[column_i].append(compressed_byte_storage)

        #print('np compressed column: ', numpy_compressed_column.itemsize*numpy_compressed_column.size)    
    numpy_compressed_block_header = compress_column.compress_single_column_pyfast(block_header, codecs_list[-1])
    serialized_compressed_block_header = numpy_compressed_block_header.tobytes(order='C')

    #gzip_compressed_block_header = compress_column.compress_single_column_standard(block_header, 'gzip', 1, data_type_byte_sizes[1])
    # serialized_compressed_block_header = numpy_compressed_block_header.tobytes(order='C')

    # serialized_block_header = serialize_body.serialize_list(block_header, 1, 4)
    # compressed_block_header = compress.compress_bitstring(block_header_compression_method, serialized_block_header)
    #print(compressed_block.itemsize*compressed_block.size)
    #print(compressed_block.tobytes(order='C'))
    #print(compressed_block)
    return numpy_compressed_block_header, compressed_block
