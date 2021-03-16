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
    blocks = funnel_format.make_all_blocks(IN_FILE, BLOCK_SIZE, NUM_COLUMNS)
    for b in blocks: print(b)
    
    fileheader = file_header.make_file_header(IN_FILE)
    
    return 3


write_new_file(IN_FILE, BLOCK_SIZE)
