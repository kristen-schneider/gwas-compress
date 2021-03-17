import basics
import struct

def deserialize_block_bitstring(dc_bitstring, block_size, list_data_types, dict_data_types):
    '''
    take decompressed bitstring for a full block and break it into columns of decompressed bitstrings. call deserialize_data on each individual decompressed bitstring.

    INPUTS
    dc_bitstring = decompressed bitstring for one block (e.g. b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01ACTGA')
    block_size = number of rows in a block
    list_data_types = list of data types in block (e.g. [int, str]
    dict_data_types = dictionary of data types and their byte sizes (e.g. {int: 5, float: 5, str: 5})    

    OUTPUTS
    list_of_ds_bitstrings: list of deserialized bitstrings

    '''
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
        column_ds_bitstring = deserialize_data(column_dc_bitstring, block_size, column_data_type, column_bytes)
        ds_bitstring_final.append(column_ds_bitstring)

    return ds_bitstring_final
        

def deserialize_data(dc_bitstring, block_size, data_type, num_bytes):
    curr_ds_bitstring = []
     
    for i in range(block_size):
        # input values are integers
        if data_type == int:
            curr_bytes = dc_bitstring[i*num_bytes:i*num_bytes+num_bytes]
            curr_ds_value = int.from_bytes(curr_bytes, byteorder='big', signed=False)
        
        # TODO floats
        elif data_type == float:
            curr_bytes = dc_bitstring[i*num_bytes:i*num_bytes+num_bytes]
            curr_ds_value = struct.unpack('>d', curr_bytes)[0]          
    
        # input values are bools        
        elif data_type == bool:
            curr_bytes = dc_bitstring[i*num_bytes:i*num_bytes+num_bytes]
            curr_ds_value = bool.from_bytes(curr_bytes, byteorder='big', signed=False)
        
        elif data_type == float:
            curr_bytes = 0
            curr_ds_value = 0
        
        # input values are strings 
        elif data_type == str:
            curr_bytes = dc_bitstring[i]
            curr_ds_value = chr(curr_bytes)

        curr_ds_bitstring.append(curr_ds_value)
    
    return curr_ds_bitstring 

