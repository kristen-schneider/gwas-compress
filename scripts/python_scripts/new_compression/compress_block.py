import compress_column
import serialize_body
import compress

def compress_block(block, codecs_list, COMPRESSION_DATA_TYPES, DECOMPRESSION_DATA_TYPES, data_type_byte_sizes, config_file_name):
    serialized_block = b''
   
    block_header_codec = 'bz2'

    column_end = 0
    block_header_list = []
    block_header_bitstring = b''
    block_bitstring = b''
    # compress one column at a time
    for column_i in range(len(block)):
        # current column info
        curr_column = block[column_i]
        curr_codec = codecs_list[column_i]
        curr_compression_data_type = int(COMPRESSION_DATA_TYPES[column_i])
        curr_decompression_data_type = int(DECOMPRESSION_DATA_TYPES[column_i])
        curr_data_type_byte_sizes = data_type_byte_sizes[curr_compression_data_type]

        compressed_column_bitstring = compress_column.column_compression_main(column_i, curr_column, curr_codec, curr_compression_data_type, curr_decompression_data_type, curr_data_type_byte_sizes, config_file_name)
        # append column info to block info
        column_end += len(compressed_column_bitstring)
        block_header_list.append(column_end)
        block_bitstring += compressed_column_bitstring

    # block_header_bitstring = compress_column.column_compression_main(block_header_list, block_header_codec,
    #                                                              1, 1, data_type_byte_sizes[1])
    block_header_serialized = serialize_body.serialize_list(block_header_list, 1, data_type_byte_sizes[1])
    block_header_bitstring = compress.compress_bitstring(block_header_serialized, block_header_codec)
    return block_header_bitstring, block_bitstring
