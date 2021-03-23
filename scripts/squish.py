# IMPORTS
import header_generate
import funnel_format

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
    # Magic number, version number, delimiter, column labels, column types, number columns
    # [1,
    # 1,
    # '\t',
    # ['chr', 'pos', 'ref', 'alt', 'af_cases_EUR', 'af_controls_EUR', 'beta_EUR', 'se_EUR', 'pval_EUR', 'low_confidence_EUR'],
    # [1, 1, 3, 3, 2, 2, 2, 2, 2, 3],
    # 10]
    header_start = header_generate.get_header_data(IN_FILE, DATA_TYPE_CODE_BOOK)
    magic_number = header_start[0]
    version = header_start[1]
    delimiter = header_start[2]
    column_labels = header_start[3]
    column_types = header_start[4]
    number_columns = header_start[5]

    # funnel format
    # list of blocks [[block1][block2]...[blockn]]
    # --> a block is a list of columns: block1 = [[col1], [co2]...[colm]]
    # -----> a column is a list of string values: col1 = ['1','1','1','1','1']
    funnel_format_data = funnel_format_data = funnel_format.make_all_blocks(IN_FILE, BLOCK_SIZE, number_columns, delimiter)

    serialize_and_compress_funnel_format(funnel_format_data, column_types)


def serialize_and_compress_funnel_format(ff, column_types):
    header_end = []
    block_end_positions = []    #
    block_header_lengths = []
    block_sizes = []    # should be two elements. one for normal block size. one for last block.

    for block in ff:
        for column in block:
            num_blocks = len(ff)
            block_column_lengths = []







if __name__ == '__main__':
    main()