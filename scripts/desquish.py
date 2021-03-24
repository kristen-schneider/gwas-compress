# imports
import squish
import decompress
import deserialize

# PARATMETERS
# 1. output file
COMPRESSED_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/'
# 2. block size
BLOCK_SIZE = 5
# 3. bytes for each data type
DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3}
DATA_TYPE_BYTE_SIZES = {1: 5, 2: 8, 3: 5}


# HEADER SHOULD BE WRITTEN IN FILE EVENTUALLY
full_header = [1, 1, '\t',
               ['chr', 'pos', 'ref', 'alt', 'af_cases_EUR', 'af_controls_EUR', 'beta_EUR', 'se_EUR', 'pval_EUR', 'low_confidence_EUR'],
               [1, 1, 3, 3, 2, 2, 2, 2, 2, 3],
               10, b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff',
               [37, 44], [306, 574], [10]]


def main():
    block_number = 0
    column_number = 0

    read_compressed_file(COMPRESSED_FILE, full_header, block_number, column_number)

def read_compressed_file(compressed_file, full_header, block_number, column_number):
    ds_full_data = []

    magic_number = full_header[0]
    version = full_header[1]
    delimeter = full_header[2]
    col_names = full_header[3]
    col_types = full_header[4]
    num_columns = full_header[5]
    end_positions = full_header[6]
    block_header_lengths = full_header[7]
    block_sizes = full_header[8]

    with open(compressed_file, 'rb') as r_file:
        all_compressed_data = r_file.read()
    r_file.close()

    num_blocks = len(end_positions)
    for block_i in range(num_blocks):

        # getting proper number of rows (last block is weird)
        if block_i < len(end_positions) - 1:
            curr_block_size = block_sizes[0]
        else:
            curr_block_size = block_sizes[1]


        curr_block_column_lengths = all_compressed_data[curr_start:block_header_lengths[block_i]]
        # dc_curr_block_column_lengths = decompress.decompress_data(curr_block_column_lengths)
        # ds_curr_block_columns_lengths = deserialize.deserialize_data(
        #     dc_curr_block_column_lengths, num_columns, 1, BYTE_SIZES[1])
        # print(curr_block_column_lengths)
        #
        # curr_start += block_header_lengths[block_i]
        # curr_end = end_positions[block_i]
        #
        # curr_bitstring = compressed_data[curr_start:curr_end]
        # dc_bitstring = decompress.decompress_data(curr_bitstring)
        # ds_bitstring = deserialize.deserialize_block(dc_bitstring, curr_block_size, col_types, BYTE_SIZES,
        #                                              curr_block_column_lengths)
        # curr_start = curr_end
        #
        # ds_full_data.append(ds_bitstring)
    return ds_full_data
