import gzip

'''
to handle all input file formats and put them into the proper format to feed into compression system
'''
TAB_FILE_75 = '/Users/kristen/Desktop/compression_sandbox/toy_data/75-lines-tab.tsv'
TAB_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-tab.tsv'
COMMA_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-comma.csv'
SPACE_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-space.ssv'
BLOCK_SIZE = 5

def main():
    print('...converting to kristen format...')
    determine_delimeter(TAB_FILE)
    determine_delimeter(COMMA_FILE)
    determine_delimeter(SPACE_FILE)
    print(make_blocks(TAB_FILE, BLOCK_SIZE)[0].split('\n'))


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
            

def ks_ds_list_of_cols(blocks): 
    '''
    stores data in lists of cols

    INPUTS
    blocks: list of strings, where each string is all lines in a block (e.g. '1\t100\t500\tA...\n1\t501\t600\G...'
    OUTPUTS
    list of cols:
        [[col1, col2, col3, ..., coln],[col1, col2, col3, ..., coln], ..., [col1, col2, col3, ..., coln]]
        
        all_blocks = [block1, block2, ..., blockn]
            block1 = [col1, col2, col3, ..., colm]    
    '''

    list_cols = []
    return list_cols

def ks_ds_dict_cols_blocks(blocks):
    '''
    stores data in dictionary where keys are column names and values are list of blocks

    INPUTS
    blocks: list of strings, where each string is all lines in a block (e.g. '1\t100\t500\tA...\n1\t501\t600\G...'
    OUTPUTS
    dictionary of blocks: cols:
        [chr:[1, col2, col3, ..., coln],[col1, col2, col3, ..., coln], ..., [col1, col2, col3, ..., coln]]
        
        all_blocks = [block1, block2, ..., blockn]
            block1 = [col1, col2, col3, ..., colm]    
    '''


def ks_ds_dict_blocks_cols(blocks):        
    '''
    stores data in lists of cols data structure

    INPUTS
    blocks: list of strings, where each string is all lines in a block (e.g. '1\t100\t500\tA...\n1\t501\t600\G...'
    '''

if __name__ == '__main__':
    main()
