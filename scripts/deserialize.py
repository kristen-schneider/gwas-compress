import basics
#dc_example = b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01ACTGA'

def deserialize_block_bitstring(dc_bitstring, block_size, list_data_types, dict_data_types):
    ds_bitstring_final = []
    num_columns = len(list_data_types)

    start = 0    
    for c in range(num_columns):
        column_data_type = list_data_types[c]
        column_bytes = dict_data_types[column_data_type] 
        column_length = basics.get_bitstring_length_by_data_type(block_size, column_data_type, column_bytes)
        column_dc_bitstring = dc_bitstring[start:start+column_length]
        start += column_length
        # deserialize a single bitstring at a time
        column_ds_bitstring = deserialize_data(column_dc_bitstring, column_data_type, column_bytes)
        ds_bitstring_final.append(column_ds_bitstring)

    return ds_bitstring_final
        
 

def deserialize_list_bitstrings_old(dc_bitstring, num_columns, lengths_of_bitstrings, data_types_of_bitstrings, num_bytes_list):
    '''
    take decompressed bitstring and break it into columns of decompressed bitstrings. call deserialize_data on each individual decompressed bitstring.

    INPUTS
    dc_bitstring: decompressed bitstring
    lengths_of_bitstrings: list of lengths to separate bitstrings by column and deserialize (lengths are of dc_bitstrings).
    data_types_of_bitstrings: list of integers indicating what data type each column holds (e.g. [0,1,0,0,1]
    num_bytes: number of bytes that each character takes up (for now--same across all columns)

    OUTPUTS
    list_of_ds_bitstrings: list of deserialized bitstrings

    '''

    ds_bitstring_final = []
    offset = 0
    
    for curr_i in range(num_columns):
        # break full dc_bitstring into column-specific bitstrings
        curr_length = lengths_of_bitstrings[curr_i]
        curr_data_type = data_types_of_bitstrings[curr_i]
        curr_num_bytes = num_bytes_list[curr_i]
        curr_dc_bitstring = dc_bitstring[offset:offset+curr_length] 
        offset+= curr_length    
        # deserialize a single bitstring at a time
        curr_ds_bitstring_list = deserialize_data(curr_dc_bitstring, curr_data_type, curr_num_bytes)        
        ds_bitstring_final.append(curr_ds_bitstring_list)

    return ds_bitstring_final 

def deserialize_data(dc_bitstring, data_type, num_bytes):
    curr_ds_bitstring = []
     
    for i in range(num_bytes):
        # input values are integers
        if data_type == int:
            curr_bytes = dc_bitstring[i*num_bytes:i*num_bytes+num_bytes]
            curr_ds_value = int.from_bytes(curr_bytes, byteorder='big', signed=False)
        
        # TODO floats
        elif data_type == float:
            curr_bytes = 0
            curr_ds_value = 0
        
        # input values are strings 
        elif data_type == str:
            curr_bytes = dc_bitstring[i]
            curr_ds_value = chr(curr_bytes)

        curr_ds_bitstring.append(curr_ds_value)
    
    return curr_ds_bitstring 


dc_example = b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01ACTGA'

deserialize_block_bitstring(dc_example, 5, [int, str], {int: 5, float: 5, str: 5})
