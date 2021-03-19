import type_handling


def get_file_data(in_file, data_type_code_book):
    '''
    retrieves some basic header information that should be stored in header up to this point. 
        (delimiter, columns names, column types, and column number from the input file)
    
    INPUT
    in_file = path to intput file (original gwas file)
    
    OUTPUT
    header_start = list of information to be included in header (so far). still need to add info about block locations and size of blocks

    ''' 
   
    header_start = []
    
    # to be included in header
    magic_number_version_number = [1,1]
    delimeter = [None]
    column_names_list = None
    column_types_list = None
    num_columns = [None]
   
    # grab first two rows which will inform our data types, names, lengthts, etc.
    with open(in_file, 'r') as f_open:
        column_names_str = f_open.readline()
        column_types_str = f_open.readline()
    f_open.close() 

    # assign 
    delimeter = get_delimeter(column_names_str)
    column_names_list = get_column_names(column_names_str, delimeter)
    column_types_list = type_handling.get_column_types(column_types_str.rstrip().split(delimeter), data_type_code_book)
    num_columns = get_num_columns(column_names_list, column_types_list)
   
    header_start.append(magic_number_version_number)
    header_start.append([delimeter])
    header_start.append(column_names_list)
    header_start.append(column_types_list)
    header_start.append([num_columns])

    return header_start 

def get_delimeter(row):
    '''
    deterimine which delimeter is used in the file
    
    INPUT
    f: path to input file
    OUTPUT
    returns delimeter used in file
    '''
    
    if len(row.split('\t')) > 1: delimeter = '\t'
    elif len(row.split(' ')) > 1: delimeter = ' '
    elif len(row.split(',')) > 1: delimeter = ','
    else: return -1
    
    return delimeter

    

def get_column_names(row, delimeter):
    '''
    gets the header names of each column
    
    INPUT 
    row = first line of the original gwas file, string
    delimeter = file delimeter

    OUTPUT
    column_names = list of all column header names (e.g. [chr, pos, ref, alt, ...])    

    ''' 

    column_names = row.rstrip().split(delimeter)
    return column_names
    
def get_num_columns(column_names_list, column_types_list):
    '''
    checks that names and types are same length to return number of columns in a file
    
    INPUT
    column_names_list = list of header names for columns
    column_types_list = list of data types for columns
    
    OUTPUT
    num_columns = number of columns
    
    '''
    if (len(column_names_list) == len(column_types_list)):
        num_columns = len(column_names_list)
    else: return -1

    return num_columns
