import numpy as np
def get_data_type(str_data, data_type_code_book):
    '''
    Retruns proper data type of incoming data. This is used only once for a the first row.
    Most data is read in as a string. this will try and discern if it is actually an integer/float

    INPUT
        data = incoming data. likely to be read in as string
    OUTPUT
        data_type = int, float, or str
        * removed bool functionality. if bool to add: int, float, bool, str.
    
    '''
    # hierarchy: int, float, string
    try:
        int(str_data)
        return data_type_code_book[int]
    except ValueError: 
        try:
            float(str_data)
            return data_type_code_book[float]
        except ValueError:
            try:
                str(str_data)
                return data_type_code_book[str]
            except ValueError:
                print('could not detect data type as int, float, or string')
                return type(str_data)

def get_column_types(row, data_type_code_book):
    '''
    Given a row of data, returns all the types of data in that row
    Data types are according to code_book
    
    INPUT
        row = list of data that we see in a row (e.g. ['1', 'A', ...]

    OUTPUT
        data_types_list = list of data types witnessed in that row (e.g. [1, 2, 2, 1, 1...])

    '''

    data_types_list = []
    for r in row:
        data_type = get_data_type(r, data_type_code_book)
        data_types_list.append(data_type)
    return data_types_list
        
def convert_to_type(column_data, data_type):
    '''
    converts a list of values in a column of some data types into a list values in some column of new data_types
    
    INPUT
        column_data = list of data (e.g. ['1','1','1','1','1']
        data_type = type to which we want to convert (e.g. int)
        data_type_code_book = code book which converts

    OUTPUT
        correct_type_column = new list with correct type (e.g. [1,1,1,1,1])

    '''
    correct_type_column = []
    
    for c in column_data:
        if data_type == 1:
            # try to convert to integer.
            try: correct_type_column.append(int(c))
            except ValueError:
                # for chromosome X,Y values
                try:
                    if 'X' in c or 'Y' in c:
                        correct_type_column.append(str(c))
                    else: print('cannot convert to integer: ', c)
                except ValueError: print('cannot convert to integer: ', c)
        elif data_type == 2:
            # try to convert to float, if cannot, return numpy's nan mask
            try: correct_type_column.append(float(c))
            except ValueError: correct_type_column.append(np.nan)
        elif data_type == 3:
            # try to convert to string.
            try: correct_type_column.append(str(c))
            except ValueError:
                print('cannot convert to string: ', c)
        else:
            print('could not convert data type to int, float, or string')
            return -1
                
    return correct_type_column

def get_bitstring_length_by_data_type(block_size, data_type, num_bytes):
    '''
    returns the the lengths of a bitstring of given data type, bytes, and original number of elements
    
    INPUTS
        block_size = number of rows present in a block
        data_type = type of data to be represented in the bitstring (e.g. [1,1,1,1,1] = int
        num_bytes = number of bytes we are using to be represented in this bitstring

    OUTPUTS
        len_bitsring = this will return the length of a bitstring that should represent one column only

    '''
    if data_type == 1: bitstring_length = block_size*num_bytes
    elif data_type == 2: bitstring_length = block_size*num_bytes
    elif data_type == 3: bitstring_length = block_size 
    else:
        print('data is not of type int, float, or string')
        bitstring_length = -1 
    return bitstring_length

def string_list_to_int(data_list, data_type):
    '''
    given a list of string data, return a list of typed data
    '''
    typed_list = []
    for data in data_list:
        typed_data = convert_to_int(data, data_type)
        typed_list.append(typed_data)
    return typed_list

def convert_to_int(data, data_type):
    '''
    given any data (int, float, string)
    INPUTS
        data = intput data
        data_tupe = original data type
    OUTPUTS
        integer version of data
    '''
    if data_type == 1:
        return int(data)
    elif data_type == 2:
        return float_to_int(data)
    elif data_type == 3:
        return string_to_int(data)

def float_to_int(data):
    int_data = None
    # float_data = float(data)
    separate_exponent = data.split('e')
    number = separate_exponent[0]
    exponent = int(separate_exponent[1])
    base_decimal = number.split('.')
    base = int(base_decimal[0])
    decimal = int(base_decimal[1])
    int_data = [base, decimal, exponent]
    return int_data

def string_to_int(data):
    # (22 integer chromosomes, x and y)
    # A,C,T,G = 2,3,4,5
    int_data = None

    if data == 'false': string_data = 0
    elif data == 'true': string_data = 1
    elif data == 'A': string_data = 2
    elif data == 'C': string_data = 3
    elif data == 'G': string_data = 4
    elif data == 'T': string_data = 5
    elif data == 'X': string_data = 23
    elif data == 'Y': string_data = 24
    else: int_data = int(data)

    return string_data

