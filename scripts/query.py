import config_arguments
import sys
from datetime import datetime
import header_decompress
import query_decompress

# CONSTANTS
DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes:4}
# DATA_TYPE_BYTE_SIZES = {1: 5, 2: 8, 3: 5, 4:None}
COMPRESSION_METHOD_CODE_BOOK = {'gzip':1, 'zlib':2, 'bz2':3}

# USER-SPECIFIED PARAMETERS
args = config_arguments.get_args_from_config('LOCAL')
# included in config file
IN_FILE = args['in_file']
OUT_DIR = args['out_dir']
BLOCK_SIZE = int(args['block_size'])
COMPRESSION_METHOD = list(args['compression_method'].split(','))
BLOCK_TO_DECOMPRESS = int(args['block_to_decompress'])
COLUMN_TO_DECOMPRESS = int(args['column_to_decompress'])
DATA_TYPE_BYTE_SIZES = {1:int(args['int_byte_size']),
                        2:int(args['float_byte_size']),
                        3:int(args['string_byte_size']),
                        4:args['bytes_byte_size']}

# output file made from combining user specified params
base_name_in_file = IN_FILE.split('/')[-1].split('.')[0]
OUT_FILE = OUT_DIR + 'kristen-' + base_name_in_file + '-blocksize-' + str(BLOCK_SIZE) + '.tsv'


# COMPRESSED_FILE = OUT_DIR + 'kristen-' + str(COMPRESSION_METHOD[0]) + '-' + str(BLOCK_SIZE) + '.tsv'
# DATA_FILE = OUT_DIR + 'plot-' + str(COMPRESSION_METHOD[0]) + '-' + str(BLOCK_SIZE) + '.csv'

# PARAMETERS
# OUT_DIR = sys.argv[1]
# BLOCK_SIZE = int(sys.argv[2])
# COMPRESSION_METHOD = sys.argv[3]
# BLOCK_TO_DECOMPRESS = int(sys.argv[4])
# COLUMN_TO_DECOMPRESS = int(sys.argv[5])
# OUT_FILE = OUT_DIR + 'kristen-' + str(COMPRESSION_METHOD) + '-' + str(BLOCK_SIZE) + '.tsv'
#
# DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes:4}
# DATA_TYPE_BYTE_SIZES = {1: 5, 2: 8, 3: 5, 4:None}
# COMPRESSION_METHOD_CODE_BOOK = {'gzip':1, 'zlib':2, 'bz2':3}

def main():

    full_header_info = header_decompress.get_full_header(DATA_TYPE_BYTE_SIZES, OUT_FILE)
    full_header_bytes = full_header_info[0]
    full_header = full_header_info[1]
    print(full_header)

    print('getting compressed block...')
    compressed_block_START = datetime.now()
    ### work ###
    compressed_block_info = query_decompress.query_block(COMPRESSION_METHOD_CODE_BOOK, BLOCK_TO_DECOMPRESS,
                                                         full_header, full_header_bytes,
                                                         DATA_TYPE_BYTE_SIZES, OUT_FILE)
    print(compressed_block_info)
    ############
    compressed_block_END = datetime.now()
    compressed_block_TIME = compressed_block_END - compressed_block_START
    print(str(compressed_block_TIME) + ' for grabbing a single block to decompress...\n')

    print('decompressing single block...')
    single_block_START = datetime.now()
    ### work ###
    dc_single_block = query_decompress.decompress_single_block(
        COMPRESSION_METHOD_CODE_BOOK, COMPRESSION_METHOD,
        compressed_block_info, full_header, DATA_TYPE_BYTE_SIZES)
    ############
    print(dc_single_block)
    single_block_END = datetime.now()
    single_block_TIME = single_block_END - single_block_START
    print(str(single_block_TIME) + ' for decompressing single block to compute...\n')

    print('decompressing single column...')
    single_column_START = datetime.now()
    ### work ###
    dc_single_column = query_decompress.decompress_single_column(
        COMPRESSION_METHOD_CODE_BOOK, COMPRESSION_METHOD,
        compressed_block_info, COLUMN_TO_DECOMPRESS, full_header, DATA_TYPE_BYTE_SIZES)
    ############
    print(dc_single_column)
    single_column_END = datetime.now()
    single_column_TIME = single_column_END - single_column_START
    print(str(single_column_TIME) + ' for decompressing single column to compute...\n')

if __name__ == "__main__":
    main()
