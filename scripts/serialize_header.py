"""
when we convert all data to itegers, serialization of strings
will work differently for header and for data.
header strings will not be converted to integers.
"""
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
        s_bitstring += s_value
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
        s_value = serialize_int_float(data, num_bytes)
    # floats
    elif data_type == 2:
        s_value = serialize_int_float(data, num_bytes)
    # strings
    elif data_type == 3:
        s_value == serialize_string(data)
    else:
        print('cannot serialize this data type: ', data_type)
    return s_value

def serialize_int_float(data, num_bytes):
    """
    header data with integers and floats should have straight forward serialization.

    INPUT:
        data: single integer or float data
        num_bytes: number of bytes used for an integer or a float

    OUTPUT:
        s_value: serialized integer or float data
    """
    s_value = data.to_bytes(num_bytes, byteorder='big', signed=False)
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
    s_value = bytes(data, 'utf-8')
    if len(s_value) > 1:
        s_value = b'\0'+s_value+b'\0'
    return s_value
