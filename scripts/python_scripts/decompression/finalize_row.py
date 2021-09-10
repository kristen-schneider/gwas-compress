def serialized_to_row(ds_bitstring, compression_data_type, decompression_data_type):
    final_row = None
    if compression_data_type == 1:
        final_row = integer_row(ds_bitstring)
    elif compression_data_type == 3:
        final_row = string_row(ds_bitstring)
    return final_row

def integer_row(ds_bitstring):
    return ds_bitstring

def string_row(ds_bitstring):
    row_of_string_data = []
    d = 0
    long_string_bool = False
    long_string_val = ''
    
    while d < len(ds_bitstring):
        if ds_bitstring[d] == '\x00':
            long_string_bool = not long_string_bool
            if long_string_val != '':
                row_of_string_data.append(long_string_val)
                long_string_val = '' 
        elif long_string_bool:
            long_string_val += ds_bitstring[d] 
        else:
            row_of_string_data.append(ds_bitstring[d]) 
        d += 1
    
    return row_of_string_data

