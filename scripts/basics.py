def get_data_type(data):
    '''
    retruns proper data type of incoming data.
    most data is read in as a string. this will try and discern if it is actually an integer or float

    INPUT
    data = incoming data. likely to be read in as string (NOT A LIST)
    OUTPUT
    data_type = int, float, bool, or str
    
    '''
    # hierarchy: int, bool, float, string
    try:
        int(data)
        return int
    except ValueError: 
        try:
            float(data)
            return float
        except ValueError:
            try:
                if 'true' in data.lower() or 'false' in data.lower():
                    return bool
                else:
                    try:
                        str(data)
                        return str
                    except ValueError:
                        return type(data)
            except ValueError:
                try:
                    str(data)
                    return str
                except ValueError:
                    return type(data)

def make_data_types_list(row):
    '''
    given a row of data, returns all the types of data in that row
    
    INPUTS
    row = list of data that we see in a row (e.g. ['1', 'A', ...]

    OUTPUTS
    data_types_list = list of data types witnessed in that row (e.g. [int, str...])

    '''

    data_types_list = []
    for r in row:
        data_type = get_data_type(r)
        data_types_list.append(data_type)
    return data_types_list
        

    
def convert_to_type(column, data_type):
    '''
    converts a list of data types into a list of new data_types
    
    INPUT
    column = list of data (e.g. ['1','1','1','1','1']
    data_type = type to which we want to convert (e.g. int)
    
    OUTPUT
    correct_type_column = new list with correct type (e.g. [1,1,1,1,1])

    '''
    correct_type_column = []
    
    # if the type is already correct, just return column
    if type(column[0]) == data_type: return column
    else:
        for c in column:
            if data_type == int:
                correct_type_column.append(int(c))
            elif data_type == float:
                correct_type_column.append(float(c))
            elif data_type == bool:
                if 'true' in c.lower(): correct_type_column.append(True)
                elif 'false' in c.lower(): correct_type_column.append(False)
                else: return -1  
            elif data_type == str:
                correct_type_column.append(str(c))
            else: return -1
                
    return correct_type_column

def get_bitstring_length_by_data_type(num_elements, data_type, num_bytes):
    '''
    returns the the lengths of a bitstring of given data type, bytes, and original number of elements
    
    INPUTS
    num_elements = original number of elements represented by this bitstring. also can be block size. (e.g. [1,1,1,1,1] = 5)
    data_type = type of data to be represented in the bitstring (e.g. [1,1,1,1,1] = int
    num_bytes = number of bytes we are using to be represented in this bitstring

    OUTPUTS
    len_bitsring = this will return the length of a bitstring that should represent one column only

    '''
    if data_type == int: bitstring_length = num_elements*num_bytes
    elif data_type == bool: bitstring_length = num_elements*num_bytes
    elif data_type == float: bitstring_length = 0 # TODO floats
    elif data_type == str: bitstring_length = num_elements 
    else: bitstring_length = -1 
    return bitstring_length

