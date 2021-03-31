import type_handling
import serialize
import compress


DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes:4}
DATA_TYPE_BYTE_SIZES = {1: 5, 2: 8, 3: 5, 4:None}

def full_header_tools(full_header):
    # get header types and serialize
    header_types = get_header_types(full_header, DATA_TYPE_CODE_BOOK)
    serialized_header_types = serialize.serialize_list(header_types, DATA_TYPE_CODE_BOOK[int], DATA_TYPE_BYTE_SIZES[DATA_TYPE_CODE_BOOK[int]])
    # print(header_types, serialized_header_types)

    # get header ends and serialize
    header_ends_data = get_header_ends_and_serialize(full_header, header_types)

    # get number of elements in each header item
    header_num_elements = header_ends_data[0]
    serialized_header_num_elements = serialize.serialize_list(header_num_elements, DATA_TYPE_CODE_BOOK[int], DATA_TYPE_BYTE_SIZES[DATA_TYPE_CODE_BOOK[int]])
    # print(header_num_elements, serialized_header_num_elements)

    header_ends = header_ends_data[1]
    serialized_header_ends = serialize.serialize_list(header_ends, DATA_TYPE_CODE_BOOK[int], DATA_TYPE_BYTE_SIZES[DATA_TYPE_CODE_BOOK[int]])
    # print(header_ends, serialized_header_ends)

    # get header data (already serialized)
    serialized_header_data = header_ends_data[2]
    # print(serialized_header_data)


    return [serialized_header_types, serialized_header_num_elements, serialized_header_ends,
            serialized_header_data]

def get_header_types(full_header, DATA_TYPE_CODE_BOOK):
    header_types = []
    for h in full_header:
        if type(h) == list :h_type = type(h[0])
        else: h_type = type(h)

        try: header_types.append(DATA_TYPE_CODE_BOOK[h_type])
        except KeyError: print('no type for this data: ', h)

    return header_types

def get_header_ends_and_serialize(full_header, header_types):
    header_num_elements = []
    header_ends = []
    serialized_full_header = b''

    h_end = 0
    for h in range(len(full_header)):
        current_h = full_header[h]  # one element of header

        try: length_curr_h = len(current_h)
        except TypeError: length_curr_h = 1
        header_num_elements.append(length_curr_h)

        # serialize a list and a single value differently
        if type(current_h) == list:
            s_current_h = serialize.serialize_list(current_h, header_types[h], DATA_TYPE_BYTE_SIZES[header_types[h]])
        else:
            s_current_h = serialize.serialize_data(current_h, header_types[h], DATA_TYPE_BYTE_SIZES[header_types[h]])
        h_end += len(s_current_h)
        header_ends.append(h_end)

        serialized_full_header += s_current_h

    return header_num_elements, header_ends, serialized_full_header

# header = [1, 1, '\t', ['chr', 'position', 'other'], [1.00,12.12,3e+05], 3]
# full_header_tools(header)
# for h in c_full_header:
#     print(h)
# dc_full_header = decompress_header(c_full_header)
# print(dc_full_header)