#### IMPORTS ####
# python imports
from datetime import datetime

# project imports
import config_arguments
import generate_header_first_half
import bgzip_compare
import compression_worker
import header_compress

# 0. GET ARGUMENTS

# CONSTANTS
DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes: 4}

# USER-SPECIFIED PARAMETERS
# user should edit config.ini to reflect proper parameters
args = config_arguments.get_args_from_config('LOCAL')
# args = config_arguments.get_args_from_config('MENDEL')
# included in config file
IN_FILE = args['in_file']
OUT_DIR = args['out_dir']
BLOCK_SIZE = int(args['block_size'])
COMPRESSION_STYLE = args['compression_style']
CODECS_LIST = list(args['compression_method'].split(','))
DATA_TYPE_BYTE_SIZES = {1: int(args['int_byte_size']),
                        2: int(args['float_byte_size']),
                        3: int(args['string_byte_size']),
                        4: args['bytes_byte_size']}
# output file made from combining user specified params
base_name_in_file = IN_FILE.split('/')[-1].split('.')[0]
COMPRESSED_FILE = OUT_DIR + 'kristen-' + base_name_in_file + '-blocksize-' + str(BLOCK_SIZE) + '.tsv'
COMPRESSION_TIMES_FILE = OUT_DIR + 'times-' + str(BLOCK_SIZE) + '.csv'

def main():
    # 1. GET FIRST HALF OF HEADER
    # first half of header is not dependent on compression style
    #
    # HEADER (FIRST HALF)
    # Magic number,
    # version number,
    # delimiter,
    # column labels,
    # column types,
    # number columns,
    # gzip header

    print('generating start of header...')
    start_of_header_start_time = datetime.now()

    ### work ###
    start_of_header = generate_header_first_half.get_header_first_half(IN_FILE, DATA_TYPE_CODE_BOOK)
    ############

    start_of_header_end_time = datetime.now()
    start_of_header_full_time = start_of_header_end_time - start_of_header_start_time
    # print(start_of_header)
    print(str(start_of_header_full_time) + ' for start of header to compute...\n')

    magic_number = start_of_header[0]
    version = start_of_header[1]
    delimiter = start_of_header[2]
    column_labels = start_of_header[3]
    column_data_types = start_of_header[4]
    num_columns = start_of_header[5]
    gzip_header = start_of_header[6]
    bz2_header = start_of_header[7]

    # 2. COMPRESS DATA
    # compresses data
    # writes compressed block header and compressed block after each block
    # returns end of header
    print('compressing data...')
    file_compression_start_time = datetime.now()
    ### work ###
    end_of_header = compression_worker.block_compression(COMPRESSION_STYLE, IN_FILE, BLOCK_SIZE,
                                                         delimiter, num_columns, column_data_types,
                                                         CODECS_LIST, DATA_TYPE_BYTE_SIZES, COMPRESSED_FILE)
    ############
    # print(end_of_header)
    print(datetime.now()-file_compression_start_time, ' for start of full compression to complete...\n')


    # 3. COMPRESS HEADER
    print('compressing header...')
    compress_header_start_time = datetime.now()
    ### work ###
    full_header = start_of_header + end_of_header
    print(full_header)
    # header types, number of elements in each header
    serialized_header_tools = header_compress.full_header_tools(DATA_TYPE_CODE_BOOK,
                                                                DATA_TYPE_BYTE_SIZES,
                                                                full_header)
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
    print(datetime.now() - compress_header_start_time, ' for header to compress...\n')


    # 4. WRITING HEADER
    f_data = open('./testing_write.txt', 'rb')
    data = f_data.read()
    f_data.close()

    f = open('./testing_write_all.txt', 'ab')
    f.truncate(0)
    f.write(bytes_size_types)
    f.write(bytes_size_num_elements)
    f.write(bytes_size_ends)
    f.write(bytes_size_data)
    f.write(serialized_header_types)
    f.write(serialized_header_num_elements)
    f.write(serialized_header_ends)
    f.write(serialized_header_data)

    # 5. READING DATA AND REWRITING DATA BENEATH HEADER
    f.write(data)
    f.close()

    # 6. COPY WRITTEN DATA AND WRITE HEADER THEN DATA


if __name__ == '__main__':
    main()
