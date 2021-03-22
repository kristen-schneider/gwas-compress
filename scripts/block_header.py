import type_handling
import deserialize

def get_block_header(s_block, block_size, column_types, type_to_bytes_code_book):
    '''
    returns the end positions of each column in a block
    '''
    col_end_positions = []
    start = 0
    for t in column_types:
        col_s_bitstring_length = \
            type_handling.get_bitstring_length_by_data_type(block_size, t, type_to_bytes_code_book[t])
        end = start+col_s_bitstring_length
        col_end_positions.append(end)
        start = start + col_s_bitstring_length

    return col_end_positions

def deserialize_one_column(s_block, block_header, column_i, block_size, data_type, num_bytes):

    if column_i != 0: start = block_header[column_i-1]
    else: start = 0

    end = block_header[column_i]



    s_column = s_block[start:end]
    ds_column = deserialize.deserialize_data(s_column, block_size, data_type, num_bytes)
    return ds_column






