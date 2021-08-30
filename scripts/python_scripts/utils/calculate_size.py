def get_ff_column_size(column):
    """
    compute size of column in it's original form ['1','1','1','1',...'1']
    """

    char_bytes = 8
    total_num_bytes = 0 
    for d in column:
        curr_num_bytes = char_bytes*len(d)
        total_num_bytes += curr_num_bytes

    return total_num_bytes

def get_bitstring_column_size(column_bitstring):
    """
    compute size of a bitstring (column after compression)
    """
    
    char_bytes = 8
    total_num_bytes = len(column_bitstring)*char_bytes
    return total_num_bytes

#a = ['1','1','1','1','1']
#b = ['4.321','3.56','4e-05','5.022','-3e-04'] 
#print(get_ff_column_size(a), get_ff_column_size(b))
