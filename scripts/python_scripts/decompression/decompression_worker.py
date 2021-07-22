import deserialize_body
import decompress_column
import type_handling
import hybrid_strings


# import decompress_serialized_data
# import decompress_array_data


def query_block(query_block_i, full_header,
                full_header_bytes, data_type_byte_sizes, compressed_file):
    """
    finds block to decompress and decompresses it's header, but keeps data in compressed form.
    returns decompressed block header, compressed block, and num rows in block

    INPUT
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
    delimiter = full_header[2]
    column_labels = full_header[3]
    column_data_types = full_header[4]
    num_columns = full_header[5]
    gzip_header = full_header[6]
    bz2_header = full_header[7]
    block_header_ends = full_header[8]
    end_positions = full_header[9]
    block_sizes = full_header[10]
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

    query_block_header_end = block_header_ends[query_block_i]
    query_block_header_bytes = content_compressed_data[query_block_header_start:query_block_header_end]
    query_block_header_np_arr = deserialize_body.deserialize_list_fastpfor(query_block_header_bytes)
    query_block_header_decomp_arr = decompress_column.decompress_np_arr(query_block_header_np_arr, num_columns, 'fastpfor128')
    #dc_curr_block_header = np.array(query_block_header, dtype=np.uint32, order='C') 
    # print(dc_curr_block_header)
    #ds_dc_curr_block_header = deserialize_header.deserialize_list(
    #    dc_curr_block_header, num_columns, 1, data_type_byte_sizes[1], None)
    # print(ds_dc_curr_block_header)

    return [query_block_header_decomp_arr,
            content_compressed_data[query_block_header_end:end_positions[query_block_i]],
            query_block_num_rows]


def decompress_single_block_int(compression_method_list, compressed_block,
                            full_header, data_type_byte_sizes):
    """
    decompresses a single block of data from compressed file

    INPUT
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
    column_labels = full_header[3]
    column_data_types = full_header[4]
    num_columns = full_header[5]
    gzip_header = full_header[6]
    bz2_header = full_header[7]
    block_header_ends = full_header[8]
    end_positions = full_header[9]
    block_sizes = full_header[10]
    compressed_block_header = compressed_block[0]
    compressed_block_data = compressed_block[1]
    num_rows = compressed_block[2]

    ds_dc_query_block = []
    # iterate over each column and deserialize/decompress every column and append data to ds_dc_query_block
    for column_i in range(num_columns):
        col_compression_method = compression_method_list[column_i]
        ds_dc_column_data = decompress_single_column_int(col_compression_method, compressed_block,
                                                     column_i, full_header, data_type_byte_sizes)
        
        ds_dc_query_block.append(ds_dc_column_data)
    return ds_dc_query_block

def decompress_single_column_int(compression_method, compressed_block,
                             query_column_i, full_header, data_type_byte_sizes):
    """
    decompresses a single column of data from compressed file

    INPUT
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
    column_labels = full_header[3]
    column_data_types = full_header[4]
    num_columns = full_header[5]
    gzip_header = full_header[6]
    bz2_header = full_header[7]
    block_header_ends = full_header[8]
    end_positions = full_header[9]
    block_sizes = full_header[10]

    if query_column_i == 0: chrm = 1
    else: chrm = 0
    
    dc_ds_block_header = compressed_block[0]
    compressed_block_data = compressed_block[1]
    num_rows = compressed_block[2]

    col_type = column_data_types[query_column_i]
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
    # print(compressed_block_data[compressed_column_start:compressed_column_end])
# Switch decompression methods for different compression types (codecs vs. other)
    if compression_method == 'gzip' or \
        compression_method == 'zlib' or \
        compression_method == 'bz2':

        ds_dc_column_data = decompress_column.decompress_single_column_standard(compressed_column,
                                                                                num_rows,
                                                                                col_type,
                                                                                data_type_byte_sizes[col_type],
                                                                                chrm,
                                                                                compression_method,
                                                                                query_column_i)


    elif 'fastpfor' in compression_method:
        # data input: serialized_data, block_size, data_type, num_bytes, chrm
        ds_dc_column_data = decompress_column.decompress_single_column_pyfast(compressed_column,
                                                                              num_rows,
                                                                              col_type,
                                                                              data_type_byte_sizes[col_type],
                                                                              chrm,
                                                                              compression_method,
                                                                              query_column_i)
    
        # must convert int back to float
        if col_type == 2:
            float_column = []
            for i in ds_dc_column_data:
                f = type_handling.int_to_float(i)
                float_column.append(f)
            return float_column
        # convert ints back to string
        if col_type == 3:
            #s = packed_strings.decode_int_to_string(ds_dc_column_data)
            s = hybrid_strings.decode_int_to_string(ds_dc_column_data)
            #string_column = []
            #for i in ds_dc_column_data:
                #s = type_handling.int_to_string(i)
                #string_column.append(s)
            #return string_column     
            return s   
    else:
        print('cannot find proper compression method to decompress')
        return -1     
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
