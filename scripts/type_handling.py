import numpy as np


def get_column_types(row, data_type_code_book):
    """
    Given a row of data, returns all the types of data in that row
    Data types are according to code_book

    INPUT
        row = list of data that we see in a row (e.g. ['1', 'A', ...]

    OUTPUT
        data_types_list = list of data types witnessed in that row (e.g. [1, 2, 2, 1, 1...])
    """

    data_types_list = []
    for r in row:
        data_type = get_data_type(r, data_type_code_book)
        data_types_list.append(data_type)
    return data_types_list


def get_data_type(str_data, data_type_code_book):
    """
    Returns proper data type of incoming data. This is used only once for a the first row.
    Most data is read in as a string. this will try and discern if it is actually an integer/float.
    We use a dictionary/code book to label each type because we cannot pass types as parameters.

    INPUT
        data = incoming data. likely to be read in as string
    OUTPUT
        data_type = int, float, or str
    """

    # hierarchy: int, float, string
    try:
        int(str_data)
        return data_type_code_book[int]
    except ValueError:
        try:
            float(str_data)
            return data_type_code_book[float]
        except ValueError:
            try:
                str(str_data)
                return data_type_code_book[str]
            except ValueError:
                print('could not detect data type as int, float, or string')
                return type(str_data)


def string_list_to_int(data_list, data_type):
    """
    given a list of string data, return a list of ints

    INPUT
        data_list: list of strings
        data_type: 1, 2, 3, or 4 (int, float, str, bytes)

    OUTPUT
        typed_list: list of ints
    """
    typed_list = []
    for data in data_list:
        typed_data = convert_to_int(data, data_type)
        typed_list.append(typed_data)
    return typed_list


def convert_to_int(data, data_type):
    """
    given any data (int, float, string, bytes), converts to integer
    INPUT
        data = itput data
        data_type = original data type

    OUTPUT
        integer version of data
    """
    if data_type == 1:
        return int(data)
    elif data_type == 2:
        return float_to_int(data)
    elif data_type == 3:
        return string_to_int(data)
    elif data_type == 4:
        return bytes_to_int(data)


def float_to_int(float_data):
    """
    converts a data type of float to a list of integers which can reconstruct the float

    INPUT
        float_data: data in float form (e.g. 4.213e-05)

    OUTPUT
        int_data: list [base, exponent];
            where base is the float number without the decimal
            and exponent is the signed value after 'e'
    """
    if float_data == 'NA':
        # choose a value that is not seen in data
        int_data = [0, -999]
    else:
        # split on base and exponent and create a list [base, exponent]
        base_exponent = float_data.split('e')
        base = base_exponent[0]
        exponent = int(base_exponent[1])
        whole_decimal = int(''.join(base.split('.')))
        int_data = [whole_decimal, exponent]
    return int_data


def string_to_int(string_data):
    """
    takes string input and converts to integer.
        false = 0
        true = 1
        A, C, G, T = 2, 3, 4, 5
        chromosome x = 23
        chromosome y = 24

    INPUT
        string_data = single data value of type string

    OUTPUT
        int_data = string data converted to integer value according to mapping above.
    """
    # (22 integer chromosomes, x and y)
    # A,C,T,G = 2,3,4,5

    int_data = None

    if string_data == 'false':
        int_data = 0
    elif string_data == 'true':
        int_data = 1
    elif string_data == 'A':
        int_data = 2
    elif string_data == 'C':
        int_data = 3
    elif string_data == 'G':
        int_data = 4
    elif string_data == 'T':
        int_data = 5
    elif string_data == 'X':
        int_data = 23
    elif string_data == 'Y':
        int_data = 24
    else:
        try:
            int_data = int(string_data)
        except ValueError:
            print('cannot convert string to int')
            return int_data

    return int_data


def bytes_to_int(bytes_data):
    """
    given a decompressed, serialized bitstring, convert from bytes to int

    INPUT
        bytes_data: decompressed, serialized bitstring

    OUTPUT
        int_data: integer version of input bitstring
    """
    int_data = None
    int_data = int.from_bytes(bytes_data, byteorder='big', signed=False)
    return int_data


# # old functionality not used now that we convert everything to ints.
# def convert_to_type(column_data, data_type):
#     """
#     converts a list of values in a column of some data types into a list values in some column of new data_types
#
#     INPUT
#         column_data = list of data (e.g. ['1','1','1','1','1']
#         data_type = type to which we want to convert (e.g. int)
#         data_type_code_book = code book which converts
#
#     OUTPUT
#         correct_type_column = new list with correct type (e.g. [1,1,1,1,1])
#
#     """
#     correct_type_column = []
#
#     for c in column_data:
#         if data_type == 1:
#             # try to convert to integer.
#             try:
#                 correct_type_column.append(int(c))
#             except ValueError:
#                 # for chromosome X,Y values
#                 try:
#                     if 'X' in c or 'Y' in c:
#                         correct_type_column.append(str(c))
#                     else:
#                         print('cannot convert to integer: ', c)
#                 except ValueError:
#                     print('cannot convert to integer: ', c)
#         elif data_type == 2:
#             # try to convert to float, if cannot, return numpy's nan mask
#             try:
#                 correct_type_column.append(float(c))
#             except ValueError:
#                 correct_type_column.append(np.nan)
#         elif data_type == 3:
#             # try to convert to string.
#             try:
#                 correct_type_column.append(str(c))
#             except ValueError:
#                 print('cannot convert to string: ', c)
#         else:
#             print('could not convert data type to int, float, or string')
#             return -1
#
#     return correct_type_column
#
#
# def get_bitstring_length_by_data_type(block_size, data_type, num_bytes):
#     '''
#     returns the the lengths of a bitstring of given data type, bytes, and original number of elements
#
#     INPUTS
#         block_size = number of rows present in a block
#         data_type = type of data to be represented in the bitstring (e.g. [1,1,1,1,1] = int
#         num_bytes = number of bytes we are using to be represented in this bitstring
#
#     OUTPUTS
#         len_bitsring = this will return the length of a bitstring that should represent one column only
#
#     '''
#     if data_type == 1:
#         bitstring_length = block_size * num_bytes
#     elif data_type == 2:
#         bitstring_length = block_size * num_bytes
#     elif data_type == 3:
#         bitstring_length = block_size
#     else:
#         print('data is not of type int, float, or string')
#         bitstring_length = -1
#     return bitstring_length
