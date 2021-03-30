# IMPORTS
import sys
from datetime import datetime
import header_generate
import funnel_format
import type_handling
import serialize
import compress
import header_compress_decompress

# PARATMETERS
# 1. input file
IN_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-tab.tsv'
#IN_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/15.tsv'
#IN_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/copy-10-lines-tab.tsv'
# FIJI
#IN_FILE = '/scratch/Users/krsc0813/gwas-compress/data/test-gwas-data/test.tsv'
#IN_FILE = '/scratch/Users/krsc0813/gwas-compress/data/test-gwas-data/big_test.tsv'
#IN_FILE = '/scratch/Users/krsc0813/gwas-compress/data/full-gwas-data/prescriptions-thiamine-both_sexes_copy.tsv'

# 2. output file
OUT_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/'
# FIJI
#OUT_FILE = '/scratch/Users/krsc0813/gwas-compress/data/compressed/'
# 3. block size
BLOCK_SIZE = int(sys.argv[1])
#BLOCK_SIZE = 100000
# 4. bytes for each data type
DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes:4}
DATA_TYPE_BYTE_SIZES = {1: 5, 2: 8, 3: 5, 4:None}

def main():

    full_header = get_full_header()
    serialized_header_tools = header_compress_decompress.full_header_tools(full_header)

    serialized_header_types = serialized_header_tools[1]
    serialized_header_num_elements = serialized_header_tools[1]
    serialized_header_ends = serialized_header_tools[2]
    serialized_header_data = serialized_header_tools[3]

    size_types = len(serialized_header_types)
    bytes_size_types = size_types.to_bytes(2, byteorder='big', signed=False)
    size_ends = len(serialized_header_ends)
    bytes_size_ends = size_ends.to_bytes(2, byteorder='big', signed=False)
    size_data = len(serialized_header_data)
    bytes_size_data = size_data.to_bytes(2, byteorder='big', signed=False)

    # writing header
    with open(OUT_FILE + 'kristen-' + str(BLOCK_SIZE) + '-out.tsv', 'rb') as compressed_file:
        all_content = compressed_file.read()
    compressed_file.close()

    compressed_with_header = open(OUT_FILE + 'kristen-' + str(BLOCK_SIZE) + '-out.tsv', 'wb')
    # write how many bytes are needed to store types, ends, and data (CONSTANT FIRST 4 BYTES)
    compressed_with_header.write(bytes_size_types)
    compressed_with_header.write(bytes_size_ends)
    compressed_with_header.write(bytes_size_data)

    # write header types and header ends (serilized)
    compressed_with_header.write(serialized_header_types)
    compressed_with_header.write(serialized_header_ends)

    # write header (serialized)
    compressed_with_header.write(serialized_header_data)

    # write contents of file (all compressed blocks)
    compressed_with_header.write(all_content)


def get_full_header():
    # header_start
    # Magic number, version number, delimiter, column labels, column types, number columns, gzip header
    # [1,
    # 1,
    # '\t',
    # ['chr', 'pos', 'ref', 'alt', 'af_cases_EUR', 'af_controls_EUR', 'beta_EUR', 'se_EUR', 'pval_EUR', 'low_confidence_EUR'],
    # [1, 1, 3, 3, 2, 2, 2, 2, 2, 3],
    # 10,
    # b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff']
    print('generating start of header...')
    header_start_START = datetime.now()
    header_start = header_generate.get_header_data(IN_FILE, DATA_TYPE_CODE_BOOK)
    header_start_END = datetime.now()
    header_start_TIME = header_start_END-header_start_START
    print(str(header_start_TIME) + ' for header start to compute...\n')

    magic_number = header_start[0]
    version = header_start[1]
    delimiter = header_start[2]
    column_labels = header_start[3]
    column_types = header_start[4]
    number_columns = header_start[5]
    gzip_header = header_start[6]

    # funnel format
    # list of blocks [[block1][block2]...[blockn]]
    # --> a block is a list of columns: block1 = [[col1], [co2]...[colm]]
    # -----> a column is a list of string values: col1 = ['1','1','1','1','1']
    print('generating funnel format...')
    funnel_format_START = datetime.now()
    funnel_format_data = funnel_format.make_all_blocks(IN_FILE, BLOCK_SIZE, number_columns, delimiter)
    funnel_format_END = datetime.now()
    funnel_format_TIME = funnel_format_END - funnel_format_START
    print(str(funnel_format_TIME) + ' for funnel format to compute...\n')

    print('compressing data...')
    header_end_START = datetime.now()
    header_end = serialize_and_compress_funnel_format(funnel_format_data, column_types)
    header_end_END = datetime.now()
    header_end_TIME = header_end_END - header_end_START
    print(str(header_end_TIME) + ' for full compression to complete...\n')

    full_header = header_start+header_end

    print('FULL HEADER:')
    print(full_header)

    # w_file = open(OUT_FILE + 'kristen-' + str(BLOCK_SIZE) + '-out.tsv', 'ab')
    # full_header_types = header_compress_decompress.get_header_types(full_header, DATA_TYPE_CODE_BOOK)
    # c_s_full_header = header_compress_decompress.compress_header(full_header, full_header_types)[1]
    # w_file.write(c_s_full_header)
    # w_file.close()
    return full_header


def serialize_and_compress_funnel_format(ff, column_types):
    header_end = [] # last half of header
    #block_header_lengths = []   # lengths of compressed block headers
    block_header_end_positions = [] # end  positions of compressed blocks
    block_end_positions = []
    block_sizes = []            # should be two elements. one for normal block size. one for last block.

    # prepare output file
    w_file = open(OUT_FILE + 'kristen-' + str(BLOCK_SIZE) + '-out.tsv', 'ab')
    w_file.truncate(0)

    header_end_value = 0
    block_end_value = 0
    block_length = 0
    # go through data, and compress each column
    for block_i in range(len(ff)):
        print('block' + str(block_i))
        block_i_START = datetime.now()

        num_rows_in_block = len(ff[block_i][0])

        curr_block = ff[block_i]
        compressed_block = b''

        block_column_ends = []
        curr_compressed_column_end = 0
        for column_i in range(len(curr_block)):

            # get column info
            curr_column = curr_block[column_i]
            column_type = column_types[column_i]
            typed_column = type_handling.convert_to_type(curr_column, column_type)
            column_bytes = DATA_TYPE_BYTE_SIZES[column_type]

            # serialize and compress a column
            s_column = serialize.serialize_list(typed_column, column_type, column_bytes)
            s_c_column = compress.compress_data(s_column, 0)[10:] # remove the gzip header bit from the compressed data
            compressed_block += s_c_column

            # add length of this column to lengths of columns in this block
            curr_compressed_column_end +=len(s_c_column)
            block_column_ends.append(curr_compressed_column_end)


        # this should only be triggered for first block and last block.
        if num_rows_in_block not in block_sizes:
            block_sizes.append(num_rows_in_block)

        # write the compressed block header and compressed block to the file
        s_block_header = serialize.serialize_list(block_column_ends, 1, DATA_TYPE_BYTE_SIZES[1])
        s_c_block_header = compress.compress_data(s_block_header, 0)[10:]

        header_length = len(s_c_block_header)


        header_end_value += (header_length + block_length)
        block_header_end_positions.append(header_end_value)

        block_length = len(compressed_block)

        block_end_value += (header_length+block_length)
        block_end_positions.append(block_end_value)


        # print('header', len(s_c_block_header), s_c_block_header)
        w_file.write(s_c_block_header)
        # print('data', len(compressed_block), compressed_block)
        w_file.write(compressed_block)

        block_i_END = datetime.now()
        block_i_TIME = block_i_END - block_i_START
        print(str(block_i_TIME) + ' for block ' + str(block_i) + ' to compress and write...\n')

        #block_end_positions = header_generate.get_block_end_positions(block_lengths, block_header_lengths)
    if len(block_sizes) < 2: block_sizes.append(num_rows_in_block)

    header_end.append(block_header_end_positions)
    header_end.append(block_end_positions)
    header_end.append(block_sizes)

    w_file.close()
    return header_end


if __name__ == '__main__':
    main()
