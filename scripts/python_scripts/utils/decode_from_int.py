from utils import packed_strings

def decode_column_from_int(column_data, decompression_data_type):
    """
    converts a column of type integer to original data type
    """
    og_column = []
    
    if decompression_data_type == 4:
        og_column = packed_strings.decode_int_to_string(column_data)
    # for all others we encode each data point individually as int
    else:
        for data in column_data:
            og_data = convert_data_type_from_int(data, decompression_data_type)
            og_column.append(og_data)
    return og_column

def convert_data_type_from_int(data, decompression_data_type):
    og_data = None
    if decompression_data_type == 1:
        return data
    elif decompression_data_type == 2:
        og_data = int_to_float(data)
    elif decompression_data_type == 3:
        og_data = int_to_TF(data)
    else:
        print('Could not convert from type ', decompression_data_type, ' to int.')
    return og_data

def int_to_float(int_data):
    """
    converts a data type of int to a float
    (for decompressing float columns)

    INPUT
        int_data: data in int form (e.g. 42130050)

    OUTPUT
        int_as_float: data in float form (e.g. 4.213e-05)
    """
    # base, base_sign, exponent, exponent_sign
    # 00000, 0, 00, 0,

    int_as_float = 0
    if int_data == 999:
        # choose a value that is not seen in data
        int_as_float = 'NA'
    else:
        int_as_float = get_float_parts(int_data)
    return int_as_float

def get_float_parts(int_data):
    base = int(int_data/10000)
    decimal_base = float(base/10000)

    leftover = int(int_data-(base*10000))

    base_sign = int(leftover/1000)
    leftover -= base_sign*1000

    exponent = int(leftover/10)
    leftover -= exponent*10

    exponent_sign = leftover

    int_as_float = construct_float(decimal_base, base_sign, exponent, exponent_sign)

    return int_as_float

def construct_float(base, base_sign, exponent, exponent_sign):
    f = round(base, 4)
    if base_sign == 0:
        f *= -1
    if exponent_sign == 0:
        exponent *= -1

    f = base * pow(10, exponent)

    return f


def int_to_TF(data):
    if data == 0: return 'False'
    elif data == 1: return 'True'
    elif data == -1: return 'NA'
    else: return None


# def string_list_to_int(data_list, data_type, column_i):
#     """
#     given a list of string data, return a list of ints
#
#     INPUT
#         data_list: list of strings
#         data_type: 1, 2, 3, or 4 (int, float, str, bytes)
#
#     OUTPUT
#         typed_list: list of ints
#     """
#     typed_list = []
#     if column_i == 2 or column_i == 3:
#         # typed_list = hybrid_strings.encode_column(data_list)
#         typed_list = packed_strings.encode_column(data_list)
#     else:
#         for data in data_list:
#             typed_data = convert_to_int(data, data_type)
#             typed_list.append(typed_data)
#     return typed_list
#
#
# def convert_to_int(data, data_type):
#     """
#     given any data (int, float, string, bytes), converts to integer
#     INPUT
#         data = itput data
#         data_type = original data type
#
#     OUTPUT
#         integer version of data
#     """
#     if data_type == 1:
#         return int_to_int(data)
#     elif data_type == 2:
#         return float_to_int(data)
#     elif data_type == 3:
#         #return data
#         return string_to_int(data)
#     elif data_type == 4:
#         return bytes_to_int(data)
#
# def string_to_int(string_data):
#     """
#     takes string input and converts to integer.
#         false = 0
#         true = 1
#         #A, C, G, T = 2, 3, 4, 5
#         NA = -1
#
#     INPUT
#         string_data = single data value of type string
#
#     OUTPUT
#         int_data = string data converted to integer value according to mapping above.
#     """
#     # A,C,T,G = 2,3,4,5
#     # -2 flags start of indel
#
#     int_data = []
#
#     if len(string_data) > 1:
#         if string_data == 'false':
#             int_data = 0
#         elif string_data == 'true':
#             int_data = 1
#         elif string_data == 'NA':
#             int_data = 2
#         else:
#             return string_data
#         return int_data
#         #else:
#             #for s in string_data:
#             #    int_data.append(single_string_to_int(s))
#     else:
#         return string_data
#         #int_data = single_string_to_int(string_data)
#     return string_data
#
# def single_string_to_int(string_data):
#     """
#     one single string value
#
#     """
#     if string_data == 'A':
#         int_data = 2
#     elif string_data == 'C':
#         int_data = 3
#     elif string_data == 'G':
#         int_data = 4
#     elif string_data == 'T':
#         int_data = 5
#     else:
#         try:
#             int_data = int(string_data)
#         except ValueError:
#             print('cannot convert string to int')
#             return int_data
#     return int_data
#
#
# def bytes_to_int(bytes_data):
#     """
#     given a decompressed, serialized bitstring, convert from bytes to int
#
#     INPUT
#         bytes_data: decompressed, serialized bitstring
#
#     OUTPUT
#         int_data: integer version of input bitstring
#     """
#     int_data = None
#     int_data = int.from_bytes(bytes_data, byteorder='big', signed=False)
#     return int_data

# def int_to_string(i):
#     if i == 0: return 'False'
#     elif i == 1: return 'True'
#     elif i == 2: return 'NA'
#     else:
#         print('cannot convert int to string')
#         return -1

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
