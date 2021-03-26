import type_handling
import struct

def deserialize_block(dc_bitstring, block_size, column_data_types, type_to_bytes_code_book, column_lengths):
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

        #column_length = type_handling.get_bitstring_length_by_data_type(block_size, column_data_type, column_bytes)
        column_length = column_lengths[c]
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
    
    # #for i in range(block_size):
    # loop = len(dc_bitstring)
    # i = 0
    # while i < loop:
    #     # input values are integers
    if data_type == 1:
        ds_bitstring = deserialize_int(dc_bitstring, block_size, num_bytes)
        # for chromosome X,Y values
        if ds_bitstring[0] == 'XY':
            ds_bitstring_ints = ds_bitstring[1]
            xy_start = ds_bitstring[2]*num_bytes
            xy_segment = dc_bitstring[xy_start:]
            ds_bitstring_chrmXY = deserialize_string(xy_segment)
            ds_bitstring = ds_bitstring_ints + ds_bitstring_chrmXY

    elif data_type == 2:
        ds_bitstring = deserialize_float(dc_bitstring, block_size, num_bytes)
    elif data_type == 3:
        ds_bitstring = deserialize_string(dc_bitstring)
    elif data_type == 4:
        ds_bitstring = dc_bitstring

    return ds_bitstring


def deserialize_int(dc_bitstring, block_size, num_bytes):
    ds_bitstring = []
    for i in range(block_size):
        curr_bytes = dc_bitstring[i*num_bytes:i*num_bytes+num_bytes]
        if b'X' in curr_bytes or b'Y' in curr_bytes:
            return ['XY', ds_bitstring, i]
        curr_ds_value = int.from_bytes(curr_bytes, byteorder='big', signed=False)
        ds_bitstring.append(curr_ds_value)
    return ds_bitstring

def deserialize_float(dc_bitstring, block_size, num_bytes):
    ds_bitstring = []
    for i in range(block_size):
        curr_bytes = dc_bitstring[i * num_bytes:i * num_bytes + num_bytes]
        curr_ds_value = struct.unpack('>d', curr_bytes)[0]
        ds_bitstring.append(curr_ds_value)
    return ds_bitstring

def deserialize_string(dc_bitstring):
    ds_bitstring = []
    loop = len(dc_bitstring)
    i = 0
    while i < loop:
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

#
# a = b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01'
# dsa = deserialize_data(a, 5, 1, 5)
# print(dsa)
# b = b'?\xf3333333@\x0b\x99\x99\x99\x99\x99\x9a\xc0\x1b\x1e\xb8Q\xeb\x85\x1f?\x17\x97\xcc9\xff\xd6\x0f@\xc8\x1a\x00\x00\x00\x00\x00'
# dsb = deserialize_data(b, 5, 2, 8)
# print(dsb)
# c = b'AC\x00TTT\x00GA'
# dsc = deserialize_data(c, 5, 3, 5)
# print(dsc)


