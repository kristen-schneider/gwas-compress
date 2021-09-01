import math


def find_blocks(block_size, decompression_start, decompression_end):
    blocks = []
    start_block = math.floor(decompression_start/block_size)
    end_block = math.floor(decompression_end/block_size)
    if decompression_start > decompression_end:
        print('start block is bigger than end block. please re-enter query')
        return [-1,-1]
    else: blocks = [start_block, end_block]
    return blocks
