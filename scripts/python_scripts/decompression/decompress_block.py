import deserialize_body
import decompress_column

def get_compressed_block_data(query_block_i, full_header,
                full_header_bytes, data_type_byte_sizes, compressed_file, COMPRESSION_DATA_TYPES):
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
    #COMPRESSION_DATA_TYPES = full_header[4]
    num_columns = full_header[4]
    block_header_ends = full_header[5]
    end_positions = full_header[6]
    block_sizes = full_header[7]

    # header is compressed with gzip
    header_compression_type = 'gzip'

    # getting proper number of rows (last block is often less than others)
    if query_block_i < len(end_positions) - 1:
        query_block_num_rows = block_sizes[0]
    else:
        query_block_num_rows = block_sizes[1]

    with open(compressed_file, 'rb') as r_file:
        all_compressed_data = r_file.read()
    r_file.close()

    header_data = all_compressed_data[0:full_header_bytes]
    content_compressed_data = all_compressed_data[full_header_bytes:]

    # get correct block header and decompress and deserialize
    if query_block_i != 0:
        try:
            query_block_header_start = end_positions[query_block_i - 1]
        except IndexError:
            print("Invalid query option.")
    else:
        query_block_header_start = 0
    query_block_header_end = block_header_ends[query_block_i]
    query_block_header_bytes = content_compressed_data[query_block_header_start:query_block_header_end]
    dc_query_block_header = decompress_column.decompress_single_column_standard(query_block_header_bytes,
                                                                                num_columns,
                                                                                1, data_type_byte_sizes[1], 0,
                                                                                header_compression_type)

    compressed_block_content = content_compressed_data[query_block_header_end:end_positions[query_block_i]]
    return [dc_query_block_header,
            compressed_block_content,
            query_block_num_rows]

def decompress_single_block(dc_block_header, compessed_block, COMPRESSION_DATA_TYPES, query_block_num_rows, data_type_byte_sizes, codecs_list, input_dat_type_list):

    num_columns = len(dc_block_header)
    dc_block = []
    start = 0
    for i in range(num_columns):
        end = dc_block_header[i]
        curr_column_data_type = int(input_dat_type_list[i])#COMPRESSION_DATA_TYPES[i]
        curr_column_codec = codecs_list[i] 
        compressed_column = compessed_block[start:end]
        dc_column = decompress_column.decompress_single_column_standard(compressed_column, query_block_num_rows, curr_column_data_type, data_type_byte_sizes[curr_column_data_type], 0, curr_column_codec)
        dc_block.append(dc_column)    
    
        start = end 
        

    return dc_block










