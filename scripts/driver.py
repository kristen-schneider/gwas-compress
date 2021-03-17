import funnel_format
import file_header
import serialize
import compress
import decompress
import deserialize


IN_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-tab.tsv'
BLOCK_SIZE = 4
NUM_COLUMNS = 10

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
    print(file_info)
    #s_fileheader = serialize.serialize_data(fileheader, 5)
    #print(s_fileheader)
    #c_fileheader = compress.compress_data(s_fileheader, 0)
    #print(c_fileheader)
    #dc_fileheader = decompress.decompress_data(c_fileheader)
    #print(dc_fileheader)
    #ds_fileheader = deserialize.deserialize_list_bitstrings(s_fileheader, 2, [25,25], [0,0], [5,5])
    
    #blocks = funnel_format.make_all_blocks(IN_FILE, BLOCK_SIZE, NUM_COLUMNS)
    
    return 0


write_new_file(IN_FILE, BLOCK_SIZE)
