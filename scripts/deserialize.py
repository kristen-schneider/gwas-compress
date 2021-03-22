import type_handling
import struct

def deserialize_block(dc_bitstring, block_size, column_data_types, type_to_bytes_code_book):
    '''
    take decompressed bitstring for a full block and break it into columns of decompressed bitstrings. call deserialize_data on each individual decompressed bitstring.

    INPUT
    dc_bitstring = decompressed bitstring for one block 
    block_size = number of rows in a block
    column_data_types = list of data types in block (e.g. [1, 3]
    type_to_bytes_code_book = dictionary of data types and their byte sizes (e.g. {1: 5, 2: 8, 3: 5})    

    OUTPUT
    list_of_ds_bitstrings: list of deserialized bitstrings

    '''
    ds_bitstring_final = []
    num_columns = len(column_data_types)

    start = 0    
    for c in range(num_columns):
        column_data_type = column_data_types[c]
        column_bytes = type_to_bytes_code_book[column_data_type] 

        column_length = type_handling.get_bitstring_length_by_data_type(block_size, column_data_type, column_bytes)
        column_dc_bitstring = dc_bitstring[start:start+column_length]
        
        start += column_length
        
        # deserialize a single bitstring at a time
        column_ds_bitstring = deserialize_data(column_dc_bitstring, block_size, column_data_type, column_bytes)
        ds_bitstring_final.append(column_ds_bitstring)

    return ds_bitstring_final
        

def deserialize_data(dc_bitstring, block_size, data_type, num_bytes):
    '''
    deserializes data for one column
    
    INPUT
    dc_bitstring = decompressed bitstring for one column
    block_size = number of rows in a block (size of output column)
    data_type = type of data in this column (1,2,3)
    num_bytes = number of bytes that is associated with this data type
    
    OUTPUT
    ds_bitstring = derserialized data for one column (e.g. [1,1,1,1,1]

    '''
    ds_bitstring = []
    curr_ds_value = None
    INDEL = False
    
    #for i in range(block_size):
    loop = len(dc_bitstring)
    i = 0
    while i < loop:
        # input values are integers
        if data_type == 1:
            curr_bytes = dc_bitstring[i*num_bytes:i*num_bytes+num_bytes]
            curr_ds_value = int.from_bytes(curr_bytes, byteorder='big', signed=False)
            i += 1

        # input values are floats
        elif data_type == 2:
            curr_bytes = dc_bitstring[i*num_bytes:i*num_bytes+num_bytes]
            curr_ds_value = struct.unpack('>d', curr_bytes)[0]
            i += 1

        # input values are strings 
        elif data_type == 3:
            curr_bytes = dc_bitstring[i]

            # treat as INDEL
            if curr_bytes == 0:
                INDEL = True
                INDEL_bitstring = ''
                i += 1 # skip flag byte and move to INDEL
                while INDEL:
                    curr_bytes = dc_bitstring[i]
                    if curr_bytes != 0:
                        curr_ds_value = chr(curr_bytes)
                        INDEL_bitstring += curr_ds_value
                        # if curr_ds_value != None:
                        #     ds_bitstring.append(curr_ds_value)
                        # else:
                        #     print('value is of bad type, cannot deserialize')
                    else:
                        ds_bitstring.append(INDEL_bitstring)
                        INDEL = False
                    i += 1
            # treat normally (reg SNP)
            else:
                curr_ds_value = chr(curr_bytes)
                if curr_ds_value != None:
                    ds_bitstring.append(curr_ds_value)
                else:
                    print('value is of bad type, cannot deserialize')
                i += 1
    return ds_bitstring


