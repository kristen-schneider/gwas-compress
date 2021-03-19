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
    starts beginning of file header

    INPUT
    in_file = input path to orginial gwas file
    block_size = size that we want each block to be (except last)
    
    OUTPUT
    header_start = header for file *so far*
    [magic_number, version_number, delimeter, [col_names], [col_types], num_cols, [end_pos], [block_sizes]]

    '''

    # getting start of header
    header_start = header.get_file_data(in_file, DATA_TYPE_CODE_BOOK)
    
    magic_number = header_start[0]
    version = header_start[1]
    delimeter = header_start[2]
    col_names = header_start[3]
    col_types = header_start[4]
    num_columns = header_start[5]
    
    print(header_start)    
    
    # getting funnel format
    funnel_format = get_funnel_format(in_file, block_size, header_start)
    
    print(funnel_format)

    # compressing/writing data    
    # getting end of header
    
    header_end = compress_and_serialize(funnel_format, block_size, header_start)
    #end_positions = get_end_positions(header_end[0])
    #block_sizes_two = endpos_compresseddata[1]
        
    full_header = header_start + header_end
    return full_header
    #print(full_header)    
    #read_compressed_file(OUT_FILE, full_header)

def get_funnel_format(in_file, block_size, header_start):
    header_end = []
    end_points = []
    block_sizes = []
    
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
    takes a file, converts to funnel format, serializes and compresses each block, write to out_file 
    
    INPUTS
    in_file: path to input file
    block_size = number of lines in each block  
    
    OUTPUTS
    write to file

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
        #print(s_block)
        #print(c_block)
        w_file.write(c_block)
        #all_compressed_data+=c_block

        compressed_block_lengths.append(len(c_block))
    
    w_file.close()    

    # if all blocks are same length, add last block size length
    if len(block_sizes_two) < 2: block_sizes_two.append(block_size)
    
    header_end.append(compressed_block_lengths)
    header_end.append(block_sizes_two)
    return header_end


def get_end_positions(block_lengths):
    '''
    '''
    end = 0
    end_positions = []
    for b in block_lengths:
        end += b
        end_positions.append(end)
    return end_positions            


def read_compressed_file(out_file, full_header):
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
    
    print(block_sizes)
    
    with open(out_file, 'rb') as r_file:
        compressed_data = r_file.read()
    r_file.close
 
    curr_start = 0
    for block_i in range(len(end_positions)):
        if block_i < len(end_positions)-1: curr_block_size = block_sizes[0]
        else: curr_block_size = block_sizes[1]
        curr_end = curr_start + end_positions[block_i]

        curr_bitstring = compressed_data[curr_start:curr_end]
        #print(curr_bitstring)
        dc_bitstring = decompress.decompress_data(curr_bitstring)
        ds_bitstring = deserialize.deserialize_block_bitstring(dc_bitstring, curr_block_size, col_types, BYTE_SIZES)
        print(ds_bitstring)

        curr_start = curr_end


#blengths = [100, 210, 175, 19]
#print(blengths, get_end_positions(blengths))

full_header = main(IN_FILE, BLOCK_SIZE)
read_compressed_file(OUT_FILE, full_header)


##read_decompress_deseralize(IN_FILE, BLOCK_SIZE)
