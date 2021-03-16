def make_file_header(in_file):
    '''
    makes header for new compression file so we know how to decompress and deserialize
    
    INPUTS
    in_file = path to intput file (original gwas file)

    OUTPUTS
    info_header = [number_columns, block_size, number_blocks, [data_types], [bytes_sizes]]
    ...still thinking    

    '''    
    info_header = []   

    with open(in_file, 'r') as f_open:
        file_header = f_open.readline()  
        file_data = f_open.readline()
        print(file_header, file_data)
        

    f_open.close()
    
