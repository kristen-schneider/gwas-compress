# IMPORTS
import header_generate
import funnel_format
import serialize
import compress

# PARATMETERS
# 1. input file
IN_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-tab.tsv'
    #IN_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/75-lines-tab.tsv'
    #IN_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/copy-10-lines-tab.tsv'
# 2. output file
OUT_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/'
# 3. block size
BLOCK_SIZE = 5
# 4. bytes for each data type
DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3}
DATA_TYPE_BYTE_SIZES = {1: 5, 2: 8, 3: 5}

def main():
    # header_start
    # Magic number, version number, delimiter, column labels, column types, number columns, gzip header
    # [1,
    # 1,
    # '\t',
    # ['chr', 'pos', 'ref', 'alt', 'af_cases_EUR', 'af_controls_EUR', 'beta_EUR', 'se_EUR', 'pval_EUR', 'low_confidence_EUR'],
    # [1, 1, 3, 3, 2, 2, 2, 2, 2, 3],
    # 10,
    # b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff']
    header_start = header_generate.get_header_data(IN_FILE, DATA_TYPE_CODE_BOOK)
    print(header_start)
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
    funnel_format_data = funnel_format_data = funnel_format.make_all_blocks(IN_FILE, BLOCK_SIZE, number_columns, delimiter)

    serialize_and_compress_funnel_format(funnel_format_data, column_types, gzip_header)


def serialize_and_compress_funnel_format(ff, column_types, gzip_header):
    header_end = []             # will contain the following:
    block_end_positions = []    # end positions for each block
    block_header_lengths = []   # lengths of compressed block headers
    block_sizes = []            # should be two elements. one for normal block size. one for last block.

    # prepare output file
    w_file = open(OUT_FILE + 'kristen-' + str(BLOCK_SIZE) + '-out.tsv', 'wb')
    w_file.truncate(0)

    # go through data, and compress each column
    for block_i in range(len(ff)):
        num_blocks = len(ff)

        curr_block = ff[block_i]
        s_c_block = b''
        block_lengths = []
        block_column_lengths = []

        for column_i in range(len(curr_block)):
            curr_column = curr_block[column_i]
            column_type = column_types[column_i]
            column_bytes = DATA_TYPE_BYTE_SIZES[column_type]

            s_column = serialize.serialize_list(curr_column, column_type, column_bytes)
            #s_c_column = compress.compress_data(s_column, 0)

            #block_column_lengths.append(len(c))


        block_lengths.append(len(s_c_block))

#def get_end_positions(block_lengths):







if __name__ == '__main__':
    main()