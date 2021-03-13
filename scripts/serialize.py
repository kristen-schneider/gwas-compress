import sys
def main():
    A = [1,1,1,1,1]
    B = ['A', 'C', 'T', 'G', 'A']
    print(serialize_data(A, 5))
    print(serialize_data(B, 5))
    
    

def serialize_data(one_col_list, num_bytes_per_char):
    '''
    INPUT
    one_col_list: list type, represents one column
    num_bytes_per_char: number of bytes needed to store each member in the column
    OUTPUT
    bytes object of list from input
    ''' 
    
    bytes_string = b''
    
    for i in one_col_list:
        # to work on integets
        try:
            bytes_string += i.to_bytes(num_bytes_per_char, byteorder='big', signed = False)
        # to work on strings
        except AttributeError: 
            bytes_string += bytes(i, 'utf-8')

    return bytes_string

if __name__ == '__main__': main()
