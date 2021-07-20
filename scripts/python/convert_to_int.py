import float_int
import string_int

def convert_list_to_int(in_list, data_type):
    list_as_int = []
    # ints
    if data_type == 1:
        for d in in_list: list_as_int.append(int(d))
    # floats
    elif data_type == 2:
        for d in in_list: list_as_int.append(float_int.float_to_int(d))
    # strings
    elif data_type == 3:
        list_as_int = string_int.encode_column(in_list)
    # bytes
    elif data_type == 4:
        return in_list
    else:
        print('invalid data type')
        return -1


    return list_as_int
