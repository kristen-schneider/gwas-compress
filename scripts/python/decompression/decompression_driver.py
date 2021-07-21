from scripts.python.compression import config_arguments
from datetime import datetime
import header_decompress
import decompression_worker

# 0. GET ARGUMENTS

# CONSTANTS
DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes:4}

# USER-SPECIFIED PARAMETERS
# user should edit config.ini to reflect proper parameters
# args = config_arguments.get_args_from_config('LOCAL')
args = config_arguments.get_args_from_config('MENDEL')
# included in config file
IN_FILE = args['in_file']
OUT_DIR = args['out_dir']
BLOCK_SIZE = int(args['block_size'])
COMPRESSION_STYLE = args['compression_style']
CODECS_LIST = list(args['compression_method'].split(','))
BLOCK_TO_DECOMPRESS = int(args['block_to_decompress'])
COLUMN_TO_DECOMPRESS = int(args['column_to_decompress'])
DATA_TYPE_BYTE_SIZES = {1:int(args['int_byte_size']),
                        2:int(args['float_byte_size']),
                        3:int(args['string_byte_size']),
                        4:args['bytes_byte_size']}

# output file made from combining user specified params
base_name_in_file = IN_FILE.split('/')[-1].split('.')[0]
OUT_FILE = OUT_DIR + 'kristen-' + base_name_in_file + '-blocksize-' + str(BLOCK_SIZE) + '.tsv'
# OUT_FILE = '/Users/kristen/PycharmProjects/gwas-compress/scripts/testing_write_all.txt'
OUT_FILE = '/home/krsc0813/projects/gwas-compress/scripts/testing_write_all.txt'

# COMPRESSED_FILE = OUT_DIR + 'kristen-' + str(COMPRESSION_METHOD[0]) + '-' + str(BLOCK_SIZE) + '.tsv'
# DATA_FILE = OUT_DIR + 'plot-' + str(COMPRESSION_METHOD[0]) + '-' + str(BLOCK_SIZE) + '.csv'

def main():

    # 1. GETTING FULL HEADER
    print('getting full header...')

    full_header_info = header_decompress.get_full_header(DATA_TYPE_BYTE_SIZES, OUT_FILE)
    full_header_bytes = full_header_info[0]
    full_header = full_header_info[1]
    #print(full_header)

    # 2. RETRIEVING COMPRESSED BLOCK AND BLOCK HEADER
    print('getting compressed block...')
    compressed_block_START = datetime.now()
    ### work ###
    compressed_block_info = decompression_worker.query_block(BLOCK_TO_DECOMPRESS,
                                                             full_header, full_header_bytes,
                                                             DATA_TYPE_BYTE_SIZES, OUT_FILE)
    ############
    compressed_block_END = datetime.now()
    compressed_block_TIME = compressed_block_END - compressed_block_START
    print(str(compressed_block_TIME) + ' for grabbing a single block to decompress...\n')

    # 3. DECOMPRESSING SINGLE BLOCK
    print('decompressing single block...')
    single_block_START = datetime.now()
    ### work ###
    if 'int' in COMPRESSION_STYLE:
        dc_single_block = decompression_worker.decompress_single_block_int(CODECS_LIST, compressed_block_info,
                                                                           full_header, DATA_TYPE_BYTE_SIZES)
    elif 'all' in COMPRESSION_STYLE:
        print('all data types')
    ############
    for dc in dc_single_block: print(dc)
    single_block_END = datetime.now()
    single_block_TIME = single_block_END - single_block_START
    print(str(single_block_TIME) + ' for decompressing single block to compute...\n')

    print('decompressing single column...')
    single_column_START = datetime.now()
    ### work ###
    dc_single_column = decompression_worker.decompress_single_column_int(CODECS_LIST[COLUMN_TO_DECOMPRESS],
                                                                         compressed_block_info, COLUMN_TO_DECOMPRESS,
                                                                         full_header, DATA_TYPE_BYTE_SIZES)
    ############
    print(dc_single_column)
    single_column_END = datetime.now()
    single_column_TIME = single_column_END - single_column_START
    print(str(single_column_TIME) + ' for decompressing single column to compute...\n')

if __name__ == "__main__":
    main()
