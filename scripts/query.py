import sys
from datetime import datetime
import header_compress_decompress
import decompress
import deserialize

# 1. output file
COMPRESSED_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/'
#FIJI
#COMPRESSED_FILE = '/scratch/Users/krsc0813/gwas-compress/data/compressed/'
# 2. block size
#BLOCK_SIZE = 3
#FIJI
BLOCK_SIZE = int(sys.argv[1])
# 3. bytes for each data type
DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes:4}
DATA_TYPE_BYTE_SIZES = {1: 5, 2: 8, 3: 5, 4:None}


def main():
    num_rows_in_block = BLOCK_SIZE#int(input("Enter number of rows to be in each block: "))
    block_to_decompress = 0#int(input("Enter block to decompress: "))
    column_to_decompress = 1#int(input("Enter column to decompress: "))

    full_header_info = get_full_header(COMPRESSED_FILE, BLOCK_SIZE)
    full_header_bytes = full_header_info[0]
    full_header = full_header_info[1]



    compressed_block_info = query_block(COMPRESSED_FILE, block_to_decompress, full_header, full_header_bytes)
    # print(compressed_block_info)

    print('decompressing single block...')
    single_block_START = datetime.now()
    dc_single_block = decompress_single_block(compressed_block_info, full_header)
    print(dc_single_block)
    single_block_END = datetime.now()
    single_block_TIME = single_block_END - single_block_START
    print(str(single_block_TIME) + ' for decompressing single block to compute...\n')

    print('decompressing single column...')
    single_column_START = datetime.now()
    dc_single_column = decompress_single_column(compressed_block_info, column_to_decompress, full_header)
    print(dc_single_column)
    single_column_END = datetime.now()
    single_column_TIME = single_column_END - single_column_START
    print(str(single_column_TIME) + ' for decompressing single column to compute...\n')

def get_full_header(compressed_file, block_size):
    compressed_file = open(compressed_file + 'kristen-' + str(BLOCK_SIZE) + '-out.tsv', 'rb')
    #content = compressed_file.read()
    STOP_HEADER = False

    HEADER_TOOLS = []
    HEADER_TYPES = None
    HEADER_NUM_ELEMENTS = None
    HEADER_ENDS = None
    HEADER_DATA = None

    total_bytes_read = 0
    while not STOP_HEADER:
        # get 3 sizes first (2 bytes each)
        if len(HEADER_TOOLS) < 4:
            num_bytes_to_read = 2

            header_types_size = compressed_file.read(num_bytes_to_read)
            ds_header_types_size = deserialize.deserialize_int(header_types_size, 1, 2, 0)[0]
            HEADER_TOOLS.append(ds_header_types_size)
            total_bytes_read += num_bytes_to_read

            header_elements_size = compressed_file.read(num_bytes_to_read)
            ds_header_elements_size = deserialize.deserialize_int(header_elements_size, 1, 2, 0)[0]
            HEADER_TOOLS.append(ds_header_elements_size)
            total_bytes_read += num_bytes_to_read

            header_ends_size = compressed_file.read(num_bytes_to_read)
            ds_header_ends_size = deserialize.deserialize_int(header_ends_size, 1, 2, 0)[0]
            HEADER_TOOLS.append(ds_header_ends_size)
            total_bytes_read += num_bytes_to_read

            header_data_size = compressed_file.read(num_bytes_to_read)
            ds_header_data_size = deserialize.deserialize_int(header_data_size, 1, 2, 0)[0]
            HEADER_TOOLS.append(ds_header_data_size)
            total_bytes_read += num_bytes_to_read


        elif HEADER_TYPES == None:
            num_bytes_to_read = HEADER_TOOLS[0]

            header_types = compressed_file.read(num_bytes_to_read)
            ds_header_types = deserialize.deserialize_int(header_types, 10, 5, 0)
            HEADER_TYPES = ds_header_types
            total_bytes_read += num_bytes_to_read

        elif HEADER_NUM_ELEMENTS == None:
            num_bytes_to_read = HEADER_TOOLS[1]

            header_elements = compressed_file.read(num_bytes_to_read)
            ds_header_elements = deserialize.deserialize_int(header_elements, 10, 5, 0)
            HEADER_NUM_ELEMENTS = ds_header_elements
            total_bytes_read += num_bytes_to_read

        elif HEADER_ENDS == None:
            num_bytes_to_read = HEADER_TOOLS[2]

            header_ends = compressed_file.read(num_bytes_to_read)
            ds_header_ends = deserialize.deserialize_int(header_ends, 10, 5, 0)
            HEADER_ENDS = ds_header_ends
            total_bytes_read += num_bytes_to_read


        elif HEADER_DATA == None:
            num_bytes_to_read = HEADER_TOOLS[3]
            header_data = compressed_file.read(num_bytes_to_read)
            ds_header_data = header_compress_decompress.decompress_header(
                HEADER_TYPES, HEADER_NUM_ELEMENTS, HEADER_ENDS, header_data)
            HEADER_DATA = ds_header_data
            total_bytes_read += num_bytes_to_read
            #STOP_HEADER = True

        else: STOP_HEADER = True
        # if header_ends_size == b'': STOP_HEADER = True
    compressed_file.close()
    return total_bytes_read, HEADER_DATA


def query_block(compressed_file, query_block_i, full_header, full_header_bytes):
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

    header_data = all_compressed_data[0:full_header_bytes]
    content_compressed_data = all_compressed_data[full_header_bytes:]


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
    query_block_header = gzip_header + content_compressed_data[query_block_header_start:query_block_header_end]
    # get decompressed, deserialized block header
    dc_curr_block_header = decompress.decompress_data(query_block_header)
    # print(dc_curr_block_header)
    ds_dc_curr_block_header = deserialize.deserialize_data(
        dc_curr_block_header, num_columns, 1, DATA_TYPE_BYTE_SIZES[1], None)
    # print(ds_dc_curr_block_header)

    x = 'debug'
    return [ds_dc_curr_block_header, content_compressed_data[query_block_header_end:end_positions[query_block_i]], query_block_num_rows]

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
