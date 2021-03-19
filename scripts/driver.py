import funnel_format
import header
import serialize
import compress
import decompress
import deserialize


IN_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-tab.tsv'
#IN_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/copy-10-lines-tab.tsv'
OUT_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/kristen-out.tsv'
BLOCK_SIZE = 5

DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3}
BYTE_SIZES = {1: 5, 2: 8, 3: 5}
HEADER_TYPES = {}

def main(in_file, block_size):
    '''
    compresses and writes data and returns full header    

    INPUT
    in_file = input path to orginial gwas file
    block_size = size that we want each block to be (except last)
    
    OUTPUT
    full_header = list of all header data    

    '''

    # getting start of header
    header_start = header.get_file_data(in_file, DATA_TYPE_CODE_BOOK)
    
    magic_number = header_start[0]
    version = header_start[1]
    delimeter = header_start[2]
    col_names = header_start[3]
    col_types = header_start[4]
    num_columns = header_start[5]
    
    # getting funnel format
    funnel_format = get_funnel_format(in_file, block_size, header_start)
    
    # compressing/writing data    
    # getting end of header
    header_end = compress_and_serialize(funnel_format, block_size, header_start)
    
    full_header = header_start + header_end
    return full_header

def get_funnel_format(in_file, block_size, header_start):
    '''
    converts a file into funnel format
    
    INPUT
    in_file = path to original gwas file
    block_size = desired size for all blocks
    header_start = some beginning pieces of header to use for funnel format converstion (e.g. num columns, delimeter)    

    OUTPUT
    funnel_format_data = data in funnel_format        

    '''

    magic_number = header_start[0]
    version = header_start[1]
    delimeter = header_start[2]
    col_names = header_start[3]
    col_types = header_start[4]
    num_columns = header_start[5]

    funnel_format_data = funnel_format.make_all_blocks(in_file, block_size, num_columns, delimeter)
    return funnel_format_data

def compress_and_serialize(funnel_format_data, block_size, header_start):
    '''
    takes funnel format data, serializes and compresses each block, write to out_file 
    returns info which will be added to header (e.g. length of blocks, block sizes, etc.)
    
    INPUTS
    funnel_format_data = data in funnel format
    block_size = number of lines in each block
    header_start = some peices of header which will be used to serialize and compress  
    
    OUTPUTS
    header_end = end parts of header which complete header info

    '''
    num_blocks = len(funnel_format_data)
    header_end = []    

    w_file = open(OUT_FILE, 'wb')
    w_file.truncate(0)
    
    compressed_block_lengths = []
    block_sizes_two = []   # first element = reg block size (equal to input block size), second element for size  of last block
    
    data_types = header_start[4]

    # for each block
        # serialize and compress
        # store size of compressed data
    for b in range(num_blocks):
        curr_block = funnel_format_data[b]
        block_size = len(funnel_format_data[b][0])
        
        # this should only be triggered for first block and last block. 
        if block_size not in block_sizes_two: block_sizes_two.append(block_size)        

        s_block = serialize.serialize_list_columns(curr_block, data_types, BYTE_SIZES)
        c_block = compress.compress_data(s_block, 0)

        # after serialization and compression, print block
        w_file.write(c_block)

        compressed_block_lengths.append(len(c_block))
    
    w_file.close()    

    # if all blocks are same length, add last block size length
    if len(block_sizes_two) < 2: block_sizes_two.append(block_size)
    
    header_end.append(compressed_block_lengths)
    header_end.append(block_sizes_two)
    return header_end


def get_end_positions(block_lengths):
    '''
    converts lengths of blocks to end positions
    
    INPUT
    block_lengths = list of all lengths of compressed blocks

    OUTPUT
    end_positions = list of all end positions of compressed blocks

    '''
    end = 0
    end_positions = []
    for b in block_lengths:
        end += b
        end_positions.append(end)
    return end_positions            


def read_compressed_file(out_file, full_header):
    '''
    reads compressed file and decompresses
    
    INPUT
    out_file = path to compressed file
    full_header = full header!
       
    OUTPUT
    nothing for now...

    '''
    
    #print(header)
    print(type(full_header), full_header)
    magic_number = full_header[0]
    version = full_header[1]
    delimeter = full_header[2]
    col_names = full_header[3]
    col_types = full_header[4]
    num_columns = full_header[5]
    end_positions = full_header[6]
    block_sizes = full_header[7]
    
    with open(out_file, 'rb') as r_file:
        compressed_data = r_file.read()
    r_file.close
 
    curr_start = 0
    for block_i in range(len(end_positions)):
        if block_i < len(end_positions)-1: curr_block_size = block_sizes[0]
        else: curr_block_size = block_sizes[1]
        curr_end = curr_start + end_positions[block_i]

        curr_bitstring = compressed_data[curr_start:curr_end]
        dc_bitstring = decompress.decompress_data(curr_bitstring)
        ds_bitstring = deserialize.deserialize_block_bitstring(dc_bitstring, curr_block_size, col_types, BYTE_SIZES)
        print(ds_bitstring)

        curr_start = curr_end


#blengths = [100, 210, 175, 19]
#print(blengths, get_end_positions(blengths))

full_header = main(IN_FILE, BLOCK_SIZE)
read_compressed_file(OUT_FILE, full_header)


##read_decompress_deseralize(IN_FILE, BLOCK_SIZE)
