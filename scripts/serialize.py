import basics

def serialize_list_columns(block_list, num_bytes_dict):
    '''
    takes input block (list of columns) and serializes each column. returns one long bitstring.    

    INPUTS
    block_list = one block in list of lists data structure (e.g. [[1,1,1...]['A', 'G', 'C', ...]...[...]])
    num_bytes_list = list of number of bytes to use for each column
    OUTPUTS
    serialized_block_bitstring = one bitstring with all column serialization concatenated together
    
    '''
    serialized_block_bitstring = b''

    for column in range(len(block_list)):
        data_type = basics.get_data_type(block_list[column][0])
        num_bytes = num_bytes_dict[data_type]
        correct_type_column = basics.convert_to_type(block_list[column], data_type)        
        s_column = serialize_data(correct_type_column, num_bytes, data_type)
        serialized_block_bitstring += s_column
    
    return serialized_block_bitstring

def serialize_data(column_list, num_bytes_per_val, data_type):
    '''
    INPUT
    one_column: list type, represents one column (e.g. [1,1,1,1,1])
    num_bytes_per_val: number of bytes needed to store each value in the column
    OUTPUT
    s_bitstring = serialized bitstring (bytes object) of list from input
    
    ''' 
    
    s_bitstring = b''
    
    
    for c in column_list:
        # serialize value according to its type
        
        # integers and booleans
        if data_type == int or data_type == bool:
            try:
                s_value = c.to_bytes(num_bytes_per_val, byteorder='big', signed = False)
            except AttributeError: return -1
        # TODO floats
        elif data_type == float: 
            try:
                s_value = None
            except AttributeError: return -1
        # strings  
        elif data_type == str:
            try:
                s_value = bytes(c, 'utf-8')
            except AttributeError: return -1

        # add serialized value to serialized bitstring
        s_bitstring += s_value
    
    return s_bitstring
