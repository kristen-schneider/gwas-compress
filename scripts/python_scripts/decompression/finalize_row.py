def serialized_to_row(ds_bitstring, data_type):
    final_row = None
    if data_type == 1:
        final_row = integer_row(ds_bitstring)
    elif data_type == 3:
        final_row = string_row(ds_bitstring)
    return final_row

def integer_row(ds_bitstring):
    return ds_bitstring

def string_row(ds_bitstring):
    string_list = []
    d = 0

    print(ds_bitstring.replace('\x00\x00', '\x00').replace('\x00', ' ').strip().split(' '))    
    while d < len(ds_bitstring):
        if ds_bitstring[d] == '\x00':
            long_data_bool = True
            long_data = ''
            while long_data_bool:
                if ds_bitstring[d] == '\x00':
                    string_list.append(long_data)
                    long_data_bool = False 
                else:
                    long_data += ds_bitstring[d]
                d += 1
        else:
            string_list.append(ds_bitstring[d])
            d += 1
    return string_list
