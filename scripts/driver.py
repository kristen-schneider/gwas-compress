import funnel_format
import file_header
import serialize
import compress
import decompress
import deserialize


IN_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-tab.tsv'
BLOCK_SIZE = 4
BYTE_SIZES = {int: 5, float: 8, bool: 5, str: 5}

def write_new_file(in_file, block_size):
    '''
    takes a file, converts to funnel format, serializes and compresses each block, write to out_file 
    
    INPUTS
    in_file: path to input file
    block_size = number of lines in each block  
    
    OUTPUTS
    write to file

    '''

    # [delimeter, [col_names], [col_types], num_cols]
    file_info = file_header.get_file_data(IN_FILE)
    delimeter = file_info[0]
    col_names = file_info[1]
    col_types = file_info[2]
    num_columns = file_info[3]
    print('header: ', file_info, '\n')
    
    funnel_format_data = funnel_format.make_all_blocks(IN_FILE, BLOCK_SIZE, num_columns, delimeter)
    num_blocks = len(funnel_format_data)
    print('funnel_format:\n')
    
    # for each block
        # serialize and compress
        # store size of compressed data
    for b in range(num_blocks):
        curr_block = funnel_format_data[b]
        block_size = len(funnel_format_data[b][0])
        print(b, curr_block, block_size)     
        
        s_block = serialize.serialize_list_columns(curr_block, BYTE_SIZES)
        c_block = compress.compress_data(s_block, 0)
        dc_block = decompress.decompress_data(c_block)
        ds_block = deserialize.deserialize_block_bitstring(dc_block, block_size, col_types, BYTE_SIZES)
        print(ds_block) 
    #blocks = funnel_format.make_all_blocks(IN_FILE, BLOCK_SIZE, NUM_COLUMNS)
    
    return 0


write_new_file(IN_FILE, BLOCK_SIZE)
