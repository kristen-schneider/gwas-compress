def get_ff_column_size(column):
    """
    compute size of column in it's original form ['1','1','1','1',...'1']
    """

    char_bytes = 8
    total_num_bytes = 0 
    for d in column:
        curr_num_bytes = num_bytes*len(d)
        total_num_bytes += curr_num_bytes

    return total_num_bytes
