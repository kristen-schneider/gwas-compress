import float_int
import string_int

def convert_list_from_int(int_list, data_type):
    list_as_type = []
    # ints
    if data_type == 1:
        return int_list
    # floats
    elif data_type == 2:
        for d in int_list: list_as_type.append(float_int.int_to_float(d))
    # strings
    elif data_type == 3:
        for d in int_list: list_as_type.append(string_int.decode_int_to_string(d))
    # bytes
    elif data_type == 4:
        return int_list
    else:
        print('invalid data type')
        return -1

    return list_as_type