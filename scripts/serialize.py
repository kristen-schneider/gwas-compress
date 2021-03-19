import type_handling
import struct

#bytes_type_code_book = {1: 5, 2: 8, 3: 5}
#data_type_code_book = {int: 1, float: 2, str: 3}

def serialize_list_columns(block_list, column_data_types, type_to_bytes_code_book):
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
        curr_column = block_list[column]
        data_type = column_data_types[column]
        num_bytes = type_to_bytes_code_book[data_type]
        
        # convert column to proper type
        correct_type_column = type_handling.convert_to_type(curr_column, data_type)        
        
        s_column = serialize_data(correct_type_column, num_bytes, data_type)
        serialized_block_bitstring += s_column
    
    return serialized_block_bitstring

def serialize_data(column_list, num_bytes, data_type):
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
    
    for c in column_list:
        
        # list (should be used for header where we have some list and some non-list data)
        if type(c) == list:  
            
            
            serialize_data(c, num_bytes, data_type)
            
        # serialize value according to its type
        else:
            # integers
            if data_type == 1:
                try:
                    s_value = c.to_bytes(num_bytes, byteorder='big', signed = False)
                except AttributeError: return -1
            # floats
            elif data_type == 2: 
                try:
                    s_value = struct.pack(">d", c)
                except AttributeError: return -1
            # strings  
            elif data_type == 3:
                try:
                    s_value = bytes(c, 'utf-8')

                except AttributeError: return -1
        
        # add serialized value to serialized bitstring
        if s_value != None: s_bitstring += s_value
        else: print('value is of bad type, cannot serialize')
    return s_bitstring

