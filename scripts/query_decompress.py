import decompress
import deserialize

# COMPRESSION_METHOD_CODE_BOOK = {'gzip':1, 'zlib':2}

def query_block(compression_method_code_book, comppression_method,
                compressed_file, query_block_i, full_header, full_header_bytes, DATA_TYPE_BYTE_SIZES, OUT_FILE):
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

    with open(OUT_FILE, 'rb') as r_file:
        all_compressed_data = r_file.read()
    r_file.close()

    header_data = all_compressed_data[0:full_header_bytes]
    content_compressed_data = all_compressed_data[full_header_bytes:]


    # get correct block header
    if query_block_i != 0:
        try:
            query_block_header_start = end_positions[query_block_i - 1]
        except IndexError:
            print("Invalid query option.")
    else:
        query_block_header_start = 0

    # to signify that we need not worry about X and Y in data
    query_block_header_end = block_header_ends[query_block_i]
    query_block_header = gzip_header + content_compressed_data[query_block_header_start:query_block_header_end]
    # get decompressed, deserialized block header
    dc_curr_block_header = decompress.decompress_data(compression_method_code_book[comppression_method], query_block_header)
    # print(dc_curr_block_header)
    ds_dc_curr_block_header = deserialize.deserialize_data(
        dc_curr_block_header, num_columns, 1, DATA_TYPE_BYTE_SIZES[1], None)
    # print(ds_dc_curr_block_header)

    x = 'debug'
    return [ds_dc_curr_block_header, content_compressed_data[query_block_header_end:end_positions[query_block_i]], query_block_num_rows]


def decompress_single_block(compression_method_code_book, compression_method, compressed_block, full_header, DATA_TYPE_BYTE_SIZES):
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
    for column_i in range(num_columns):
        if column_i == 0: chrm = True
        else: chrm = False
        column_end = compressed_block_header[column_i]
        column_data = gzip_header + compressed_block_data[column_start:column_end]
        dc_column_data = decompress.decompress_data(compression_method_code_book[compression_method], column_data)
        col_type = col_types[column_i]
        ds_dc_column_data = deserialize.deserialize_data(
            dc_column_data, num_rows, col_type, DATA_TYPE_BYTE_SIZES[col_type], chrm)
        ds_dc_query_block.append(ds_dc_column_data)
        column_start = column_end

    return ds_dc_query_block

def decompress_single_column(compression_method_code_book, compression_method, compressed_block, query_column_i,
                             full_header, DATA_TYPE_BYTE_SIZES):
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
    dc_column_data = decompress.decompress_data(compression_method_code_book[compression_method], compressed_column)
    ds_ds_column_data = deserialize.deserialize_data(dc_column_data, num_rows, col_type,
                                                     DATA_TYPE_BYTE_SIZES[col_type], query_column_i)
    return ds_ds_column_data