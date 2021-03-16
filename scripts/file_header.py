import funnel_format

def make_file_header(in_file, block_size):
    '''
    makes header for new compression file so we know how to decompress and deserialize
    
    INPUTS
    in_file = path to intput file (original gwas file)

    OUTPUTS
    info_header = [number_columns, block_size, [data_types], [bytes_sizes]]
    ...still thinking    (number of blocks?)

    '''    
    info_header = []   
    
    data_types = []
    bytes_sizes = []

    with open(in_file, 'r') as f_open:
        file_header = f_open.readline().rstrip().split()
        file_data = f_open.readline().rstrip().split()
   
    f_open.close()
 
    info_header.append(len(file_header))
    info_header.append(block_size)
    #info_header.append(get_data_types(file_data))
    #info_header.append(bytes_sizes)
   
    return info_header 
    
def get_data_types(file_data):
    '''
    gets the types of each column
    
    INPUTS 
    file_data = first line of the original gwas file (not the header)

    OUTPUTS
    data_types = list of all types of data (in order) for each column    

    '''
    data_types = []
    for d in file_data:
        data_types.append(type(d))
    print(data_types)
    return data_types
