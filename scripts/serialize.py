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
    for i in in_list:
        s_value = serialize_data(i, data_type, num_bytes)
        
        # add serialized value to serialized bitstring
        if s_value != None: s_bitstring += s_value
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



# i = 4
# ia=[4,4,4,4]
# s = "A"
# sa = ["A", "A", "A", "A"]
# f = 1.32e+00
#
# b = [[4,4,4,4], ["A", "A", "A", "A"]]
# print(serialize_data(i, 1, 5))
# print(serialize_list(ia, 1, 5))
# print(serialize_block(b, [1,3], {1: 5, 2: 8, 3: 5}))

#header = [[1, 1], ['\t'], ['chr', 'pos', 'ref', 'alt'], [1, 1, 3, 3], [4]]
#print(serialize_list_columns(header, [1, 3, 3, 1, 1], {1: 5, 2: 8, 3: 5}))
