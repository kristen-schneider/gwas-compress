from datetime import datetime

def make_all_blocks(f, block_size, num_columns, delimeter):
    """
    take a list of strings and makes each string a list of columns, where each column is a list of values

    INPUTS
        f = file path to input file
        block_size = number of lines in a block

    OUTPUTS
        all_blocks_list = [[[1,1,1,1,1],[100,200,300,400,500]...],[[2,2,2,2,2],[100,200,300,400,500]...]]]

    """
    string_block_START = datetime.now()
    all_blocks_string = split_into_blocks(f, block_size)
    string_block_END = datetime.now()
    string_block_TIME = string_block_END - string_block_START
    print('file', 'string_block', string_block_TIME)

    all_blocks_list = []
    for b in all_blocks_string:
        curr_block = make_one_block(b, num_columns, delimeter)
        all_blocks_list.append(curr_block)
    return all_blocks_list

def split_into_blocks(f, block_size):
    """
    takes a file and splits into blocks.
    each block is just a long string of lines separated by newline character.

    INPUT
    f = path to input file
    block_size = number of lines to go into a block

    OUTPUT
    blocks = list of strings [block1, block2, ..., blockn]
    """
    reading_data_START = datetime.now()
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
    reading_data_END = datetime.now()
    # reading_data_TIME = 
    # print('file', 'making_blocks'
    return all_blocks

def make_one_block(block_string, num_columns, delimiter):
    """
    takes a single block from split_into_blocks (one long string) and makes it a list of columns

    INPUT
    block_string = block as a string with new line and tab characters
    num_columns = number of columns in file
    block_size = number of lines in a block
    delimiter = file delimiter

    OUTPUT
    one_block = one block as a list
    """

    block_separate_lines = block_string.split('\n')
    block_separate_lines.pop()
    one_block = [[] for i in range(num_columns)]
    
    for i in range(len(block_separate_lines)):
        curr_line = block_separate_lines[i].split(delimiter)
        for v in range(num_columns):
            one_block[v].append(curr_line[v])
    return one_block

