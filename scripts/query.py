from datetime import datetime
import decompress
import deserialize

# 1. output file
COMPRESSED_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/'
#FIJI
#COMPRESSED_FILE = '/scratch/Users/krsc0813/gwas-compress/data/compressed/'
# 2. block size
BLOCK_SIZE = 3
# 3. bytes for each data type
DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes:4}
DATA_TYPE_BYTE_SIZES = {1: 5, 2: 8, 3: 5, 4:None}



#full_header = [1, 1, '\t', ['chr', 'pos', 'ref', 'alt', 'af_cases_EUR', 'af_controls_EUR', 'beta_EUR', 'se_EUR', 'pval_EUR', 'low_confidence_EUR'], [1, 1, 3, 3, 2, 2, 2, 2, 2, 3], 10, b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff', [57, 2148765, 4290908, 6406763, 8508534, 10496717, 12643750, 14723260, 16805127, 18896080], [2148707, 4290849, 6406704, 8508475, 10496659, 12643692, 14723202, 16805069, 18896022, 20977667], [100000, 99999]]


def main():
    num_rows_in_block = BLOCK_SIZE#int(input("Enter number of rows to be in each block: "))
    block_to_decompress = 0#int(input("Enter block to decompress: "))
    column_to_decompress = 9#int(input("Enter column to decompress: "))

    full_header = get_full_header(COMPRESSED_FILE, BLOCK_SIZE)

    #
    #
    # compressed_block_info = query_block(COMPRESSED_FILE, block_to_decompress)
    # # print(compressed_block_info)
    #
    # print('decompressing single block...')
    # single_block_START = datetime.now()
    # dc_single_block = decompress_single_block(compressed_block_info)
    # #print(dc_single_block)
    # single_block_END = datetime.now()
    # single_block_TIME = single_block_END - single_block_START
    # print(str(single_block_TIME) + ' for decompressing single block to compute...\n')
    #
    # print('decompressing single column...')
    # single_column_START = datetime.now()
    # dc_single_column = decompress_single_column(compressed_block_info, column_to_decompress)
    # # print(dc_single_column)
    # single_column_END = datetime.now()
    # single_column_TIME = single_column_END - single_column_START
    # print(str(single_column_TIME) + ' for decompressing single column to compute...\n')

def get_full_header(compressed_file, block_size):
    compressed_file = open(compressed_file + 'kristen-' + str(BLOCK_SIZE) + '-out.tsv', 'rb')
    #content = compressed_file.read()
    STOP_HEADER = False

    HEADER_SIZES = []
    HEADER_ENDS = None
    HEADER_DATA = None
    while not STOP_HEADER:

        # get 2 sizes first (2 bytes each)
        if len(HEADER_SIZES) < 2:
            num_bytes_to_read = 2

            header_ends_size = compressed_file.read(num_bytes_to_read)
            ds_header_ends_size = deserialize.deserialize_int(header_ends_size, 1, 2, 0)[0]
            HEADER_SIZES.append(ds_header_ends_size)

            header_data_size = compressed_file.read(num_bytes_to_read)
            ds_header_data_size = deserialize.deserialize_int(header_data_size, 1, 2, 0)[0]
            HEADER_SIZES.append(ds_header_data_size)
        elif HEADER_ENDS == None:
            num_bytes_to_read = HEADER_SIZES[0]

            header_ends = compressed_file.read(num_bytes_to_read)
            ds_header_ends = deserialize.deserialize_int(header_ends, 10, 5, 0)

        elif HEADER_DATA == None:
            num_bytes_to_read = HEADER_SIZES[1]

            header_data = compressed_file.read(num_bytes_to_read)
            ds_header_data = deserialize.deserialize_data()


            x = 2

        if header_ends_size == b'': STOP_HEADER = True
    compressed_file.close()


def query_block(compressed_file, query_block_i, full_header):
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

    with open(compressed_file + 'kristen-' + str(BLOCK_SIZE) + '-out.tsv', 'rb') as r_file:
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

    # to signify that we need not worry about X and Y in data
    chrm = False
    query_block_header_end = block_header_ends[query_block_i]
    query_block_header = gzip_header + all_compressed_data[query_block_header_start:query_block_header_end]
    # get decompressed, deserialized block header
    dc_curr_block_header = decompress.decompress_data(query_block_header)
    print(dc_curr_block_header)
    ds_dc_curr_block_header = deserialize.deserialize_data(
        dc_curr_block_header, num_columns, 1, DATA_TYPE_BYTE_SIZES[1], None)
    print(ds_dc_curr_block_header)

    x = 'debug'
    return [ds_dc_curr_block_header, all_compressed_data[query_block_header_end:end_positions[query_block_i]], query_block_num_rows]

def decompress_single_block(compressed_block, full_header):
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
        if column == 0: chrm = True
        else: chrm = False
        column_end = compressed_block_header[column]
        column_data = gzip_header + compressed_block_data[column_start:column_end]
        dc_column_data = decompress.decompress_data(column_data)
        col_type = col_types[column]
        ds_dc_column_data = deserialize.deserialize_data(
            dc_column_data, num_rows, col_type, DATA_TYPE_BYTE_SIZES[col_type], column)
        ds_dc_query_block.append(ds_dc_column_data)
        column_start = column_end

    return ds_dc_query_block

def decompress_single_column(compressed_block, query_column_i, full_header):
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
    ds_ds_column_data = deserialize.deserialize_data(dc_column_data, num_rows, col_type, DATA_TYPE_BYTE_SIZES[col_type], query_column_i)
    return ds_ds_column_data

if __name__ == "__main__":
    main()
