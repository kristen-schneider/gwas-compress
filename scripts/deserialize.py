def deserialize_data(dc_bitstring, lengths_of_bitstrings, val_types_of_bitstrings, num_bytes_list):
    '''
    take decompressed bitstring (same as serilized bitstring) and deserializes it.

    INPUTS
    dc_bitstring: decompressed bitstring
    lengths_of_bitstrings: list of lengths to separate bitstrings by column and deserialize (lengths are of dc_bitstrings).
    val_types_of_bitstrings: list of integers indicating what data type each column holds (e.g. [0,1,0,0,1]
    num_bytes: number of bytes that each character takes up (for now--same across all columns)
    
    OUTPUTS
    deserialized bitstring (same as original list)
    
    '''
    print(dc_bitstring)
    ds_list = []
    
    offset = 0 
    
    for curr_i in range(len(lengths_of_bitstrings)):
        # work with one bitstring segement at a time to deserialize
        curr_len_bitstring = lengths_of_bitstrings[curr_i]
        curr_val_type = val_types_of_bitstrings[curr_i]
        curr_ds_bitstring = []
        num_bytes = num_bytes_list[curr_i]
        
        for i in range(num_bytes):
            i += offset
            # input values are integers
            if curr_val_type == 0:
                curr_bytes = dc_bitstring[i*num_bytes:i*num_bytes+num_bytes]
                curr_ds_value = int.from_bytes(curr_bytes, byteorder='big', signed=False)
               
            # input values are strings 
            elif curr_val_type == 1:
                curr_bytes = dc_bitstring[i]
                print(curr_bytes)
                curr_ds_value = chr(curr_bytes)
            
            # input values are floats--STILL WORKING ON
            elif curr_val_type == 2:
                curr_bytes = 0
                curr_ds_value = 0                
            
            curr_ds_bitstring.append(curr_ds_value)
        
        offset+=curr_len_bitstring
        ds_list.append(curr_ds_bitstring)
    return ds_list


