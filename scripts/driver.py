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

    fileheader = file_header.make_file_header(IN_FILE, BLOCK_SIZE)
    fileheader_data_type = [0, 0]
    #for i in fileheader:
    s_fileheader = serialize.serialize_data(fileheader, 5)
    ds_fileheader = deserialize.deserialize_list_bitstrings(s_fileheader, 2, [25,25], [0,0], [5,5])
    print(s_fileheader, ds_fileheader)
    
    blocks = funnel_format.make_all_blocks(IN_FILE, BLOCK_SIZE, NUM_COLUMNS)
    
    return 3


write_new_file(IN_FILE, BLOCK_SIZE)
