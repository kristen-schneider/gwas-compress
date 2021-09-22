#### IMPORTS ####
# python_scripts imports
from datetime import datetime
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# kristen imports
from utils import config_arguments
#from utils import type_handling
import header_decompress
import decompression_worker
import search
import decompress_block

# 0. GET ARGUMENTS

# CONSTANTS
#DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes:4}

# USER-SPECIFIED PARAMETERS
# user should edit config.ini to reflect proper parameters
# args = config_arguments.get_args_from_config('LOCAL')
COMPRESSED_FILE = sys.argv[1]#'/home/krsc0813/projects/gwas-compress/scripts/testing_write_all.txt'
config_file = sys.argv[2]#'/home/krsc0813/projects/gwas-compress/config_files/config.ini'
args = config_arguments.get_args_from_config('MENDEL', config_file)
# included in config file
IN_FILE = args['in_file']
OUT_DIR = args['out_dir']
BLOCK_SIZE = int(args['block_size'])
CODECS_LIST = list(args['compression_method'].split(','))
COMPRESSION_DATA_TYPES=list(args['input_data_type'].split(','))
DECOMPRESSION_START = int(args['decompression_start'])
DECOMPRESSION_END = int(args['decompression_end'])
DATA_TYPE_BYTE_SIZES = {1:int(args['int_byte_size']),
                        2:int(args['float_byte_size']),
                        3:int(args['string_byte_size']),
                        4:args['bytes_byte_size']}

# output file made from combining user specified params
basename_compressed_file = IN_FILE.split('/')[-1].split('.')[0]
#COMPRESSED_FILE = OUT_DIR + 'kristen-' + basename_compressed_file + '-' + str(BLOCK_SIZE) + '.tsv'
# COMPRESSED_FILE = '/Users/kristen/PycharmProjects/gwas-compress/scripts/testing_write_all.txt'

# COMPRESSED_FILE = OUT_DIR + 'kristen-' + str(COMPRESSION_METHOD[0]) + '-' + str(BLOCK_SIZE) + '.tsv'
# DATA_FILE = OUT_DIR + 'plot-' + str(COMPRESSION_METHOD[0]) + '-' + str(BLOCK_SIZE) + '.csv'

def main():

    # 1. GETTING FULL HEADER
    print('getting full header...')
    full_header_info = header_decompress.get_full_header(DATA_TYPE_BYTE_SIZES, COMPRESSED_FILE)
    full_header_bytes = full_header_info[0]
    full_header = full_header_info[1]
    #print(full_header)
    
    # 2. RETRIVEING BLOCKS TO DECOMPRESS
    query_blocks = search.find_blocks(BLOCK_SIZE, DECOMPRESSION_START, DECOMPRESSION_END)
    print('from row ', DECOMPRESSION_START, ' to row ', DECOMPRESSION_END,
            '...decompression blocks ', query_blocks[0], 'to', query_blocks[1])
    num_blocks_to_decompress = query_blocks[1]-query_blocks[0]+1
    start_end_index = search.block_row_mapping(query_blocks, BLOCK_SIZE, DECOMPRESSION_START, DECOMPRESSION_END)
    #block_decomp_index = search.make_block_start_end_list(num_blocks_to_decompress, BLOCK_SIZE, start_end_index[0], start_end_index[1])

    for b in range(num_blocks_to_decompress):
        # 2. RETRIEVING COMPRESSED ROWS DECOMPRESSION_START to DECOMPRESSION_END
        print('getting compressed block...', b)

        compressed_block_START = datetime.now()
        ### work ###
        cbi = decompress_block.get_compressed_block_data(b, full_header,
                            full_header_bytes, DATA_TYPE_BYTE_SIZES, COMPRESSED_FILE, COMPRESSION_DATA_TYPES)
        #############
        compressed_block_END = datetime.now()
        compressed_block_TIME = compressed_block_END - compressed_block_START
        print(str(compressed_block_TIME) + ' for grabbing a single block to decompress...\n')
    
        # # 3. DECOMPRESSING SINGLE BLOCK
        # print('decompressing single block...')
        # single_block_START = datetime.now()
        # ### work ###
        dc_block_header = cbi[0]
        compressed_block = cbi[1]
        block_row_count = cbi[2]
    
        decompressed_block = decompress_block.decompress_single_block(dc_block_header, compressed_block, COMPRESSION_DATA_TYPES, full_header[4], block_row_count, DATA_TYPE_BYTE_SIZES, CODECS_LIST)
    
        # 4. RETRIEVE NECESSARY ROWS FROM FULL BLOCK
    
        # if there is only one block, we already have start and end indices
        if num_blocks_to_decompress == 1:
            block_start_index = start_end_index[0]
            block_end_index = start_end_index[1]
        # if there is more than one block, we need to find the start and end indices for each block
        else:
            if b == 0: # first block is query_start to end of block
                block_start_index = start_end_index[0]
                block_end_index = BLOCK_SIZE-1
            elif b == num_blocks_to_decompress-1: # last block is 0 to query_end
                block_start_index = 0
                block_end_index = start_end_index[1]
            else: # want all rows from middle blocks 0 to end of block
                block_start_index = 0
                block_end_index = BLOCK_SIZE-1
                        

        reduced_columns = search.find_rows(decompressed_block, block_start_index, block_end_index)
        
        # for packed strings
        num_rows_to_decomp = len(reduced_columns[0])
        for c in range(len(reduced_columns)):
            for l in range(len(reduced_columns[c])):
                if type(reduced_columns[c][l]) == list:
                    reduced_columns[c][l] = reduced_columns[c][l][0:num_rows_to_decomp]
                

        reduced_rows = search.make_into_rows(reduced_columns)
        print(reduced_columns)
        print(list(reduced_rows))
        for r in list(reduced_rows): print(r)
        #for r in reduced_rows: print(r)
    # if 'int' in COMPRESSION_STYLE:
    #     dc_single_block = decompression_worker.decompress_single_block_int(CODECS_LIST, compressed_block_info,
    #                                                                        full_header, DATA_TYPE_BYTE_SIZES)
    # elif 'all' in COMPRESSION_STYLE:
    #     print('all data types')
    # ############
    # for dc in dc_single_block: print(dc)
    # single_block_END = datetime.now()
    # single_block_TIME = single_block_END - single_block_START
    # print(str(single_block_TIME) + ' for decompressing single block to compute...\n')
    #
    # print('decompressing single column...')
    # single_column_START = datetime.now()
    # ### work ###
    # dc_single_column = decompression_worker.decompress_single_column_int(CODECS_LIST[COLUMN_TO_DECOMPRESS],
    #                                                                      compressed_block_info, COLUMN_TO_DECOMPRESS,
    #                                                                      full_header, DATA_TYPE_BYTE_SIZES)
    # ############
    # print(dc_single_column)
    # single_column_END = datetime.now()
    # single_column_TIME = single_column_END - single_column_START
    # print(str(single_column_TIME) + ' for decompressing single column to compute...\n')

if __name__ == "__main__":
    main()
