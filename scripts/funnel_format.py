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
    print('...converting to funnel format...')
    
    # delimeters
    tab_d = determine_delimeter(TAB_FILE)
    comma_d = determine_delimeter(COMMA_FILE)
    space_d = determine_delimeter(SPACE_FILE)
    # header
    header = get_header(TAB_FILE, tab_d)
    
    #chromosome format
    chr_flag = get_chr_format(TAB_FILE, header, tab_d)
    blocks = make_blocks(TAB_FILE, BLOCK_SIZE)
    
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
        if len(header.split('\t')) > 1: delimeter = '\t'
        elif len(header.split(' ')) > 1: delimeter = ' '
        elif len(header.split(',')) > 1: delimeter = ','
    
    f_open.close()
    return delimeter

def get_header(f, delimeter):
    '''
    stores a list which is the header of the file, so that we know what columns are included and need be stored
    
    INPUTS
    f = path to uncompressed input file
    OUTPUTS
    header = list of the first row of the file

    '''
    with open(f, 'r') as f_open:
        header = f_open.readline().rstrip().split(delimeter)
    
    f_open.close()
    return header

def get_chr_format(f, header, delimeter):
    '''
    looking to see how the first column (chr) is formatted
         
    INPUTS
    f = path to uncompressed input file
    OUTPUTS
    1 if chr is in front of the chromosomee number/character
    0 if only the chromosome number/character is present
    None otherwise
   
    '''    

    chr_flag = None
    with open(f, 'r') as f_open:
        # reads one line for header and one to get to data
        h = f_open.readline()
        first_data = f_open.readline().rstrip().split(delimeter)
        try: 
            chr_index = header.index('chr')
            chr_format = first_data[chr_index]
            if 'chr' in chr_format or 'chrm' in chr_format: chr_flag = 1
            else: chr_flag = 0
        except ValueError:
            try:
                chr_index = header.index('chrm')
                chr_format = first_data[chr_index]
                if 'chr' in chr_format or 'chrm' in chr_format: chr_flag = 1
                else: chr_flag = 0
            except ValueError:
                chr_flag = None
                print('VAL_ERROR: cannot find chromosome column to determine format of entries')
    
    f_open.close()        
    return chr_flag
 
def split_into_blocks(f, block_size):
    '''
    takes a file and splits into blocks. each block is just a long string of lines separated by newline character.

    INPUTS
    f = path to input file
    block_size = number of lines to go into a block
    OUTPUTS
    blocks = list of strings [block1, block2, ..., blockn]

    '''
    # initialize 
    all_blocks = []    
    header = None
    curr_block = ''
    line_count = 0
 
    f_open = open(f, 'r')
    for line in f_open:
        if header == None: header = line
        else:   
            if line_count < block_size:
                curr_block += line
                line_count += 1
            else:
                all_blocks.append(curr_block)
                curr_block = line
                line_count = 1
    
    all_blocks.append(curr_block)
        
    f_open.close()
    return all_blocks

def make_one_block(block_string, delimeter):
    '''
    takes a single block from split_into_blocks (one long string) and makes it a list of columns
    
    INPUTS
    block_string = block as a string with new line and tab characters
    OUTPUTS
    one_block = one block as a list
    
    '''



def make_all_blocks(f, block_size):
    '''
    take a list of strings and makes each string a list of columns, where each column is a list of values
    
    INPUTS
    f = file path to input file 
    block_size = number of lines in a block
    OUTPUTS
    all_blocks_list = [[[1,1,1,1,1],[100,200,300,400,500]...],[[2,2,2,2,2],[100,200,300,400,500]...]]]

    '''
    delimeter = determine_delimeter(f)
    all_blocks_string = split_into_blocks(f, block_size)

    all_blocks_list = []
    for b in all_blocks_string:
        curr_block = make_one_block(b, delimeter)
        all_blocks_list.append(curr_block)
    return all_blocks_list

#def make_block(f, block_size, delimeter):
#    '''
#    splits a file into blocks
#
#    INPUTS
#    f = path to input file
#    block_size = number of lines per block
#    OUTPUTS
#    a list of all blocks. one block is a list of columns. (e.g. [[1,1,1,1,1],[100,200,300,400,500],['A', 'C', 'T', 'G', 'A'], ...)
#
#    '''
#    # initialize variables
#    all_blocks = []    
#    header = None
#    curr_block = []
#    line_count_per_block = 0
#    
#    f_open = open(f, 'r')
#    for line in f_open:
#        # grab header
#        if header == None: header = line.rstrip().split(delimeter)
#        # add new block every 'block_size' lines
#        else:
#            if line_count_per_block < block_size:
#                
#                curr_block.append(line.rstrip().split(delimeter)
#                line_count_per_block += 1
#            else:
#                all_blocks.append(curr_block.rstrip())
#                curr_block = line
#                line_count_per_block = 1
#    all_blocks.append(curr_block.rstrip())
#    f_open.close()
#    return all_blocks
            
if __name__ == '__main__':
    main()
