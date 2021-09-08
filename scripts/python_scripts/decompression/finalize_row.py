def serialized_to_row(ds_bitstring, data_type):
    final_row = None
    if data_type == 1:
        final_row = integer_row(ds_bitstring)
    return final_row

def integer_row(ds_bitstring):
    string_list = []
    for d in ds_bitstring:
        string_list.append(d)
    return string_list
