import funnel_format
import file_header
import serialize
import compress
import decompress
import deserialize


#IN_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-tab.tsv'
IN_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/copy-10-lines-tab.tsv'
OUT_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/kristen-out.tsv'
BLOCK_SIZE = 100
BYTE_SIZES = {int: 5, float: 8, bool: 5, str: 5}

def header_and_compress(in_file, block_size):
    '''
    takes a file, converts to funnel format, serializes and compresses each block, write to out_file 
    
    INPUTS
    in_file: path to input file
    block_size = number of lines in each block  
    
    OUTPUTS
    write to file

    '''
    endpoints_compresseddata = []
    
    # file_info = [delimeter, [col_names], [col_types], num_cols]
    file_info = file_header.get_file_data(IN_FILE)
    delimeter = file_info[0]
    col_names = file_info[1]
    col_types = file_info[2]
    num_columns = file_info[3]

    funnel_format_data = funnel_format.make_all_blocks(IN_FILE, BLOCK_SIZE, num_columns, delimeter)
    #for ff in funnel_format_data: print(ff)
    #print('\n\n')
    num_blocks = len(funnel_format_data)

    compressed_block_sizes = []
    block_size_last = []
    all_compressed_data = b""
    
    # for each block
        # serialize and compress
        # store size of compressed data
    for b in range(num_blocks):
        curr_block = funnel_format_data[b]
        #print(curr_block)
        block_size = len(funnel_format_data[b][0])
        if block_size not in block_size_last: block_size_last.append(block_size)        

        s_block = serialize.serialize_list_columns(curr_block, BYTE_SIZES)
        c_block = compress.compress_data(s_block, 0)
        #print(s_block)
        #print(c_block)
        all_compressed_data+=c_block

        c_block_size = len(c_block)
        compressed_block_sizes.append(c_block_size)
        #dc_block = decompress.decompress_data(c_block)
        #ds_block = deserialize.deserialize_block_bitstring(dc_block, block_size, col_types, BYTE_SIZES)
        #print(ds_block) 
    #blocks = funnel_format.make_all_blocks(IN_FILE, BLOCK_SIZE, NUM_COLUMNS)
    

    #print(all_compressed_data, '\n')        
    if len(block_size_last) < 2: block_size_last.append(block_size)
    endpoints_compresseddata.append(compressed_block_sizes)
    endpoints_compresseddata.append(all_compressed_data)
    endpoints_compresseddata.append(block_size_last)
    return endpoints_compresseddata


def write_compressed_file(in_file, block_size):
    w_file = open(OUT_FILE, 'wb')
    #o_file.truncate(0)
    #file_header = [delimeter, [col_names], [col_types], num_cols, [end_pos], [block_sizes]]
    header = []

    # file_info = [delimeter, [col_names], [col_types], num_cols]
    file_info = file_header.get_file_data(IN_FILE)
    delimeter = file_info[0]
    col_names = file_info[1]
    col_types = file_info[2]
    num_columns = file_info[3]
        
    endpos_compresseddata = header_and_compress(in_file, block_size)
    end_positions = endpos_compresseddata[0]
    compressed_blocks = endpos_compresseddata[1]
    block_size_last = endpos_compresseddata[2]

    print("WRITTEN:\n")
    print(compressed_blocks)

    header = [delimeter, col_names, col_types, num_columns, end_positions, block_size_last]
    w_file.write(compressed_blocks)
    w_file.close()
    return header

def read_compressed_file(out_file, header):
    #print(header)
    delimeter = header[0]
    col_names = header[1]
    col_types = header[2]
    num_cols = header[3]
    end_positions = header[4]
    block_sizes = header[5]

    with open(out_file, 'rb') as r_file:
        compressed_data = r_file.read()
    r_file.close
 
    print("\nREAD:\n")
    print(compressed_data)
     
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


header=write_compressed_file(IN_FILE, BLOCK_SIZE)
read_compressed_file(OUT_FILE, header)
#read_decompress_deseralize(IN_FILE, BLOCK_SIZE)
