import sys
from datetime import datetime
import header_decompress
import query_decompress

# PARAMETERS
COMPRESSED_FILE = sys.argv[1]
BLOCK_SIZE = int(sys.argv[2])
COMPRESSION_METHOD = sys.argv[3]

DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes:4}
DATA_TYPE_BYTE_SIZES = {1: 5, 2: 8, 3: 5, 4:None}
COMPRESSION_METHOD_CODE_BOOK = {'gzip':1, 'zlib':2}

BLOCK_TO_DECOMPRESS = 2#int(input("Enter block to decompress: "))
COLUMN_TO_DECOMPRESS = 1#int(input("Enter column to decompress: "))

# COMPRESSED_FILE
#COMPRESSED_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/'
#FIJI: '/scratch/Users/krsc0813/gwas-compress/data/compressed/'
# BLOCK SIZE
#BLOCK_SIZE = 3
#FIJI
# BLOCK_SIZE = int(sys.argv[1])

def main():

    full_header_info = header_decompress.get_full_header(DATA_TYPE_BYTE_SIZES, COMPRESSED_FILE, BLOCK_SIZE)
    full_header_bytes = full_header_info[0]
    full_header = full_header_info[1]

    print('getting compressed block...')
    compressed_block_START = datetime.now()
    ### work ###
    compressed_block_info = query_decompress.query_block(COMPRESSION_METHOD_CODE_BOOK, COMPRESSION_METHOD, COMPRESSED_FILE, BLOCK_TO_DECOMPRESS, full_header, full_header_bytes, BLOCK_SIZE, DATA_TYPE_BYTE_SIZES)
    ############
    compressed_bloc_END = datetime.now()
    compressed_bloc_TIME = compressed_bloc_END - compressed_block_START
    print(str(compressed_bloc_TIME) + ' for grabbing a single block to decompress...\n')

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
