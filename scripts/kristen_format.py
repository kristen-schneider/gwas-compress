import gzip

'''
to handle all input file formats and put them into the proper format to feed into compression system
'''
TAB_FILE_10000 = '/Users/kristen/Desktop/compression_sandbox/toy_data/10000-lines-tab.tsv'
TAB_FILE_75 = '/Users/kristen/Desktop/compression_sandbox/toy_data/75-lines-tab.tsv'
TAB_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-tab.tsv'
COMMA_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-comma.csv'
SPACE_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-space.ssv'
BLOCK_SIZE = 5000

def main():
    print('...converting to kristen format...')
    tab_d = determine_delimeter(TAB_FILE)
    comma_d = determine_delimeter(COMMA_FILE)
    space_d = determine_delimeter(SPACE_FILE)
    header = get_header(TAB_FILE, tab_d)
    blocks = make_blocks(TAB_FILE, BLOCK_SIZE)
    ds1 = ks_ds_list_of_cols(len(header), blocks, tab_d)
    ds2 = ks_ds_dict_cols_blocks(header, blocks, tab_d)
    ds3 = ks_ds_dict_blocks_cols(len(header), blocks, tab_d)
    write_ds1(ds1)
    write_ds2(ds2)
    write_ds3(ds3)
    
def determine_delimeter(f):
    '''
    deterimine which delimeter is used in the file
    
    INPUTS
    f: path to input file
    OUTPUS
    returns delimeter used in file
    '''
    with open(f, 'r') as f_open:
        header = f_open.readline()
        if len(header.split('\t')) > 1: return '\t'
        elif len(header.split(' ')) > 1: return ' '
        elif len(header.split(',')) > 1: return ','
    
    f_open.close()

def get_header(f, delimeter):
    '''
    stores a string which is the header of the file, so that we know what columns are included and need be stored
    
    INPUTS
    f = path to uncompressed input file
    OUTPUTS
    header = list of the first row of the file

    '''
    with open(f, 'r') as f_open:
        header = f_open.readline().rstrip().split(delimeter)
    return header

def get_chr_format(f, delimeter):
    '''
    looking to see how the first column (chr) is formatted
    
    INPUTS
    f = path to uncompressed input file
    
    '''    


 
def make_blocks(f, block_size):
    '''
    splits a file into blocks

    INPUTS
    f = path to input file
    block_size = number of lines per block
    OUTPUTS
    a list of all blocks. one block is a string that might look like '1\t10294\t10306\tA...\n1\t10307\t10543\t...'
    '''
    # initialize variables
    all_blocks = []    
    header = ''
    curr_block = ''
    line_count_per_block = 0
    
    f_open = open(f, 'r')
    for line in f_open:
        # grab header
        if header == '': header = line
        # add new block every 'block_size' lines
        else:
            if line_count_per_block < block_size:
                curr_block += line
                line_count_per_block += 1
            else:
                all_blocks.append(curr_block.rstrip())
                curr_block = line
                line_count_per_block = 1
    all_blocks.append(curr_block.rstrip())
    f_open.close()
    return all_blocks
            

