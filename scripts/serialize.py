import sys
def main():
    A = [1,1,1,1,1]
    B = ['A', 'C', 'T', 'G', 'A']
    print(len(serialize_data(A, sys.getsizeof(int()))))
    print(sys.getsizeof(int()))
    print(serialize_data(B, sys.getsizeof(str())))
    
    

def serialize_data(one_col_list, num_bytes_per_char):
    '''
    INPUT
    one_col_list: list type, represents one column
    num_bytes_per_char: number of bytes needed to store each member in the column
    OUTPUT
    bytes object of list from input
    ''' 
    
    byte_list = b''
    
    for i in one_col_list:
        # to work on integets
        try:
            byte_list += i.to_bytes(num_bytes_per_char, byteorder='big', signed = False)
        # to work on strings
        except AttributeError: 
            byte_list += bytes(i, 'utf-8')

    return byte_list

if __name__ == '__main__': main()
