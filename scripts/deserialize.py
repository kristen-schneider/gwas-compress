def deserialize_list_bitstrings(dc_bitstring, num_columns, lengths_of_bitstrings, val_types_of_bitstrings, num_bytes_list):
    '''
    take decompressed bitstring and break it into columns of decompressed bitstrings. call deserialize_data on each individual decompressed bitstring.

    INPUTS
    dc_bitstring: decompressed bitstring
    lengths_of_bitstrings: list of lengths to separate bitstrings by column and deserialize (lengths are of dc_bitstrings).
    val_types_of_bitstrings: list of integers indicating what data type each column holds (e.g. [0,1,0,0,1]
    num_bytes: number of bytes that each character takes up (for now--same across all columns)

    OUTPUTS
    list_of_ds_bitstrings: list of deserialized bitstrings

    '''

    ds_bitstring_final = []
    offset = 0
    
    for curr_i in range(num_columns):
        # break full dc_bitstring into column-specific bitstrings
        curr_length = lengths_of_bitstrings[curr_i]
        curr_val_type = val_types_of_bitstrings[curr_i]
        curr_num_bytes = num_bytes_list[curr_i]
        curr_dc_bitstring = dc_bitstring[offset:offset+curr_length] 
        offset+= curr_length    
        # deserialize a single bitstring at a time
        curr_ds_bitstring_list = deserialize_data(curr_dc_bitstring, curr_val_type, curr_num_bytes)        
        ds_bitstring_final.append(curr_ds_bitstring_list)

    return ds_bitstring_final 

def deserialize_data(dc_bitstring, val_type, num_bytes):
    curr_ds_bitstring = []
     
    for i in range(num_bytes):
        # input values are integers
        if val_type == 0:
            curr_bytes = dc_bitstring[i*num_bytes:i*num_bytes+num_bytes]
            curr_ds_value = int.from_bytes(curr_bytes, byteorder='big', signed=False)

        # input values are strings 
        elif val_type == 1:
            curr_bytes = dc_bitstring[i]
            curr_ds_value = chr(curr_bytes)

        # input values are floats--STILL WORKING ON
        elif val_type == 2:
            curr_bytes = 0
            curr_ds_value = 0


        curr_ds_bitstring.append(curr_ds_value)
    
    return curr_ds_bitstring 

