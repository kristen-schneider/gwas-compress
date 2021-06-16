import column_compress
import convert_to_int
from datetime import datetime

def block_compression(compression_style,
                      in_file, block_size, delimiter, num_columns, column_data_types,
                      codecs_list, data_type_byte_sizes):
    """
    opens gwas file and splits into block
    for each block:
        performs according to
    """
    gwas_file = open(in_file, 'r')
    gwas_file_header = ''
    block_line_count = 0
    block = []

    for line in gwas_file:
        # fill header
        if gwas_file_header == '':
            gwas_file_header = line
        # start with data
        else:
            # check to see if block is full size
            if len(block) < block_size:
                block.append(line.rstrip().split(delimiter))
                block_line_count += 1
            elif len(block) == block_size:
                # compress block according to compression style
                if compression_style == 'bgzip_compare':
                    bgzip_compare_compression()
                elif compression_style == 'int_pyfast':
                    int_compression(block, num_columns, column_data_types, codecs_list, data_type_byte_sizes)
                elif compression_style == 'int_mix':
                    int_compression(block, num_columns, column_data_types, codecs_list, data_type_byte_sizes)
                elif compression_style == 'all_mix':
                    all_data_type_compression()
                else:
                    print('invalid compression style')
                    return -1
            else:
                print('block exceed block size.')
                return -1

    gwas_file.close()

def bgzip_compare_compression():
    print('bgzip compare compression')


def int_compression(block, num_columns, column_data_types, codecs_list, data_type_byte_sizes):
    """
    for a block:
        splits into columns
        converts to integers
        compresses column of integers
    """

    # split into columns
    block_as_columns = block_to_columns(block, num_columns)
    # convert column to ints
    block_as_columns_ints = convert_block_to_int(block_as_columns, column_data_types)
    # compress full block
    block_compressed = column_compress.compress_block(num_columns, block_as_columns_ints, codecs_list,
                                                      column_data_types, data_type_byte_sizes)

    return block_compressed


def all_data_type_compression():
    print('all mix compression')


def block_to_columns(block, num_columns):
    """
    takes a block which is a list of rows (a row is a list of column data as strings)
    and formats the block as a list of columns
    """
    block_as_columns = [[] for i in range(num_columns)]
    block_size = len(block)  # do not want to pass in block size parameter bc the last block might not be max size

    # take each column from each row and append to the column-based block
    for row in range(block_size):
        curr_row = block[row]
        for col in range(num_columns):
            block_as_columns[col].append(curr_row[col])
    return block_as_columns

def convert_block_to_int(block_as_columns, column_data_types):
    """
    Takes a list of columns for N rows and converts all columns to integers

    :param block_as_columns:
    :param column_data_types:
    :return:
    """
    block_as_integers = []

    start_time = datetime.now()

    for c in range(len(block_as_columns)):
        column_as_int = convert_to_int.convert_list_to_int(block_as_columns[c], column_data_types[c])
        block_as_integers.append(column_as_int)

    #print('conver to ints: ', datetime.now()-start_time)

    return block_as_integers
