import decompress
import deserialize
import decompress_serialized_data

def query_block(compression_method_code_book, query_block_i, full_header,
                full_header_bytes, data_type_byte_sizes, compressed_file):
    """
    finds block to decompress and decompresses it's header, but keeps data in compressed form.
    returns decompressed block header, compressed block, and num rows in block

    INPUT
        compression_method_code_book: e.g. {'gzip':1, 'zlib':2, 'bz2':3}
        query_block_i: integer value which specifies which block we want to decompress
        full_header: decompressed version of full header
        full_header_bytes: number of bytes taken up by full header (to use as offset when reading compressed data)
        data_type_byte_sizes: from config file, assigns bytes to each data type, for compression
        compressed_file: file where compressed data has been written (read this to decompress)

    OUTPUT
        [ds_dc_curr_block_header: decompressed block header with end positions of columns
        content_compressed_data[query_block_header_end:end_positions[query_block_i]]:compressed block
        query_block_num_rows: number of rows that are in this block (different for last block sometimes)]
    """
    # header info
    magic_number = full_header[0]
    version = full_header[1]
    delimeter = full_header[2]
    col_names = full_header[3]
    col_types = full_header[4]
    num_columns = full_header[5]
    gzip_header = full_header[6]
    zlib_header = full_header[7]
    bz2_header = full_header[8]
    block_header_ends = full_header[9]
    end_positions = full_header[10]
    block_sizes = full_header[11]

    # header is compressed with gzip
    header_compression_type = 'gzip'


    # getting proper number of rows (last block is often less than others)
    if query_block_i < len(end_positions) - 1:
        query_block_num_rows = block_sizes[0]
    else:
        query_block_num_rows = block_sizes[1]

    with open(compressed_file, 'rb') as r_file:
        all_compressed_data = r_file.read()
    # print(all_compressed_data)
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
    # get decompressed, deserialized block header (compressed with gzip for now)
    dc_curr_block_header = decompress.decompress_data(compression_method_code_book[header_compression_type],
                                                      query_block_header)
    # print(dc_curr_block_header)
    ds_dc_curr_block_header = deserialize.deserialize_data(
        dc_curr_block_header, num_columns, 1, data_type_byte_sizes[1], None)
    # print(ds_dc_curr_block_header)

    x = 'debug'
    return [ds_dc_curr_block_header,
            content_compressed_data[query_block_header_end:end_positions[query_block_i]],
            query_block_num_rows]


def decompress_single_block(compression_method_code_book, compression_method_list, compressed_block,
                            full_header, data_type_byte_sizes):
    """
    decompresses a single block of data from compressed file

    INPUT
        compression_method_code_book: e.g. {'gzip':1, 'zlib':2, 'bz2':3}
        compression_method_list: list of compression methods for all columns
        compressed_block: [decompressed block header, compressed data for a full block]
        full_header: decompressed version of full header
        data_type_byte_sizes: from config file, assigns bytes to each data type, for compression

    OUTPUT
        ds_dc_query_block: list of decompressed data (all of proper type)
    """

    # header info
    magic_number = full_header[0]
    version = full_header[1]
    delimiter = full_header[2]
    col_names = full_header[3]
    col_types = full_header[4]
    num_columns = full_header[5]
    gzip_header = full_header[6]
    gzip_header = full_header[6]
    zlib_header = full_header[7]
    bz2_header = full_header[8]
    block_header_ends = full_header[9]
    end_positions = full_header[10]
    block_sizes = full_header[11]

    compressed_block_header = compressed_block[0]
    compressed_block_data = compressed_block[1]
    num_rows = compressed_block[2]

    ds_dc_query_block = []

    # iterate over each column and deserialize/decompress every column and append data to ds_dc_query_block
    for column_i in range(num_columns):
        col_compression_method = compression_method_list[column_i]
        ds_dc_column_data = decompress_single_column(compression_method_code_book, col_compression_method,
                                 compressed_block, column_i, full_header, data_type_byte_sizes)
        ds_dc_query_block.append(ds_dc_column_data)
    return ds_dc_query_block

def decompress_single_column(compression_method_code_book, compression_method, compressed_block,
                             query_column_i, full_header, data_type_byte_sizes):
    """
    decompresses a single column of data from compressed file

    INPUT
        compression_method_code_book: e.g. {'gzip':1, 'zlib':2, 'bz2':3}
        compression_method: compression method used for given column
        compressed_block: [decompressed block header, compressed data for a full block]
        query_column_i: integer column number to decompress
        full_header: decompressed version of full header
        data_type_byte_sizes: from config file, assigns bytes to each data type, for compression

    OUTPUT
        ds_ds_column_data: decompressed column (as a list of values)
    """

    # header info
    magic_number = full_header[0]
    version = full_header[1]
    delimiter = full_header[2]
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

    # get proper compression header for given column
    compression_header = get_compression_header(compression_method, full_header)

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
    compressed_column = compression_header + compressed_block_data[compressed_column_start:compressed_column_end]
    
    # Switch decompression methods for different compression types (codecs vs. other)
    if compression_method == 'gzip' or \
        compression_method == 'zlib' or \
        compression_method == 'bz2':
        # dc_column_data = decompress.decompress_data(compression_method_code_book[compression_method], compressed_column)
        # ds_dc_column_data = deserialize.deserialize_data(dc_column_data, num_rows, col_type,
        #                                              data_type_byte_sizes[col_type], query_column_i)

        ds_dc_column_data = decompress_serialized_data.decompress_single_column(compression_method_code_book[compression_method],
                                                                                compressed_column,
                                                                                num_rows,
                                                                                col_type,
                                                                                data_type_byte_sizes[col_type],
                                                                                query_column_i)
    return ds_dc_column_data

def get_compression_header(column_compression_method, full_header):
    """
    returns proper compression header for each compression type
    """
    codec_header = b''
    if column_compression_method == 'gzip':
        return full_header[6]
    elif column_compression_method == 'zlib':
        return full_header[7]
    elif column_compression_method == 'bz2':
        return full_header[8]
    elif column_compression_method == 'fastpfor128':
        return codec_header
    elif column_compression_method == 'fastpfor256':
        return codec_header
    else:
        print('invalid compression type. cannot return a header.')
        return 0
