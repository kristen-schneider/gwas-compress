import funnel_format
import serialize
import compress
import decompress
import deserialize


IN_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-tab.tsv'
BLOCK_SIZE = 10

def write_new_file(in_file, block_size):
    '''
    takes a file, converts to funnel format, serializes and compresses each block, write to out_file 
    
    INPUTS
    in_file: path to input file
    block_size = number of lines in each block  
    
    OUTPUTS
    write to file

    '''
    delimeter = funnel_format.determine_delimeter(in_file)
    blocks = funnel_format.split_into_blocks(in_file, 2)
    print(len(blocks))

    return 3


write_new_file(IN_FILE, BLOCK_SIZE)
