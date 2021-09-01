def find_blocks(block_size, decompression_start, decompresssion_end):
    blocks = []
    start_block = decompression_start/block_size
    end_block = decompression_end/block_size
    blocks = [start_block, end_block]
    return blocks
