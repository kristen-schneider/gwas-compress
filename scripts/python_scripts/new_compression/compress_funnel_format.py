# python_scripts imports
from datetime import datetime
import numpy as np
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

# personal imports
from utils import type_handling
import compress_block


def compress_all_blocks(CODECS_LIST, COMPRESSION_DATA_TYPES, DATA_TYPE_BYTE_SIZES,
                        header_first_half, funnel_format_data, config_file_name):
    """
    returns end of header: [end of block headers, end of blocks, sizes of blocks]

    INPUT
        CODECS_LIST: list of compression methods to use on columns
        COMPRESSION_DATA_TYPES: list of data types to convert each column
        DATA_TYPE_BYTE_SIZES: byte sizes for each data type
        header_first_half: first half of header
        funnel_format_data: funnel format data (all data is in strings)

    OUTPUT
        compresses data and returns second half of header
    """

    # full header break down
    magic_number = header_first_half[0]
    version = header_first_half[1]
    delimiter = header_first_half[2]
    column_labels = header_first_half[3]
    decompression_data_types = header_first_half[4]
    number_columns = header_first_half[5]

    # ends of block headers
    block_header_ends = []

    # ends of blocks
    block_ends = []

    block_sizes = []
    # go through funnel format, and compress each block

    all_compressed_data = b''

    for block_i in range(len(funnel_format_data)):

        # current block from funnel format
        curr_block = funnel_format_data[block_i]

        # compress block
        block_header_and_block_data = compress_block.compress_block(curr_block,
                                                              CODECS_LIST,
                                                              COMPRESSION_DATA_TYPES,
                                                              decompression_data_types,
                                                              DATA_TYPE_BYTE_SIZES,
                                                              config_file_name)
        # return block_header_and_data

        compressed_block_header = block_header_and_block_data[0]
        compressed_block = block_header_and_block_data[1]
        all_compressed_data+=compressed_block_header
        all_compressed_data+=compressed_block
        # HEADER END DATA
        # add to block header ends
        try:
            block_header_end = (block_ends[block_i-1]+len(compressed_block_header))
        except IndexError:
            block_header_end = (0+len(compressed_block_header))
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

    if len(block_sizes) < 2:
        #block_sizes.append(curr_block_size)
        block_sizes.append(0)

    header_second_half = [block_header_ends, block_ends, block_sizes]
    return all_compressed_data,header_second_half
