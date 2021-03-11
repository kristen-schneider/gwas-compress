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
    tab_d = determine_delimeter(TAB_FILE)
    comma_d = determine_delimeter(COMMA_FILE)
    space_d = determine_delimeter(SPACE_FILE)
    header = get_header(TAB_FILE, tab_d)
    blocks = make_blocks(TAB_FILE, BLOCK_SIZE)
    ks_ds_list_of_cols(len(header), blocks, tab_d)
    ks_ds_dict_cols_blocks(header, blocks, tab_d)
    ks_ds_dict_blocks_cols(len(header), blocks, tab_d)

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
            

def ks_ds_list_of_cols(num_columns, blocks, delimeter): 
    '''
    stores data in lists of cols

    INPUTS
    num_columns: number of columns (usually len(header))
    blocks: list of strings, where each string is all lines in a block (e.g. '1\t100\t500\tA...\n1\t501\t600\G...'
    delimeter: delimeter of file (e.g. tab, space, comma)
    OUTPUTS
    list of cols:
        [[col1, col2, ..., coln],[col1, col2, ..., coln], ..., [col1, col2, ..., coln]]
        
        *specifically...*
        list_cols = [block1, block2, ..., blockn]
            block1 = [col1, col2, ..., colm]    
    
    '''
    all_blocks = []
    for b in blocks:
        list_cols = [''] * num_columns
        rows = b.split('\n')
        for r in rows:
            rows_list = r.split(delimeter)
            for rl in range(len(rows_list)):
                data = rows_list[rl] + delimeter
                list_cols[rl] += data
        all_blocks.append(list_cols) 
    
    return all_blocks

def ks_ds_dict_cols_blocks(header, blocks, delimeter):
    '''
    stores data in dictionary where keys are column names and values are list of blocks

    INPUTS
    blocks: list of strings, where each string is all lines in a block (e.g. '1\t100\t500\tA...\n1\t501\t600\G...'
    OUTPUTS
    dictionary of cols: blocks:
        [col1:[block1, block2, ..., blockn],
         col2:[block1, block2, ..., blockn], 
            ...
         colm:[block1, block2, ..., blockn]]
    *col1 here might be "chromosome"*
       
    '''
    
    final_dict = {col: [[] for i in range(len(blocks))] for col in header}
    for b in range(len(blocks)):
        rows = blocks[b].split('\n')
        for r in rows:
            rows_list = r.split(delimeter)
            for rl in range(len(rows_list)):
                final_dict[header[rl]][b].append(rows_list[rl])
                
    #for d in final_dict: print(d, final_dict[d])
    return final_dict    

def ks_ds_dict_blocks_cols(num_cols, blocks, delimeter):        
    '''
    stores data in lists of cols data structure

    INPUTS
    blocks: list of strings, where each string is all lines in a block (e.g. '1\t100\t500\tA...\n1\t501\t600\G...'
    OUTPUTS
    dictionary of blocks: cols:
        [block1: [col1, col2, ..., colm],
         block2: [col1, col2, ..., colm], 
            ...
         blockn: [col1, col2, ..., colm]]
    
    '''
    header = ['chrm', 'pos', 'start', 'end', 'base']
    final_dict = {block_num: [[] for i in range(num_cols)] for block_num in range(len(blocks))}
    for b in range(len(blocks)):
        rows = blocks[b].split('\n')
        for r in rows:
            rows_list = r.split(delimeter)
            for rl in range(len(rows_list)):
                final_dict[b][rl].append(rows_list[rl])
    
    #for d in final_dict: print(d, final_dict[d])
    return final_dict
 

if __name__ == '__main__':
    main()
