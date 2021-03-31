# IMPORTS
import sys
from datetime import datetime
import generate_header_first_half
import funnel_format
import type_handling
import multiprocessing
from multiprocessing.pool import Pool
import funnel_format_compression
import serialize
import compress
import header_compress_decompress


# PARATMETERS
IN_FILE = sys.argv[1]
OUT_FILE = sys.argv[2]
BLOCK_SIZE = int(sys.argv[3])

DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes:4}
DATA_TYPE_BYTE_SIZES = {1: 5, 2: 8, 3: 5, 4:None}
COMPRESSION_METHOD_CODE_BOOK = {'gzip':1, 'zlib':2}

# IN FILE
#'/Users/kristen/Desktop/compression_sandbox/toy_data/
# FIJI: '/scratch/Users/krsc0813/gwas-compress/data/test-gwas-data/test.tsv'

# OUT FILE
# '/Users/kristen/Desktop/compression_sandbox/toy_data/'
# FIJI: '/scratch/Users/krsc0813/gwas-compress/data/compressed/'

def new_main():
    # 1. GET FIRST HALF OF HEADER
    ### Magic number, version number, delimiter, column labels, column types, number columns, gzip header
    ### [1,1,'\t',['chr', 'pos', 'ref', 'alt', 'af_cases_EUR', 'af_controls_EUR', 'beta_EUR', 'se_EUR', 'pval_EUR', 'low_confidence_EUR'],[1, 1, 3, 3, 2, 2, 2, 2, 2, 3],10,b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff']
    print('generating start of header...')
    header_first_half_START = datetime.now()
    ### work ###
    header_first_half = generate_header_first_half.get_header_data(IN_FILE, DATA_TYPE_CODE_BOOK)
    ############
    header_first_half_END = datetime.now()
    header_first_half_TIME = header_first_half_END - header_first_half_START
    print(str(header_first_half_TIME) + ' for header start to compute...\n')

    magic_number = header_first_half[0]
    version = header_first_half[1]
    delimiter = header_first_half[2]
    column_labels = header_first_half[3]
    column_types = header_first_half[4]
    number_columns = header_first_half[5]
    gzip_header = header_first_half[6]

    # 2. GET FUNNEL FORMAT
    ### list of blocks [[block1][block2]...[blockn]]
    ### --> a block is a list of columns: block1 = [[col1], [co2]...[colm]]
    ### -----> a column is a list of string values: col1 = ['1','1','1','1','1']
    print('generating funnel format...')
    funnel_format_START = datetime.now()
    ### work ###
    funnel_format_data = funnel_format.make_all_blocks(IN_FILE, BLOCK_SIZE, number_columns, delimiter)
    ############
    funnel_format_END = datetime.now()
    funnel_format_TIME = funnel_format_END - funnel_format_START
    print(str(funnel_format_TIME) + ' for funnel format to compute...\n')

    # 3. COMPRESS DATA, GET SECOND HALF OF HEADER
    print('compressing data...')
    compress_data_START = datetime.now()
    ### work ###
    serialize_compress_data = serialize_and_compress_funnel_format(COMPRESSION_METHOD_CODE_BOOK['gzip'],
                                                                   funnel_format_data, column_types)
    header_second_half = serialize_compress_data[0]
    all_compressed_content = serialize_compress_data[1]
    ############
    compress_data_END = datetime.now()
    compress_data_TIME = compress_data_END - compress_data_START
    print(str(compress_data_TIME) + ' for full compression to complete...\n')

    # 4. COMPRESS HEADER
    print('compressing header...')
    compress_header_START = datetime.now()
    ### work ###
    # full header and compressed data
    compressed_info = get_full_header()
    full_header = compressed_info[0]
    compressed_content = compressed_info[1]

    # header types, number of elements in each header
    serialized_header_tools = header_compress_decompress.full_header_tools(full_header)
    serialized_header_types = serialized_header_tools[0]
    serialized_header_num_elements = serialized_header_tools[1]
    serialized_header_ends = serialized_header_tools[2]
    serialized_header_data = serialized_header_tools[3]

    size_types = len(serialized_header_types)
    bytes_size_types = size_types.to_bytes(2, byteorder='big', signed=False)
    size_elements = len(serialized_header_num_elements)
    bytes_size_num_elements = size_elements.to_bytes(2, byteorder='big', signed=False)
    size_ends = len(serialized_header_ends)
    bytes_size_ends = size_ends.to_bytes(2, byteorder='big', signed=False)
    size_data = len(serialized_header_data)
    bytes_size_data = size_data.to_bytes(2, byteorder='big', signed=False)
    ############
    compress_header_END = datetime.now()
    compress_header_TIME = compress_header_END - compress_header_START
    print(str(compress_header_TIME) + ' for header to compress...\n')


    # 5. WRITE COMPRESSED HEADER
    print('writing header...')
    write_header_START = datetime.now()
    ### work ###
    compressed_with_header = open(OUT_FILE + 'kristen-' + str(BLOCK_SIZE) + '-out.tsv', 'wb')
    # write how many bytes are needed to store types, ends, and data (CONSTANT FIRST 4 BYTES)
    compressed_with_header.write(bytes_size_types)
    compressed_with_header.write(bytes_size_num_elements)
    compressed_with_header.write(bytes_size_ends)
    compressed_with_header.write(bytes_size_data)

    # write header types and header ends (serialized)
    compressed_with_header.write(serialized_header_types)
    compressed_with_header.write(serialized_header_num_elements)
    compressed_with_header.write(serialized_header_ends)

    # write header (serialized)
    compressed_with_header.write(serialized_header_data)
    ############
    write_header_END = datetime.now()
    write_header_TIME = write_header_END - write_header_START
    print(str(write_header_TIME) + ' for header to write...\n')

    # 6. WRITE COMPRESSED DATA
    print('writing data...')
    write_data_START = datetime.now()
    ### work ###
    compressed_with_header.write(compressed_content)
    ############
    write_data_END = datetime.now()
    write_data_TIME = write_data_END - write_data_START
    print(str(write_data_TIME) + ' for data to write...\n')



# def main():
#
#     # full header and compressed data
#     compressed_info = get_full_header()
#     full_header = compressed_info[0]
#     compressed_content = compressed_info[1]
#
#     # header types, number of elements in each header
#     serialized_header_tools = header_compress_decompress.full_header_tools(full_header)
#     serialized_header_types = serialized_header_tools[0]
#     serialized_header_num_elements = serialized_header_tools[1]
#     serialized_header_ends = serialized_header_tools[2]
#     serialized_header_data = serialized_header_tools[3]
#
#     size_types = len(serialized_header_types)
#     bytes_size_types = size_types.to_bytes(2, byteorder='big', signed=False)
#     size_elements = len(serialized_header_num_elements)
#     bytes_size_num_elements = size_elements.to_bytes(2, byteorder='big', signed=False)
#     size_ends = len(serialized_header_ends)
#     bytes_size_ends = size_ends.to_bytes(2, byteorder='big', signed=False)
#     size_data = len(serialized_header_data)
#     bytes_size_data = size_data.to_bytes(2, byteorder='big', signed=False)
#
#     # writing data
#
#     # with open(OUT_FILE + 'kristen-' + str(BLOCK_SIZE) + '-out.tsv', 'rb') as compressed_file:
#     #     all_content = compressed_file.read()
#     # compressed_file.close()
#
#     compressed_with_header = open(OUT_FILE + 'kristen-' + str(BLOCK_SIZE) + '-out.tsv', 'wb')
#     # write how many bytes are needed to store types, ends, and data (CONSTANT FIRST 4 BYTES)
#     compressed_with_header.write(bytes_size_types)
#     compressed_with_header.write(bytes_size_num_elements)
#     compressed_with_header.write(bytes_size_ends)
#     compressed_with_header.write(bytes_size_data)
#
#     # write header types and header ends (serilized)
#     compressed_with_header.write(serialized_header_types)
#     compressed_with_header.write(serialized_header_num_elements)
#     compressed_with_header.write(serialized_header_ends)
#
#     # write header (serialized)
#     compressed_with_header.write(serialized_header_data)
#
#     # write contents of file (all compressed blocks)
#     compressed_with_header.write(compressed_content)
#
#
# def get_full_header():
#     # header_start
#     # Magic number, version number, delimiter, column labels, column types, number columns, gzip header
#     # [1,
#     # 1,
#     # '\t',
#     # ['chr', 'pos', 'ref', 'alt', 'af_cases_EUR', 'af_controls_EUR', 'beta_EUR', 'se_EUR', 'pval_EUR', 'low_confidence_EUR'],
#     # [1, 1, 3, 3, 2, 2, 2, 2, 2, 3],
#     # 10,
#     # b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff']
#     print('generating start of header...')
#     header_start_START = datetime.now()
#     ###work###
#     header_start = generate_header_first_half.get_header_data(IN_FILE, DATA_TYPE_CODE_BOOK)
#     ##########
#     header_start_END = datetime.now()
#     header_start_TIME = header_start_END-header_start_START
#     print(str(header_start_TIME) + ' for header start to compute...\n')
#
#     magic_number = header_start[0]
#     version = header_start[1]
#     delimiter = header_start[2]
#     column_labels = header_start[3]
#     column_types = header_start[4]
#     number_columns = header_start[5]
#     gzip_header = header_start[6]
#
#     # funnel format
#     # list of blocks [[block1][block2]...[blockn]]
#     # --> a block is a list of columns: block1 = [[col1], [co2]...[colm]]
#     # -----> a column is a list of string values: col1 = ['1','1','1','1','1']
#     print('generating funnel format...')
#     funnel_format_START = datetime.now()
#     ###work###
#     funnel_format_data = funnel_format.make_all_blocks(IN_FILE, BLOCK_SIZE, number_columns, delimiter)
#     ##########
#     funnel_format_END = datetime.now()
#     funnel_format_TIME = funnel_format_END - funnel_format_START
#     print(str(funnel_format_TIME) + ' for funnel format to compute...\n')
#
#     print('compressing data...')
#     header_end_START = datetime.now()
#     ###work###
#     serialize_compress_data = serialize_and_compress_funnel_format(COMPRESSION_METHOD_CODE_BOOK['gzip'], funnel_format_data, column_types)
#     header_end = serialize_compress_data[0]
#     all_compressed_content = serialize_compress_data[1]
#     ##########
#     header_end_END = datetime.now()
#     header_end_TIME = header_end_END - header_end_START
#     print(str(header_end_TIME) + ' for full compression to complete...\n')
#
#     full_header = header_start+header_end
#
#     print('FULL HEADER:')
#     print(full_header)
#
#     return full_header, all_compressed_content
#
#
# def serialize_and_compress_funnel_format(compression_method, ff, column_types):
#     full_header_end = [[] for i in range(3)] # last half of header
#     compressed_content = b''
#
#     block_end = 0
#     # go through data, and compress each column
#     for block_i in range(len(ff)):
#         # start timer for block
#         print('block ' + str(block_i))
#         block_i_START = datetime.now()
#
#         # current block from funnel format
#         curr_block = ff[block_i]
#
#         # returns full_header_end and final compressed block
#         block_compression_info = block_compression.compress_block(compression_method,
#             column_types, full_header_end, block_end, curr_block)
#
#         full_header_end = block_compression_info[0]
#         compressed_block = block_compression_info[1]
#         compressed_content += compressed_block
#
#         block_end = full_header_end[1][-1]
#
#         block_i_END = datetime.now()
#         block_i_TIME = block_i_END - block_i_START
#         print(str(block_i_TIME) + ' for block ' + str(block_i) + ' to compress...\n')
#
#     block_sizes = full_header_end[2]
#     num_rows_last_block = len(ff[-1][0])
#     if len(block_sizes) < 2: block_sizes.append(num_rows_last_block)
#
#     return full_header_end, compressed_content

if __name__ == '__main__':
    new_main()
