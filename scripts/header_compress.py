import type_handling
import serialize
import compress


# DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes:4}
# DATA_TYPE_BYTE_SIZES = {1: 5, 2: 8, 3: 5, 4:None}

def full_header_tools(data_type_code_book, data_type_byte_sizes, full_header):
    '''
    works to serialize the header as well as any pertinent tools which will aide to reconstruct the header

    INPUT
    data_type_code_book: something like {int: 1, float: 2, str: 3, bytes:4}
    data_type_byte_sizes: something like {1: 5, 2: 8, 3: 5, 4:None}
    full_header: full header

    OUTPUT
    [serialized_header_types: data types of all elements of header, serialized
     serialized_header_num_elements: number of elements in each part of the header, serialized
     serialized_header_ends: end locations of each serialized element, serialized
     serialized_header_data: serialized header]
    '''
    # get header types and serialize
    header_types = get_header_types(full_header, data_type_code_book)
    serialized_header_types = serialize.serialize_list(header_types, data_type_code_book[int], data_type_byte_sizes[data_type_code_book[int]])

    # get number of elements in each header item
    header_num_elements = get_header_lengths(full_header)
    serialized_header_num_elements = serialize.serialize_list(header_num_elements, data_type_code_book[int], data_type_byte_sizes[data_type_code_book[int]])

    # get full serialized header as a list
    serialized_header_list = serialize_header(header_types, data_type_byte_sizes, full_header)
    # get full serialized header as a bitstring
    serialized_header = join_serialized_list(serialized_header_list)

    # get ends of each serialized element in column
    header_ends = get_header_ends(serialized_header_list)
    serialized_header_ends = serialize.serialize_list(header_ends, data_type_code_book[int], data_type_byte_sizes[data_type_code_book[int]])

    return [serialized_header_types, serialized_header_num_elements, serialized_header_ends,
            serialized_header]

def get_header_types(full_header, DATA_TYPE_CODE_BOOK):
    '''
    returns the types of each element in the header
    '''
    header_types = []
    for h in full_header:
        if type(h) == list :h_type = type(h[0])
        else: h_type = type(h)

        try: header_types.append(DATA_TYPE_CODE_BOOK[h_type])
        except KeyError: print('no type for this data: ', h)

    return header_types

def get_header_lengths(full_header):
    '''
    returns the lengths of each element in the header
    '''
    header_lengths = []
    for h in full_header:
        try: header_lengths.append(len(h))
        except TypeError: header_lengths.append(1)
    return header_lengths

def serialize_header(header_types, data_type_byte_sizes, full_header):
    '''
    returns serialized header as a list
    '''
    serialized_header_list = []

    for h in range(len(full_header)):
        current_h = full_header[h]  # one element of header

        # serialize a list and a single value differently
        if type(current_h) == list:
            s_current_h = serialize.serialize_list(current_h, header_types[h], data_type_byte_sizes[header_types[h]])
        else:
            s_current_h = serialize.serialize_data(current_h, header_types[h], data_type_byte_sizes[header_types[h]])

        serialized_header_list.append(s_current_h)
    return serialized_header_list

def join_serialized_list(serialized_header_list):
    '''
    returns a full bitstring of a list of bitstrings
    '''
    serialized_header = b''
    for sh in serialized_header_list:
        serialized_header+=sh
    return serialized_header

def get_header_ends(serialized_header_list):
    '''
    return ends of each serialized element of the header
    '''
    end = 0
    header_ends = []
    for h in serialized_header_list:
        header_ends.append(end+len(h))
        end+=len(h)
    return header_ends