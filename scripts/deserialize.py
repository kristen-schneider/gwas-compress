def deserialize_data(dc_bitstring, char_type, len_bitstring, size_char):
    '''
    take decompressed bitstring (same as serilized bitstring) and deserializes it.

    INPUTS
    dc_bitstring: decompressed bitstring
    len_bistring: length of original data
    size_char: number of bytes that each character takes up
    OUTPUTS
    deserialized bitstring (same as original list)

    '''

    ds_list = []
    
    for i in range(len_bitstring):
        # input values are integers
        if char_type == 0:
            ds_list.append(int.from_bytes(dc_bitstring[i*size_char:i*size_char+size_char], byteorder='big', signed=False))
        # input values are strings 
        elif char_type == 1:
            ds_list.append(chr(dc_bitstring[i]))
    
    return ds_list

