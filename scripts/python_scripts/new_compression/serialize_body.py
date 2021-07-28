def serialize_list(in_list, data_type, num_bytes):
    """
    serializes a list of data according to their data type

    INPUT
        in_list: incoming list of integer values
        data_type: original data type value
        num_bytes: number of bytes used to serialize for a given data_type

    OUPUT
        s_bitstring = serialized bitstring
    """
    s_bitstring = b''
    s_value = None
    
    for i in in_list:
        s_value = serialize_data(i, data_type, num_bytes)
        try:
            s_bitstring += s_value
        except TypeError:
            print('cannot concat s_value to bitstring: ', i, s_value)
    return s_bitstring

def serialize_data(data, data_type, num_bytes):
    """
    serializes a single piece of data according to its data type

    INPUT
        data: incoming data value
        data_type: data type of data
        num_bytes: number of bytes used to serialize for a given data_type

    OUTPUT
        s_value: serialized data
    """
    s_value = None
    # ints
    if data_type == 1:
        s_value = serialize_int(data, num_bytes)
    # floats
    elif data_type == 2:
        s_value = serialize_float(data, num_bytes)
    # strings
    elif data_type == 3:
        s_value = serialize_string(data)
        # string value converted to int
        if s_value == -1:
            s_value = serialize_int(data, num_bytes)
    else:
        s_value = data
    return s_value


def serialize_int(data, num_bytes):
    """

    INPUT
        data: incoming data value
        num_bytes: number of bytes used to serialize for a given data_type

    OUTPUT
        s_value: serialized integer value
    """
    try:
        s_value = data.to_bytes(num_bytes, byteorder='big', signed=True)
    # numpy data is not integer
    except AttributeError: 
        s_value = data.tobytes(order='C')
    except OverflowError:
        return -1
    return s_value

def serialize_float(data, num_bytes):
    """
        float columns are 4, 5, 6, 7, 8
        INPUT
            data: incoming data value
            num_bytes: number of bytes used to serialize for a given data_type

        OUTPUT
            s_value: serialized integer value
        """
    try:
        s_value = data.to_bytes(num_bytes, byteorder='big', signed=True)
    # numpy data is not integer
    except AttributeError: 
        s_value = data.tobytes(order='C')
    return s_value

def serialize_string(data):
    """
    converts string data to serialized data.
    pads a string with more than one character with
     leading and trailing zeros to indicate beginning and end of string

    INPUT:
        data: string data

    OUTPUT:
        s_value: serialized string data
    """
    # single string value (e.g. 'H')
    try:
        s_value = bytes(data, 'utf-8')
        if len(s_value) > 1:
            s_value = b'\0'+s_value+b'\0'
    except TypeError: return -1
    return s_value


# def serialize_list(in_list, data_type, num_bytes):
#     """
#     INPUT
#         one_column = list type, represents one column (e.g. [1,1,1,1,1])
#         num_bytes = number of bytes needed to store each value in the column
#         data_type = data type of column (1, 2, 3)
#
#     OUTPUT
#         s_bitstring = serialized bitstring (bytes object) of list from input
#     """
#     s_bitstring = b''
#     s_value = None
#     for i in in_list:
#         s_value = serialize_data(i, data_type, num_bytes)
#
#         # we have more than one string "AAA"
#         if s_value != None:
#             # special exception for strings:
#             if data_type != 3:
#                 s_bitstring += s_value
#             elif data_type == 3:
#                 if len(s_value) > 1:
#                     s_bitstring += b'\0'+s_value+b'\0'
#                 else:
#                     s_bitstring += s_value
#             else: print('value is of bad type, cannot serialize')
#         else: print('value is of bad type, cannot serialize')
#     return s_bitstring
#
# def serialize_data(data, data_type, num_bytes):
#     # integers
#     s_value = None
#     if data_type == 1:
#         try:
#             s_value = data.to_bytes(num_bytes, byteorder='big', signed=True)
#         except AttributeError:
#             if type(data) != int:
#                 # data coming in from codec compression/numpy array
#                 data = int(data)
#                 try: s_value = data.to_bytes(num_bytes, byteorder='big', signed=True)
#                 except AttributeError:
#                     if 'X' in data or 'Y' in data:
#                         try:
#                             s_value = bytes(data, 'utf-8')
#                         except AttributeError:
#                             return -1
#                     else:
#                         print('cannot convert ' + str(data), ' to int')
#                         return -1
#             # for chromosome X,Y values
#             elif 'X' in data or 'Y' in data:
#                 try:
#                     s_value = bytes(data, 'utf-8')
#                 except AttributeError:
#                     return -1
#             else:
#                 print('cannot convert '+str(data), ' to int')
#                 return -1
#     # floats
#     elif data_type == 2:
#         try:
#             s_value = struct.pack(">d", data)
#         except AttributeError:
#             print('cannot convert ' + str(data), ' to float')
#             return -1
#     # strings
#     elif data_type == 3:
#         try:
#             s_value = bytes(data, 'utf-8')
#         except AttributeError:
#             print('cannot convert ' + str(data), ' to str')
#             return -1
#
#     # bytes (used for header, gzip_header
#     elif data_type == 4:
#         s_value = data
#     return s_value
