import compress_column

def compress_block(block, codecs_list, column_types, input_data_type_list, data_type_byte_sizes):
    # serialized block info:
    ##  serialized block header
    ##  serliazed block data
    serialized_block = b''
   
    block_header_compression_method = 'gzip'
    
    # compress one column at a time
    for column_i in range(len(block)):
        # current column info
        curr_column = block[column_i]
        curr_codec = codecs_list[column_i]
        curr_data_type = column_types[column_i]
        curr_compression_data_type = input_data_type_list[column_i]
        curr_data_type_byte_sizes =


        
        compress_column.compress_column(curr_column, curr_codec)

