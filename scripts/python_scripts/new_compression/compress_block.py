import compress_column
import serialize_body

def compress_block(block, codecs_list, column_types, input_data_type_list, data_type_byte_sizes):
    # serialized block info:
    ##  serialized block header
    ##  serliazed block data
    serialized_block = b''
   
    block_header_codec = 'gzip'

    column_end = 0
    block_header_list = []
    block_header_bitstring = b''
    block_bitstring = b''
    
    # compress one column at a time
    for column_i in range(len(block)):
        # current column info
        curr_column = block[column_i]
        curr_codec = codecs_list[column_i]
        curr_data_type = column_types[column_i]
        curr_compression_data_type = int(input_data_type_list[column_i])
        curr_data_type_byte_sizes = data_type_byte_sizes[curr_compression_data_type]

        compressed_column_bitstring = compress_column.column_compression_main(curr_column, curr_codec, curr_data_type,
                                                curr_compression_data_type, curr_data_type_byte_sizes)
        column_end += len(compressed_column_bitstring)
        block_header_list.append(column_end)
        block_bitstring += compressed_column_bitstring

    block_header_bitstring = compress_column.column_compression_main(block_header_list, block_header_codec,
                                                                 1, 1, data_type_byte_sizes[1])
    
    return block_header_bitstring, block_bitstring

