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
     b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff', [40, 80, 120], [303, 553, 814], [3, 3]]


def main():
    num_rows_in_block = 3#int(input("Enter number of rows to be in each block: "))
    block_to_decompress = 0#int(input("Enter block to decompress: "))
    column_to_decompress = 0#int(input("Enter column to decompress: "))
    compressed_block_info = query_block(COMPRESSED_FILE, block_to_decompress)
    print(compressed_block_info)
    print(decompress_single_block(compressed_block_info))
    print(decompress_single_column(compressed_block_info, column_to_decompress))


def query_block(compressed_file, query_block_i):
    # get full header somehow. later.

    # header info
    magic_number = full_header[0]
    version = full_header[1]
    delimeter = full_header[2]
    col_names = full_header[3]
    col_types = full_header[4]
    num_columns = full_header[5]
    gzip_header = full_header[6]
    block_header_ends = full_header[7]
    end_positions = full_header[8]
    block_sizes = full_header[9]

    # getting proper number of rows (last block is weird)
    if query_block_i < len(end_positions) - 1:
        query_block_num_rows = block_sizes[0]
    else:
        query_block_num_rows = block_sizes[1]

    with open(compressed_file + 'kristen-' + str(query_block_num_rows) + '-out.tsv', 'rb') as r_file:
        all_compressed_data = r_file.read()
    r_file.close()

    # get correct block header
    ds_dc_curr_block = []
    if query_block_i != 0:
        try:
            query_block_header_start = end_positions[query_block_i - 1]
        except IndexError:
            print("Invalid query option.")
    else:
        query_block_header_start = 0

    query_block_header_end = block_header_ends[query_block_i]
    query_block_header = gzip_header + all_compressed_data[query_block_header_start:query_block_header_end]
    # get decompressed, deserialized block header
    dc_curr_block_header = decompress.decompress_data(query_block_header)
    ds_dc_curr_block_header = deserialize.deserialize_data(
        dc_curr_block_header, num_columns, 1, DATA_TYPE_BYTE_SIZES[1])


    return [ds_dc_curr_block_header, all_compressed_data[query_block_header_end:end_positions[query_block_i]], query_block_num_rows]

def decompress_single_block(compressed_block):
    # header info
    magic_number = full_header[0]
    version = full_header[1]
    delimeter = full_header[2]
    col_names = full_header[3]
    col_types = full_header[4]
    num_columns = full_header[5]
    gzip_header = full_header[6]
    block_header_ends = full_header[7]
    end_positions = full_header[8]
    block_sizes = full_header[9]

    compressed_block_header = compressed_block[0]
    compressed_block_data = compressed_block[1]
    num_rows = compressed_block[2]

    ds_dc_query_block = []

    # getcurrent block data
    # for each compressed column in this block we need to add the gzip header separately
    column_start = 0
    for column in range(num_columns):
        column_end = compressed_block_header[column]
        column_data = gzip_header + compressed_block_data[column_start:column_end]
        dc_column_data = decompress.decompress_data(column_data)
        col_type = col_types[column]
        ds_dc_column_data = deserialize.deserialize_data(
            dc_column_data, num_rows, col_type, DATA_TYPE_BYTE_SIZES[col_type])
        ds_dc_query_block.append(ds_dc_column_data)
        column_start = column_end

    return ds_dc_query_block

def decompress_single_column(compressed_block, query_column_i):
    # header info
    magic_number = full_header[0]
    version = full_header[1]
    delimeter = full_header[2]
    col_names = full_header[3]
    col_types = full_header[4]
    num_columns = full_header[5]
    gzip_header = full_header[6]
    block_header_ends = full_header[7]
    end_positions = full_header[8]
    block_sizes = full_header[9]

    dc_ds_block_header = compressed_block[0]
    compressed_block_data = compressed_block[1]
    num_rows = compressed_block[2]
    col_type = col_types[query_column_i]



    # get correct block header
    ds_dc_column = []
    if query_column_i != 0:
        try:
            compressed_column_start = dc_ds_block_header[query_column_i - 1]
        except IndexError:
            print("Invalid query option.")
    else:
        compressed_column_start = 0

    compressed_column_end = dc_ds_block_header[query_column_i]
    compressed_column = gzip_header + compressed_block_data[compressed_column_start:compressed_column_end]
    dc_column_data = decompress.decompress_data(compressed_column)
    ds_ds_column_data = deserialize.deserialize_data(dc_column_data, num_rows, col_type, DATA_TYPE_BYTE_SIZES[col_type])
    return ds_ds_column_data

if __name__ == "__main__":
    main()
