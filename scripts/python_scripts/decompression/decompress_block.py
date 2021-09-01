import deserialize_body
import decompress_column

def get_compressed_data(query_block_i, full_header,
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
    block_header_ends = full_header[6]
    end_positions = full_header[7]
    block_sizes = full_header[8]

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

#def decompress_block():
