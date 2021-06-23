import compress_column
import convert_to_int
import serialize_body
from datetime import datetime

def compress_funnel_format_ints(funnel_format, num_columns, column_data_types, codecs_list, data_type_byte_sizes):
    # to write to
    f = open('./testing_write.txt', 'ab')
    f.truncate(0)

    # for second part of header (to return)
    block_header_end_positions = []
    block_end_positions = []
    block_sizes = []

    block_header_end = 0
    block_end = 0
    for block in funnel_format:
        curr_block_size = len(block[0])
        if curr_block_size not in block_sizes: block_sizes.append(len(block))
        block_header = []
        compressed_block = b''
        column_end_position = 0
        for column_i in range(len(block)):
            curr_column = block[column_i]
            curr_column_data_type = column_data_types[column_i]
            curr_column_codec = codecs_list[column_i]

            # convert column to ints
            column_as_ints = convert_column_to_int(curr_column, curr_column_data_type)

            # compress column
            compressed_column = compress_column_ints(column_as_ints, curr_column_codec, data_type_byte_sizes)

            # add to block header
            column_end_position += len(compressed_column)
            block_header.append(column_end_position)
            # add to compressed block
            compressed_block += compressed_column

        serialized_block_header = serialize_body.serialize_list(block_header, 1, data_type_byte_sizes[1])
        print(serialized_block_header, compressed_block)

        # add to block header end positions
        block_header_end += len(serialized_block_header)
        block_header_end_positions.append(block_header_end)
        # add to block end positions
        block_end += len(compressed_block)
        block_end_positions.append(block_end)
        #f.write(serialized_block_header)
        #f.write(compressed_block)
    f.close()
    print([block_header_end_positions, block_end_positions, block_sizes])
    return [block_header_end_positions, block_end_positions, block_sizes]

def compress_column_ints(column, column_codec, data_type_byte_sizes):
    compressed_column = b''
    col_data_type = 1  # all ints
    col_num_bytes = data_type_byte_sizes[col_data_type]

    # standard compression
    standard_codecs = ['gzip', 'zlib', 'bz2']
    if any(standard_codec in column_codec
           for standard_codec in standard_codecs):
        compressed_column = compress_column.compress_single_column_standard(column, column_codec,
                                                                            col_data_type, col_num_bytes)
    # pyfast
    else:
        compressed_column = compress_column.compress_single_column_pyfast(column, column_codec)

    return compressed_column

def convert_column_to_int(column, column_data_type):
    """
    Takes a columns and converts to integers

    :param column: column as incoming string data
    :param column_data_type: data-type for  column
    :return: column as list of integers
    """
    column_as_ints = []
    column_as_ints = convert_to_int.convert_list_to_int(column, column_data_type)
    return column_as_ints

