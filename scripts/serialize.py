import sys

def serialize_data(one_col_list, num_bytes_per_char):
    '''
    INPUT
    one_col_list: list type, represents one column
    num_bytes_per_char: number of bytes needed to store each member in the column
    OUTPUT
    bytes object of list from input
    ''' 
    
    s_bitstring = b''
    
    for i in one_col_list:
        # to work on integets
        try:
            s_bitstring += i.to_bytes(num_bytes_per_char, byteorder='big', signed = False)
        # to work on strings
        except AttributeError: 
            s_bitstring += bytes(i, 'utf-8')

    return s_bitstring

