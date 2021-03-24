import decompress
import deserialize

# 1. output file
COMPRESSED_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/'
# 2. bytes for each data type
DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3}
DATA_TYPE_BYTE_SIZES = {1: 5, 2: 8, 3: 5}

full_header = \
    [1, 1, '\t', ['chr', 'pos', 'ref', 'alt', 'af_cases_EUR', 'af_controls_EUR', 'beta_EUR', 'se_EUR', 'pval_EUR',
                  'low_confidence_EUR'], [1, 1, 3, 3, 2, 2, 2, 2, 2, 3], 10,
     b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff', [29, 26, 33], [292, 528, 782], [3, 3]]


def main():
    num_rows_in_block = int(input("Enter number of rows to be in each block: "))
    block_to_decompress = int(input("Enter block to decompress: "))

    query_block(COMPRESSED_FILE, block_to_decompress, num_rows_in_block)

def query_block(compressed_file, query_block_i, num_rows_in_block):

    # get full header somehow. later.

    with open(compressed_file+'kristen-'+str(num_rows_in_block)+'-out.tsv', 'rb') as r_file:
        all_compressed_data = r_file.read()
    r_file.close()

    # header info
    magic_number = full_header[0]
    version = full_header[1]
    delimeter = full_header[2]
    col_names = full_header[3]
    col_types = full_header[4]
    num_columns = full_header[5]
    gzip_header = full_header[6]
    block_header_lengths = full_header[7]
    end_positions = full_header[8]
    block_sizes = full_header[9]

    # getting proper number of rows (last block is weird)
    if query_block_i < len(end_positions) - 1:
        curr_block_num_rows = block_sizes[0]
    else:
        curr_block_num_rows = block_sizes[1]

    # get correct block header
    ds_dc_curr_block = []
    if query_block_i != 0:
        try: query_block_header_start = end_positions[query_block_i-1]
        except IndexError:
            print("Invalid query option.")
    else: query_block_header_start = 0
    query_block_header_length = block_header_lengths[query_block_i]
    query_block_header_end = query_block_header_start+query_block_header_length
    query_block_header = gzip_header + all_compressed_data[query_block_header_start:query_block_header_end]
    # get decompressed, deserialized block header
    dc_curr_block_header = decompress.decompress_data(query_block_header)
    ds_dc_curr_block_header = deserialize.deserialize_data(
            dc_curr_block_header, num_columns, 1, DATA_TYPE_BYTE_SIZES[1])

    # getcurrent block data
    # for each compressed column in this block we need to add the gzip header separately
    query_block_data_start = query_block_header_end
    for column in range(num_columns):
        query_block_data_end = query_block_data_start+ds_dc_curr_block_header[row]
        # curr_block_data = gzip_header+all_compressed_data[curr_block_data_start:curr_block_data_end]
        # curr_block_data_start = curr_block_data_end
        #
        # dc_curr_block_data = decompress.decompress_data(curr_block_data)
        #
        # col_type = col_types[row]
        # ds_dc_curr_block_data = deserialize.deserialize_data(
        #     dc_curr_block_data, curr_block_num_rows, col_type, DATA_TYPE_BYTE_SIZES[col_type])
        # ds_dc_curr_block.append(ds_dc_curr_block_data)


    # num_blocks = len(end_positions)
    # curr_block_header_start = 0
    # for block_i in range(num_blocks):
    #
    #     # getting proper number of rows (last block is weird)
    #     if block_i < len(end_positions) - 1:
    #         curr_block_num_rows = block_sizes[0]
    #     else:
    #         curr_block_num_rows = block_sizes[1]
    #
    #     # current block header
    #     curr_block_header_length = block_header_lengths[block_i]
    #     curr_block_header_end = curr_block_header_start+curr_block_header_length
    #     curr_block_header = gzip_header + all_compressed_data[curr_block_header_start:curr_block_header_end]
    #
    #     dc_curr_block_header = decompress.decompress_data(curr_block_header)
    #     ds_dc_curr_block_header = deserialize.deserialize_data(
    #         dc_curr_block_header, num_columns, 1, DATA_TYPE_BYTE_SIZES[1])
    #
    #     ds_dc_curr_block = []
    #     # current block data
    #     curr_block_data_start = curr_block_header_end
    #     # for each compressed column in this block we need to add the gzip header separately
    #     for row in range(len(ds_dc_curr_block_header)):
    #         curr_block_data_end = curr_block_data_start+ds_dc_curr_block_header[row]
    #         curr_block_data = gzip_header+all_compressed_data[curr_block_data_start:curr_block_data_end]
    #         curr_block_data_start = curr_block_data_end
    #
    #         dc_curr_block_data = decompress.decompress_data(curr_block_data)
    #
    #         col_type = col_types[row]
    #         ds_dc_curr_block_data = deserialize.deserialize_data(
    #             dc_curr_block_data, curr_block_num_rows, col_type, DATA_TYPE_BYTE_SIZES[col_type])
    #         ds_dc_curr_block.append(ds_dc_curr_block_data)
    #
    #     ds_full_data.append(ds_dc_curr_block)
    #
    #     curr_block_header_start = end_positions[block_i]
    # for b in ds_full_data: print(b)
    # return ds_full_data
    x = 'debug'


def decompress_full_block():
    x = 'debug'

if __name__ == "__main__":
    main()
