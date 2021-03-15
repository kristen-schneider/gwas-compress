import sys

def serialize_data(one_column, num_bytes_per_val):
    '''
    INPUT
    one_column: list type, represents one column (e.g. [1,1,1,1,1])
    num_bytes_per_val: number of bytes needed to store each value in the column
    OUTPUT
    s_bitstring = serialized bitstring (bytes object) of list from input
    
    ''' 
    
    s_bitstring = b''
    
    for c in one_column:
        # serialize value according to its type
        try: #integers
            s_value = c.to_bytes(num_bytes_per_val, byteorder='big', signed = False)
        except AttributeError: #strings
            s_value = bytes(c, 'utf-8')

        # add serialized value to serialized bitstring
        s_bitstring += s_value
    
    return s_bitstring

