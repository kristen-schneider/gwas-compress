import funnel_format
def get_column_data(in_file, delimeter):
    '''
    gets columns names, types, and number from the input file
    
    INPUTS
    in_file = path to intput file (original gwas file)
    delimeter = file delimeter
    
    OUTPUTS
    column_info = list of names, types, and number (e.g. [[chr, pos, ref, alt, ...], [int, int, str, str, ...], 10]

    '''    
    column_info = []
       
    with open(in_file, 'r') as f_open:
        column_names_str = f_open.readline()
        column_types_str = f_open.readline()
    f_open.close() 
     
    column_names_list = get_column_names(column_names_str, delimeter)
    column_types_list = get_column_types(column_types_str, delimeter)
    
    column_info.append(column_names_list)
    column_info.append(column_types_list)

    return column_info 

def determine_delimeter(f):
    '''
    deterimine which delimeter is used in the file
    
    INPUTS
    f: path to input file
    OUTPUS
    returns delimeter used in file
    '''
    with open(f, 'r') as f_open:
        header = f_open.readline()
        if len(header.split('\t')) > 1: delimeter = '\t'
        elif len(header.split(' ')) > 1: delimeter = ' '
        elif len(header.split(',')) > 1: delimeter = ','

    f_open.close()
    return delimeter

    

def get_column_names(row, delimeter):
    '''
    gets the header names of each column
    
    INPUTS 
    row = first line of the original gwas file
    delimeter = file delimeter

    OUTPUT
    column_names = list of all column header names (e.g. [chr, pos, ref, alt, ...])    

    '''

    column_names = row.rstrip.split(delimeter)
    return column_names
    
def get_column_types(row, delimeter):
    '''
    gets the data types of each column
    
    INPUTS 
    row = second line of the original gwas file
    delimeter = file delimeter

    OUTPUTS
    data_types = list of all types of data (in order) for each column    

    '''
    
    data_types = basics.make_data_types_list(row.rstrip().split(delimeter))
    
    return data_types
