def serialize_list(in_list, data_type, num_bytes):
    """
    serializes a list of data type integers, according to their original type

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
        s_value = serialize_string(data, num_bytes)
    else:
        s_value = data
    return s_value


def serialize_int(data, num_bytes):
    """
    integer columns are 1 and 2: chrm and pos
    special cases with X and Y values.

    INPUT
        data: incoming data value
        num_bytes: number of bytes used to serialize for a given data_type

    OUTPUT
        s_value: serialized integer value
    """
    s_value = data.to_bytes(num_bytes, byteorder='big', signed=True)
    return s_value

def serialize_float(data, num_bytes):
    """
        integer columns are 1 and 2:
            chrm-data values 1-24
                *special cases with X and Y values.
            pos-data values in thousands and up
        INPUT
            data: incoming data value
            num_bytes: number of bytes used to serialize for a given data_type

        OUTPUT
            s_value: serialized integer value
        """
    s_value = data.to_bytes(num_bytes, byteorder='big', signed=True)
    return s_value

def serialize_string(data, num_bytes):
    """
    converts string data to serialized data

    INPUT
        data: integer values representing string data

    OUTPUT
        s_value: serialized value representing string data
    """
    s_bitstring = b''
    indel_flag = -2
    s_indel_flag = serialize_int(indel_flag, num_bytes)
    s_bitstring+=s_indel_flag
    # INDEL
    if type(data) == list:
        for i in data:
            s_value = serialize_int(i, num_bytes)
            s_bitstring += s_value
        s_bitstring += s_indel_flag
    # SNP
    elif type(data) == int:
        s_value = serialize_int(data, num_bytes)
        s_bitstring += s_value

    return s_bitstring


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
