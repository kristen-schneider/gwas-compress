#### IMPORTS ####
# python imports
from datetime import datetime

# kristen imports
import config_arguments
import generate_header_first_half
import generate_funnel_format
import funnel_format_compress
import funnel_format_compress_ints
import header_compress

#### CONSTANTS ####
# code book for easier type identification
DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes:4}
AVAILABLE_COMPRESSION_METHODS = ['gzip', 'zlib', 'bz2', 'fastpfor128', 'fastpfor256']

#### USER-SPECIFIED PARAMETERS ####
# user should edit config.ini to reflect proper parameters
args = config_arguments.get_args_from_config('MENDEL')

# included in config file
IN_FILE = args['in_file']
OUT_DIR = args['out_dir']
BLOCK_SIZE = int(args['block_size'])
COMPRESSION_METHOD = list(args['compression_method'].split(','))
DATA_TYPE_BYTE_SIZES = {1:int(args['int_byte_size']),
                        2:int(args['float_byte_size']),
                        3:int(args['string_byte_size']),
                        4:args['bytes_byte_size']}
# output file made from combining user specified params
base_name_in_file = IN_FILE.split('/')[-1].split('.')[0]
COMPRESSED_FILE = OUT_DIR + 'kristen-' + base_name_in_file + '-blocksize-' + str(BLOCK_SIZE) + '.tsv'
COMPRESSION_TIMES_FILE = OUT_DIR + 'times-' + str(BLOCK_SIZE) + '.csv'


def main():
    """
    1. gets beginning of header (magic number, version, delimiter, column labels, column types, num columns, gzip header)
    2. generates funnel format (list of blocks)
    3. compress data and get second half of header
    4. compress full header
    5. write compressed header
    6. write compressed data
    """
    # 1. GET FIRST HALF OF HEADER
    ### Magic number, version number, delimiter, column labels, column types, number columns, gzip header
    print('generating start of header...')
    header_first_half_START = datetime.now()
    ### work ###
    header_first_half = generate_header_first_half.get_header_first_half(IN_FILE, DATA_TYPE_CODE_BOOK)
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


    # 2. GET FUNNEL FORMAT
    ### list of blocks [[block1][block2]...[blockn]]
    ### --> a block is a list of columns: block1 = [[col1], [co2]...[colm]]
    ### -----> a column is a list of string values: col1 = ['1','1','1','1','1']
    print('generating funnel format...')
    funnel_format_START = datetime.now()
    ### work ###
    funnel_format_data = generate_funnel_format.make_all_blocks(IN_FILE, BLOCK_SIZE, number_columns, delimiter)
    ############
    funnel_format_END = datetime.now()
    funnel_format_TIME = funnel_format_END - funnel_format_START
    print(str(funnel_format_TIME) + ' for funnel format to compute...\n')

    # 3. COMPRESS DATA, GET SECOND HALF OF HEADER
    print('compressing data...')
    compress_data_START = datetime.now()
    ### work ###
    # serialized_compressed_data = funnel_format_compress.compress_all_blocks(DATA_TYPE_CODE_BOOK, DATA_TYPE_BYTE_SIZES,
    #                                                                         AVAILABLE_COMPRESSION_METHODS,
    #                                                                         COMPRESSION_METHOD, header_first_half,
    #                                                                         funnel_format_data, OUT_DIR)
    # header_second_half = serialized_compressed_data[0]
    # compressed_data = serialized_compressed_data[1]

    serialized_compressed_data_all_ints = funnel_format_compress_ints.compress_all_blocks(AVAILABLE_COMPRESSION_METHODS,
                                                                                          COMPRESSION_METHOD,
                                                                                          header_first_half,
                                                                                          funnel_format_data,
                                                                                          OUT_DIR)

    try:
        header_second_half = serialized_compressed_data_all_ints[0]
    except:
        print('could not compress data')
        return -1
    #try:
    #    compressed_data = serialized_compressed_data_all_ints[1]
    #except:
    #    print('could not compress data')
    #    return -1


    ############
    compress_data_END = datetime.now()
    compress_data_TIME = compress_data_END - compress_data_START
    print(str(compress_data_TIME) + ' for full compression to complete...\n')

    # 4. COMPRESS HEADER
    print('compressing header...')
    compress_header_START = datetime.now()
    ### work ###
    full_header = header_first_half+header_second_half
    #print(full_header)
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
    compress_header_END = datetime.now()
    compress_header_TIME = compress_header_END - compress_header_START
    print(str(compress_header_TIME) + ' for header to compress...\n')

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
    f.write(data)
    f.close()

    # ######################################################
    # ## OLD WRITE METHOD WHERE EVERYTHING WRITTEN AT END ##
    # ######################################################
    #
    # # 5. WRITE COMPRESSED HEADER
    # print('writing header...')
    # write_header_START = datetime.now()
    # ### work ###
    # compressed_with_header = open(COMPRESSED_FILE, 'wb')
    # # write how many bytes are needed to store types, ends, and data (CONSTANT FIRST 4 BYTES)
    # compressed_with_header.write(bytes_size_types)
    # compressed_with_header.write(bytes_size_num_elements)
    # compressed_with_header.write(bytes_size_ends)
    # compressed_with_header.write(bytes_size_data)
    #
    # # write header types and header ends (serialized)
    # compressed_with_header.write(serialized_header_types)
    # compressed_with_header.write(serialized_header_num_elements)
    # compressed_with_header.write(serialized_header_ends)
    #
    # # write header (serialized)
    # compressed_with_header.write(serialized_header_data)
    # ############
    # write_header_END = datetime.now()
    # write_header_TIME = write_header_END - write_header_START
    # print(str(write_header_TIME) + ' for header to write...\n')
    #
    # # 6. WRITE COMPRESSED DATA
    # print('writing data...')
    # write_data_START = datetime.now()
    # ### work ###
    # compressed_with_header.write(compressed_data)
    # ############
    # write_data_END = datetime.now()
    # write_data_TIME = write_data_END - write_data_START
    # print(str(write_data_TIME) + ' for data to write...\n')

if __name__ == '__main__':
    main()
