import type_handling
import struct


def deserialize_list(dc_bitstring, block_size, data_type, num_bytes, chrm):
    """
    deserializes data for one column

    INPUT
        dc_bitstring = decompressed bitstring for one column
        block_size = number of rows in a block (size of output column)
        data_type = type of data in this column (1,2,3)
        num_bytes = number of bytes that is associated with this data type

    OUTPUT
        ds_bitstring = deserialized data for one column (e.g. [1,1,1,1,1]
    """
    ds_bitstring = []
    
    if data_type == 1:
        ds_bitstring = deserialize_int(dc_bitstring, block_size, num_bytes, chrm)
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


def deserialize_int(dc_bitstring, block_size, num_bytes, chrm):
    ds_bitstring = []
    for i in range(block_size):
        curr_bytes = dc_bitstring[i*num_bytes:i*num_bytes+num_bytes]
        if chrm and (b'X' in curr_bytes or b'Y' in curr_bytes):
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
