import type_handling
import struct

#bytes_type_code_book = {1: 5, 2: 8, 3: 5}
#data_type_code_book = {int: 1, float: 2, str: 3}

def serialize_block(block, column_data_types, type_to_bytes_code_book):
    '''
    takes input block (list of columns) and serializes each column. returns one long bitstring.    

    INPUTS
    block_list = one block in list of lists data structure (e.g. [[1,1,1...]['A', 'G', 'C', ...]...[...]])
    column_data_types = list of types (1,2,3) for each column
    type_to_bytes_code_book = code book which looks up the number of bytes used for each type
    
    OUTPUTS
    serialized_block_bitstring = one bitstring with all column serialization concatenated together
    
    '''
    serialized_block_bitstring = b''
    num_columns = len(column_data_types)

    for column in range(num_columns):


        curr_column = block[column]
        #print('data: ', curr_column)
        data_type = column_data_types[column]
        num_bytes = type_to_bytes_code_book[data_type]
        
        # convert column to proper type
        correct_type_column = type_handling.convert_to_type(curr_column, data_type)

        s_column = serialize_list(correct_type_column, data_type, num_bytes)

        serialized_block_bitstring += s_column
        #print('column: ', s_column)
        #print('block-update: ', serialized_block_bitstring)
    #print('block: ', serialized_block_bitstring)
    return serialized_block_bitstring

def serialize_list(in_list, data_type, num_bytes):
    '''
    INPUT
    one_column = list type, represents one column (e.g. [1,1,1,1,1])
    num_bytes = number of bytes needed to store each value in the colum
    data_type = data type of column (1, 2, 3)        

    OUTPUT
    s_bitstring = serialized bitstring (bytes object) of list from input
    
    '''
    s_bitstring = b''
    s_value = None
    for i in in_list:
        s_value = serialize_data(i, data_type, num_bytes)

        # is we have more than one string "AAA"

        if s_value != None:
            # special exception for strings:
            if data_type != 3:
                s_bitstring += s_value
            elif data_type == 3:
                if len(s_value) > 1:
                    s_bitstring += b'\0'+s_value+b'\0'
                else:
                    s_bitstring += s_value
            else: print('value is of bad type, cannot serialize')
        else: print('value is of bad type, cannot serialize')
    return s_bitstring

def serialize_data(data, data_type, num_bytes):

    # integers
    s_value = None
    if data_type == 1:
        try:
            s_value = data.to_bytes(num_bytes, byteorder='big', signed=False)
        except AttributeError:
            return -1
    # floats
    elif data_type == 2:
        try:
            s_value = struct.pack(">d", data)
        except AttributeError:
            return -1
    # strings
    elif data_type == 3:
        try:
            s_value = bytes(data, 'utf-8')
        except AttributeError:
            return -1
    return s_value

import deserialize

# string data
S = ['A', 'C', 'TTT', 'G', 'A']
S_s = b'ACTTTGA'
S_c = b''
S_dc = b''
S_ds = ['A', 'C', 'TTT', 'G', 'A']
#
# new_s = serialize_list(S, 3, 5)
# print(new_s)
# print(deserialize.deserialize_data(new_s, 5, 3, 5))

