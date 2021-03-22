import type_handling
import serialize
import compress
import decompress
import deserialize

# DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3}
BYTE_SIZES = {1: 5, 2: 8, 3: 5}

def get_header_data(in_file, data_type_code_book):
    '''
    retrieves some basic header information that should be stored in header up to this point.
        (delimiter, columns names, column types, and column number from the input file)

    INPUT
    in_file = path to intput file (original gwas file)

    OUTPUT
    header_start = list of information to be included in header (so far). still need to add info about block locations and size of blocks

    '''

    header_start = []

    # to be included in header
    magic_number = 1
    version_number = 1
    delimeter = None
    column_names_list = None
    column_types_list = None
    num_columns = None

    # grab first two rows which will inform our data types, names, lengthts, etc.
    with open(in_file, 'r') as f_open:
        column_names_str = f_open.readline()
        column_types_str = f_open.readline()
    f_open.close()

    # assign
    delimeter = get_delimeter(column_names_str)
    column_names_list = get_column_names(column_names_str, delimeter)
    column_types_list = type_handling.get_column_types(column_types_str.rstrip().split(delimeter), data_type_code_book)
    num_columns = get_num_columns(column_names_list, column_types_list)

    header_start.append(magic_number)
    header_start.append(version_number)
    header_start.append(delimeter)
    header_start.append(column_names_list)
    header_start.append(column_types_list)
    header_start.append(num_columns)

    return header_start


def get_delimeter(row):
    '''
    deterimine which delimeter is used in the file

    INPUT
    f: path to input file
    OUTPUT
    returns delimeter used in file
    '''

    if len(row.split('\t')) > 1:
        delimeter = '\t'
    elif len(row.split(' ')) > 1:
        delimeter = ' '
    elif len(row.split(',')) > 1:
        delimeter = ','
    else:
        return -1

    return delimeter


def get_column_names(row, delimeter):
    '''
    gets the header names of each column

    INPUT
    row = first line of the original gwas file, string
    delimeter = file delimeter

    OUTPUT
    column_names = list of all column header names (e.g. [chr, pos, ref, alt, ...])

    '''

    column_names = row.rstrip().split(delimeter)
    return column_names


def get_num_columns(column_names_list, column_types_list):
    '''
    checks that names and types are same length to return number of columns in a file

    INPUT
    column_names_list = list of header names for columns
    column_types_list = list of data types for columns

    OUTPUT
    num_columns = number of columns

    '''
    if (len(column_names_list) == len(column_types_list)):
        num_columns = len(column_names_list)
    else:
        return -1

    return num_columns


### FOR HEADER COMPRESSION AND DECOMPRESSION ###
def get_header_types(full_header, DATA_TYPE_CODE_BOOK):
    header_types = []
    for h in full_header:
        h_type = type(h[0])
        header_types.append(DATA_TYPE_CODE_BOOK[h_type])
    return header_types


def compress_header(full_header, header_types):
    '''
    '''
    num_columns = full_header[4][0]
    # header_types = [1, 3, 3, 1, 1, 1, 1]
    # header_sizes = [2, 1, num_columms, num_columns, 1, num_columns, 2]
    len_compressed_headers = []
    c_header = b''

    for h in range(len(full_header)):
        # serialize_data([1,1,1,1,1], type_to_bytes_code_book[1], 1)
        s_header = serialize.serialize_data(full_header[h], BYTE_SIZES[header_types[h]], header_types[h])
        curr_c_header = compress.compress_data(s_header, 0)
        c_header += curr_c_header
        len_compressed_headers.append(len(curr_c_header))
    return [c_header, len_compressed_headers, num_columns]


def decompress_header(c_header_info, header_types):
    full_dc_header = []

    c_header = c_header_info[0]
    len_c_headers = c_header_info[1]
    num_columns = c_header_info[2]
    header_sizes = [2, 1, num_columns, num_columns, 1, num_columns, 2]
    # header_types = [1, 3, 3, 1, 1, 1, 1]

    start = 0
    for l in range(len(len_c_headers)):
        curr_len_c_header = len_c_headers[l]
        curr_num_cols_c_header = header_sizes[l]
        curr_data_type_c_header = header_types[l]
        curr_num_bytes_c_header = BYTE_SIZES[curr_data_type_c_header]
        # decompress
        ds_header = decompress.decompress_data(c_header[start:start + curr_len_c_header])
        start += curr_len_c_header

        # deserialize
        # deserialize_data(dc_bitstring, block_size, data_type, num_bytes)
        dc_header = deserialize.deserialize_data(ds_header, curr_num_cols_c_header, curr_data_type_c_header,
                                                 curr_num_bytes_c_header)
        full_dc_header.append(dc_header)

    return full_dc_header

