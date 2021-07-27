import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from utils import type_handling

def get_header_first_half(in_file, data_type_code_book):
    """
    retrieves some basic header information that should be stored in header up to this point.
        (delimiter, columns names, column types, and column number from the input file)

    INPUT
        in_file = path to input file (original gwas file)

    OUTPUT
        header_first_half = list of information to be included in header.
        << end of header will add information about block locations and size of blocks. >>
    """

    # final header data
    header_first_half = []

    # to be included in header
    magic_number = 1
    version_number = 1
    delimiter = None
    column_names_list = None
    column_types_list = None
    num_columns = None
    gzip_header = None
    zlib_header = None
    bz2_header = None

    # get first two rows which will inform our header data
    row1_row2 = get_first_two_rows(in_file)
    row1_string = row1_row2[0]
    row2_string = row1_row2[1]

    # assign proper data to the pieces of the header
    delimiter = get_delimiter(row1_string)
    column_names_list = get_column_names(row1_string, delimiter)
    column_types_list = type_handling.get_column_types(row2_string.rstrip().split(delimiter))
    num_columns = get_num_columns(column_names_list, column_types_list)
    # gzip_header = get_compression_method_header('gzip')
    # zlib_header = get_compression_method_header('zlib')
    # bz2_header = get_compression_method_header('bz2')

    header_first_half.append(magic_number)
    header_first_half.append(version_number)
    header_first_half.append(delimiter)
    header_first_half.append(column_names_list)
    header_first_half.append(column_types_list)
    header_first_half.append(num_columns)
    # header_first_half.append(gzip_header)
    # header_first_half.append(bz2_header)

    return header_first_half

def get_first_two_rows(in_file):
    """
    returns strings of the first two rows in the file,
    which contain the data that will help construct
    the first half of the header

    INPUT
        in_file: input gwas file

    OUTPUT
        string representations of first two lines in gwas file
        row1_string: header line of gwas file
        row2_string: first line of data in gwas file
    """
    with open(in_file, 'r') as f_open:
        row1_string = f_open.readline()
        row2_string = f_open.readline()
    f_open.close()

    return [row1_string, row2_string]


def get_delimiter(row):
    """
    determine which delimiter is used in the file

    INPUT
        f: path to input file
    OUTPUT
        delimiter: delimiter used in file
    """

    if len(row.split('\t')) > 1: delimiter = '\t'
    elif len(row.split(' ')) > 1: delimiter = ' '
    elif len(row.split(',')) > 1: delimiter = ','
    else:
        print('could not split on delimiter to return a list greater than length 1.')
        return -1
    return delimiter


def get_column_names(row, delimiter):
    """
    gets the header names of each column

    INPUT
        row = first line of the original gwas file, string
        delimiter = file delimiter

    OUTPUT
        column_names = list of all column header names (e.g. [chr, pos, ref, alt, ...])
    """
    column_names = row.rstrip().split(delimiter)
    return column_names


def get_num_columns(column_names_list, column_types_list):
    """
    checks that names and types are same length to return number of columns in a file

    INPUT
        column_names_list = list of header names for columns
        column_types_list = list of data types for columns

    OUTPUT
        num_columns = number of columns
    """
    if (len(column_names_list) == len(column_types_list)):
        num_columns = len(column_names_list)
    else:
        print('row 1 and row 2 have different lengths, exiting.')
        return -1

    return num_columns

