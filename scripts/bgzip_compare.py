"""
bgzip compare is meant to provide a baseline for comparison with our compression and with bgzip.
block compression, which is to take a file, split into blocks, and compress each block.
"""

def parse_file(in_file, block_size):
    """
    with bgzip style compression, we parse the file into blocks and compress
    """
    # open file
    gwas_f = open(in_file, 'r')
    # close file
    gwas_f.close()

def compress_block(block):
    """
    will call a method to compression a single block
    """
    compressed_block = None
    return compressed_block