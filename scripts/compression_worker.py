import column_based_compression
import convert_to_int
import serialize_body
import compress
from datetime import datetime

def block_compression(compression_style,
                      in_file, block_size, delimiter, num_columns, column_data_types,
                      codecs_list, data_type_byte_sizes, out_file):
    """
    opens gwas file and splits into block
    for each block:
        performs splits and compression according to compression style

    :param compression_style: specifies how we handle data and (block compression vs column compression, ints vs. all)
    :param in_file: input gwas file
    :param block_size: input size of block (how many lines per block)
    :param delimiter: for input gwas file
    :param num_columns: for input gwas file
    :param column_data_types: for input gwas file
    :param codecs_list: list of codecs for each column
    :param data_type_byte_sizes: dictionary for byte sizes for each data type
    """
    # prepare space for end of header information
    end_block_headers_list = []
    end_block_headers_value = 0
    end_blocks_list = []
    end_blocks_value = 0
    size_of_last_block = -1

    # open output file and clear it if data already written
    f = open('./testing_write.txt', 'ab')
    f.truncate(0)
    f.close()
    # o = open(out_file, 'ab')
    # o.truncate(0)
    # o.close()

    # open file and prepare space for compressed data
    gwas_file = open(in_file, 'r')
    gwas_file_header = ''
    block_line_count = 0
    block = []

    # go through gwas file, line by line
    # establish block
    # compress block according to compression type
    for line in gwas_file:
        # fill header
        if gwas_file_header == '':
            gwas_file_header = line
        # start with data
        else:
            # if block is not full size, add line to block
            if len(block) < block_size:
                block.append(line.rstrip().split(delimiter))
                block_line_count += 1
            # if block is full size, compress block
            elif len(block) == block_size:
                # compress block according to compression style
                # compression style should be data type, block/col
                if 'int' in compression_style:
                    compressed_block_info = int_compression(block, num_columns, column_data_types,
                                                            codecs_list, data_type_byte_sizes)
                elif 'all' in compression_style:
                    compressed_block_info = all_data_type_compression()

                # compress block header
                block_header = compressed_block_info[0]
                block_header_data_type = 1 # ints only
                block_header_bytes = data_type_byte_sizes[block_header_data_type]
                serialized_block_header = serialize_body.serialize_list(block_header,
                                                                        block_header_data_type,
                                                                        block_header_bytes)
                compressed_block_header = compress.compress_bitstring('gzip', serialized_block_header)
                compressed_block = compressed_block_info[1]

                # fill end of header information
                end_block_headers_value += len(compressed_block_header)
                end_block_headers_list.append(end_block_headers_value)
                end_blocks_value += (len(compressed_block_header)+len(compressed_block_info[1]))
                end_blocks_list.append(end_blocks_value)
                size_of_last_block = len(block)

                # write block header and compressed block
                f = open('./testing_write.txt', 'ab')
                f.write(compressed_block_header)
                f.write(compressed_block)
                f.close()

                # reset block information
                block = []
                block.append(line.rstrip().split(delimiter))
                block_line_count += 1

            # block is not less than block size or equal to block size.
            else:
                print('block exceed block size.')
                return -1

    # at end of file, consider the last block, however long it is
    if len(block) > 0:
        # compress block according to compression style
        # block-based compression
        if compression_style == 'bgzip_compare':
            bgzip_compare_compression()

        # column-based compression
        # Integer types
        elif 'int' in compression_style:
            compressed_block_info = int_compression(block, num_columns, column_data_types, codecs_list,
                                                    data_type_byte_sizes)
        # all data types
        elif 'all' in compression_style:
            all_data_type_compression()
        else:
            print('invalid compression style')
            return -1

        # compress block header
        serialized_block_header = serialize_body.serialize_list(compressed_block_info[0],
                                                                1, data_type_byte_sizes[1])
        compressed_block_header = compress.compress_bitstring('gzip', serialized_block_header)
        compressed_block = compressed_block_info[1]
        # fill end of header information
        end_block_headers_value += len(compressed_block_header)
        end_block_headers_list.append(end_block_headers_value)
        end_blocks_value += len(compressed_block_info[1])
        end_blocks_list.append(end_blocks_value)
        size_of_last_block = len(block)

        # write block header and compressed block
        f = open('./testing_write.txt', 'ab')
        f.write(compressed_block_header)
        f.write(compressed_block)
        f.close()
        # o = open(out_file, 'ab')
        # o.write(compressed_block_header)
        # o.write(compressed_block_info[1])
        # o.close()

    gwas_file.close()

    end_of_header = [end_block_headers_list, end_blocks_list, [block_size,size_of_last_block]]
    return end_of_header

def bgzip_compare_compression():
    """

    """
    print('bgzip compare compression')


def int_compression(block, num_columns, column_data_types, codecs_list, data_type_byte_sizes):
    """
    for a block:
        splits into columns
        converts to integers
        compresses column of integers

    :param block: block as list of integer columns
    :param num_columns: number of columns in each block
    :param column_data_types: data types for each column
    :param codecs_list: list of codecs for each column
    :param data_type_byte_sizes: dictionary for byte sizes for each data type
    :return block_compressed: list of lengths for compressed columns, compressed block (excluding compression header)
    """

    # split into columns
    block_as_columns = block_to_columns(block, num_columns)
    # convert column to ints
    block_as_columns_ints = convert_block_to_int(block_as_columns, column_data_types)
    # compress full block
    new_column_data_types = [1]*num_columns
    block_compressed = column_based_compression.compress_block(num_columns, block_as_columns_ints, codecs_list,
                                                               new_column_data_types, data_type_byte_sizes)

    return block_compressed


def all_data_type_compression():
    print('all mix compression')

def block_to_columns(block, num_columns):
    """
    takes a block which is a list of rows (a row is a list of column data as strings)
    and formats the block as a list of columns

    :param block: block as list of rows
    :param num_columns: number of columns in block
    :return block_as_columns: block as list of columns
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

    :param block_as_columns: block as list of columns
    :param column_data_types: list of data-types for each column
    :return: block as list of integers
    """
    block_as_integers = []

    start_time = datetime.now()

    for c in range(len(block_as_columns)):
        column_as_int = convert_to_int.convert_list_to_int(block_as_columns[c], column_data_types[c])
        block_as_integers.append(column_as_int)

    #print('conver to ints: ', datetime.now()-start_time)

    return block_as_integers

