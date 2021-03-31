import multiprocessing
from multiprocessing.pool import Pool
import type_handling
import serialize
import compress

# 4. bytes for each data type
DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes:4}
DATA_TYPE_BYTE_SIZES = {1: 5, 2: 8, 3: 5, 4:None}

#EXAMPLE
def main():
    arr_inputs=[1,2,3]

    with Pool(3) as p:
        arr_outputs = p.map(add_to_five, arr_inputs)

    print(arr_outputs)

def compress_in_parallel(column_types, header_end, block_header_end, block_end, block):
    compressed_block_header = b''
    compressed_block = b''
    compressed_block_final = b''

    HEADER_block_header_ends = header_end[0]
    HEADER_block_ends = header_end[1]
    HEADER_block_num_rows = header_end[2]

    num_cols_in_block = len(block)
    num_rows_in_block = len(block[0])
    # this should only be triggered for first block and last block.
    if num_rows_in_block not in HEADER_block_num_rows:
        HEADER_block_num_rows.append(num_rows_in_block)

    # COLUMN COMPRESSION AND BLOCK HEADER INFO
    block_col_ends = []
    curr_compressed_col_end = 0
    for column_i in range(len(block)):

        # get column info
        curr_column = block[column_i]
        column_type = column_types[column_i]
        typed_column = type_handling.convert_to_type(curr_column, column_type)
        column_bytes = DATA_TYPE_BYTE_SIZES[column_type]

        # serialize and compress a column
        s_column = serialize.serialize_list(typed_column, column_type, column_bytes)
        s_c_column = compress.compress_data(s_column, 0)[10:]  # remove the gzip header bit from the compressed data
        compressed_block += s_c_column

        # add length of this column to lengths of columns in this block
        curr_compressed_col_end += len(s_c_column)
        block_col_ends.append(curr_compressed_col_end)

    # write the compressed block header and compressed block to the file
    s_block_header = serialize.serialize_list(block_col_ends, DATA_TYPE_CODE_BOOK[type(block_col_ends[0])], DATA_TYPE_BYTE_SIZES[1])
    compressed_block_header = compress.compress_data(s_block_header, 0)[10:]

    block_header_length = len(compressed_block_header)
    block_header_end = (block_header_length + block_end)
    HEADER_block_header_ends.append(block_header_end)

    block_length = len(compressed_block)

    block_end += (block_header_length + block_length)
    HEADER_block_ends.append(block_end)

    compressed_block_final += compressed_block_header
    compressed_block_final += compressed_block

    header_end = [HEADER_block_header_ends, HEADER_block_ends, HEADER_block_num_rows]

    return header_end, compressed_block_final



def add_to_five(x):
      return x+5

if __name__ == '__main__':
    main()



