"""
bgzip compare is meant to provide a baseline for comparison with our compression and with bgzip.
block compression, which is to take a file, split into blocks, and compress each block.
"""

def parse_file(in_file, block_size):
