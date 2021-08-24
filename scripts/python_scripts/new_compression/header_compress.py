import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

# personal imports
from utils import type_handling
import serialize_header

def full_header_tools(data_type_byte_sizes, full_header):
    """
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
    """
    # get header types and serialize
    header_types = get_header_types(full_header)
    # can pass 1 as data type because data types are all integers (1, 2, 3, 4)
    serialized_header_types = serialize_header.serialize_list(header_types, 1, data_type_byte_sizes[1])

    ## get number of elements in each header item
    header_num_elements = get_header_lengths(full_header)
    # can pass 1 as data type because data types are all integers (1, 2, 3, 4)
    serialized_header_num_elements = serialize_header.serialize_list(header_num_elements, 1, data_type_byte_sizes[1])

    ## get full serialized header as a list
    #serialized_header_list = get_serialized_header_as_list(header_types, data_type_byte_sizes, full_header)
    ## get full serialized header as a bitstring
    #serialized_header = join_serialized_list(serialized_header_list)

    ## get ends of each serialized element in column
    #header_ends = get_header_ends(serialized_header_list)
    #serialized_header_ends = serialize_header.serialize_list(header_ends,
    #                                                         data_type_byte_sizes[data_type_code_book[int]])

    #return [serialized_header_types, serialized_header_num_elements, serialized_header_ends,
    #        serialized_header]

def get_header_types(full_header):
    """
    returns the types of each element in the header

    INPUT
        full_header = full header (12 elements)
        data_type_code_book = e.g. {int: 1, float: 2, str: 3, bytes:4}

    OUTPUT
        header_types = data types of each element in the header
    """
    header_types = []
    for h in full_header:
        try: header_types.append(type_handling.get_data_type(h))
        except TypeError: header_types.append(type_handling.get_data_type(h[0]))
        #if type(h) == list :h_type = type(h[0])
        #else: h_type = type(h)
    
        #try: header_types.append(data_type_code_book[h_type])
        #except KeyError: print('no type for this data: ', h)

    return header_types

def get_header_lengths(full_header):
    """
    returns the lengths of each element in the header

    INPUT
        full_header = full header

    OUTPUT
        header_lengths = lengths of each element in the header
    """
    header_lengths = []
    for h in full_header:
        try: header_lengths.append(len(h))
        except TypeError: header_lengths.append(1)
    return header_lengths

def get_serialized_header_as_list(header_types, data_type_byte_sizes, full_header):
    """
    returns serialized header as a list

    INPUT
        header_types = data types of each element in the header
        data_type_byte_sizes: from config file, assigns bytes to each data type, for compression
        full_header = full header (12 elements)

    OUTPUT
        serialized_header_list = returns a list of serialized header elements
    """
    serialized_header_list = []

    for h in range(len(full_header)):
        current_h = full_header[h]  # one element of header

        # serialize a list and a single value differently
        if type(current_h) == list:
            s_current_h = serialize_header.serialize_list(current_h,
                                                          header_types[h],
                                                          data_type_byte_sizes[header_types[h]])
        else:
            s_current_h = serialize_header.serialize_data(current_h,
                                                          header_types[h],
                                                          data_type_byte_sizes[header_types[h]])

        serialized_header_list.append(s_current_h)
    return serialized_header_list

def join_serialized_list(serialized_header_list):
    """
    returns a full bitstring of a list of bitstrings

    INPUT
        serialized_header_list = returns a list of serialized header elements

    OUTPUT
       serialized_header = full bitstring of all serialized header data together
    """
    serialized_header = b''
    for sh in serialized_header_list:
        serialized_header+=sh
    return serialized_header

def get_header_ends(serialized_header_list):
    """
    return ends of each serialized element of the header

    INPUT
        serialized_header_list = returns a list of serialized header elements

    OUTPUT
        header_ends = end positions of each serialized element of header (for deserialization)
    """
    end = 0
    header_ends = []
    for h in serialized_header_list:
        header_ends.append(end+len(h))
        end+=len(h)
    return header_ends
