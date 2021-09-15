import math

def find_blocks(block_size, decompression_start, decompression_end):
    """
    searches for the blocks that need to be decompressed

    INPUT:
        block_size: number of rows in block
        decompression_start: starting row which user queries
        decompression_end: ending row which user queries
    OUTPUT:
        blocks: list of block indexes which need to be decompressed
    """
    blocks = []
    start_block = math.floor(decompression_start/block_size)
    end_block = math.floor(decompression_end/block_size)
    if decompression_start > decompression_end:
        print('start block is bigger than end block. please choose different query.')
        return [-1,-1]
    else: blocks = [start_block, end_block]
    return blocks

def block_row_mapping(blocks, block_size, decompression_start, decompression_end):
    """
    returns a list of starting and ending positions for each block
    
    INPUT:
        
    OUTPUT:
        row_maps: list of start place for first block and end place positions 
    """
    row_maps = []
    
    start = None
    end = None
    
    block_start_index = blocks[0]
    start = decompression_start - (block_size * blocks_start_index)
    end = decompression_end - (block_size * blocks_start_index)
    
    return [start, end] 

def find_rows(decompressed_block, block_row_start, block_row_end):
    """
    reduces columns to just the necessary rows
    INPUT:
        decompressed block: all rows in block
        block_row_start: starting point for rows in this block
        block_row_end: ending point for rows in this block
    OUTPUT:
        reduced_columns: only rows which were queried
    """
    reduced_columns = []
    
    for column in decompressed_block:
        reduced_columns.append(column[block_row_start:block_row_end])
    
    return reduced_columns

def make_into_rows(reduced_columns):
    """
    takes reduced columns and makes them back into rows

    INPUT:
        reduced_columns: only column data from necessary rows in block
    
    OUTPUT:
        reduced_rows: only row data from necessary rows in block
    """
    reduced_rows = map(list, zip(*reduced_columns))
    return reduced_rows


