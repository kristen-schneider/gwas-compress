import gzip
import kristen_format
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
    write_data(ds1)
    
    #write_ds1(ds1)
    #write_ds2(ds2)
    #write_ds3(ds3)
    

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
    for b in all_blocks: print(b)
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
    
    final_dict = {col: ['' for i in range(len(blocks))] for col in header}
    for b in range(len(blocks)):
        rows = blocks[b].split('\n')
        for r in rows:
            rows_list = r.split(delimeter)
            for rl in range(len(rows_list)): 
                final_dict[header[rl]][b] += (rows_list[rl] + '\t')
                #final_dict[header[rl]][b].append(rows_list[rl])
    for d in final_dict: print(d, final_dict[d])
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
    final_dict = {block_num: ['' for i in range(num_cols)] for block_num in range(len(blocks))}
    for b in range(len(blocks)):
        rows = blocks[b].split('\n')
        for r in rows:
            rows_list = r.split(delimeter)
            for rl in range(len(rows_list)):
                final_dict[b][rl] += (rows_list[rl] + '\t')
                #final_dict[b][rl].append(rows_list[rl])
    for d in final_dict: print(d, final_dict[d])
    return final_dict

def write_data(ds):
    # open new gz file
    out_file = open('/Users/kristen/Desktop/compression_sandbox/toy_data/ds_kristen.tsv.gz', 'ab')
    out_file.truncate(0)
    # write to gz file
    for b in ds1:
        for col in b:
            bytes_data = bytes(col, 'utf-8')
            compressed_data = gzip.compress(bytes_data)
            out_file.write(compressed_data)
    out_file.close()


def write_ds1(ds1):
    '''
    take take each element from ds1, convert to bytes, compress, and write to file

    INPUTS
    ds1: list of cols:
        [[col1, col2, ..., coln],[col1, col2, ..., coln], ..., [col1, col2, ..., coln]]
        
        *specifically...*
        list_cols = [block1, block2, ..., blockn]
            block1 = [col1, col2, ..., colm]  
    OUTPUTS
    none. writes to out_file.

    '''
    # open new gz file
    out_file = open('/Users/kristen/Desktop/compression_sandbox/toy_data/ds1.tsv.gz', 'ab')
    out_file.truncate(0) 
    # write to gz file
    for b in ds1:
        for col in b:
            bytes_data = bytes(col, 'utf-8')
            compressed_data = gzip.compress(bytes_data)
            out_file.write(compressed_data)
    out_file.close()

def write_ds2(ds2):
    '''
    take each element from ds2, convert to bytes, compress, and write to file

    INPUTS
    dictionary of cols: blocks:
        [col1:[block1, block2, ..., blockn],
         col2:[block1, block2, ..., blockn], 
            ...
         colm:[block1, block2, ..., blockn]]
    *col1 here might be "chromosome"*
    OUTPUTS
    none. writes to out_file.

    '''
    # open new gz file
    out_file = open('/Users/kristen/Desktop/compression_sandbox/toy_data/ds2.tsv.gz', 'ab')
    out_file.truncate(0)
    # write to gz file
    for c in ds2:
        for b in ds2[c]:
            bytes_data = bytes(b, 'utf-8')
            compressed_data = gzip.compress(bytes_data)
            out_file.write(compressed_data)
    out_file.close()

def write_ds3(ds3):
    '''
    take each element from ds3, convert to bytes, compress, and write to file

    INPUTS
    dictionary of blocks: cols:
        [block1: [col1, col2, ..., colm],
         block2: [col1, col2, ..., colm], 
            ...
         blockn: [col1, col2, ..., colm]]
    OUTPUTS
    none. writes to out_file.

    '''
    # open new gz file
    out_file = open('/Users/kristen/Desktop/compression_sandbox/toy_data/ds3.tsv.gz', 'ab')
    out_file.truncate(0)
    # write to gz file
    for b in ds3:
        for col in ds3[b]:
            bytes_data = bytes(col, 'utf-8')
            compressed_data = gzip.compress(bytes_data)
            out_file.write(compressed_data)
    out_file.close()


    
if __name__ == '__main__':
    main()
