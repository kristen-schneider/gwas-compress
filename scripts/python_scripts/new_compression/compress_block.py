import compress_column

def compress_block(block, codecs_list, data_type, data_type_bytes):
    # serialized block info:
    ##  serialized block header
    ##  serliazed block data
    serialized_block = b''
   
    block_header_compression_method = 'gzip'
    
    # compress one column at a time
    for column_i in range(len(block)):
        # current column info
        curr_column = block[column_i]
        col_codec = codec_list[curr_column]
    
        
        compress_column.compress_column(curr_column, col_codec)

