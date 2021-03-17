import basics


def get_file_data(in_file):
    '''
    gets columns names, types, and number from the input file
    
    INPUT
    in_file = path to intput file (original gwas file)
    
    OUTPUT
    file_info = list of information from file [delimeter, col_names, col_types, number_cols (e.g. ['\t', [chr, pos, ref, alt, ...], [int, int, str, str, ...], 10]

    ''' 
   
    file_info = []
    delimeter = None
    column_names_list = None
    column_types_list = None
    num_columns = 0
   
    with open(in_file, 'r') as f_open:
        column_names_str = f_open.readline()
        delimeter = get_delimeter(column_names_str)
        column_types_str = f_open.readline()
    f_open.close() 

    column_names_list = get_column_names(column_names_str, delimeter)
    column_types_list = get_column_types(column_types_str, delimeter)
    #print(column_names_list)
    #print(column_types_list)
    num_columns = get_num_columns(column_names_list, column_types_list)
   
    file_info.append(delimeter)
    file_info.append(column_names_list)
    file_info.append(column_types_list)
    file_info.append(num_columns)

    return file_info 

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
    
def get_column_types(row, delimeter):
    '''
    gets the data types of each column
    
    INPUT 
    row = second line of the original gwas file
    delimeter = file delimeter

    OUTPUT
    data_types = list of all types of data (in order) for each column    

    '''
    
    data_types = basics.make_data_types_list(row.rstrip().split(delimeter))
    return data_types

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
