import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


from utils import type_handling
import struct
import numpy as np

# when float data is NA, int data is [0,-999]
# when string data is NA, int data is -1

def deserialize_list(dc_bitstring, block_size, data_type, num_bytes, chrm):
    """
    deserializes data for one column. incoming data is all in form of integers,
     but we must return values that match original data

    INPUT
        dc_bitstring = decompressed bitstring for one column
        block_size = number of rows in a block (size of output column)
        data_type = type of data in this column (1,2,3,4)
        num_bytes = number of bytes that is associated with this data type

    OUTPUT
        ds_bitstring = deserialized data for one column (e.g. [1,1,1,1,1]
    """
    ds_bitstring = []
    if data_type == 1:
        ds_bitstring = deserialize_int(dc_bitstring, block_size, num_bytes, chrm)
    elif data_type == 2:
        ds_bitstring = deserialize_float(dc_bitstring, block_size, num_bytes)
    elif data_type == 3 or data_type == 4:
        ds_bitstring = deserialize_string(dc_bitstring)
    else:
        ds_bitstring = dc_bitstring

    return ds_bitstring


def deserialize_int(dc_bitstring, block_size, num_bytes, chrm):
    """
    takes serialized integer data and converts to integers.
    accounts for X and Y chromosomes being 23 and 24, respectfully
    """
    ds_bitstring = []
    # for every piece of data in a given block
    for i in range(block_size):
        curr_bytes = dc_bitstring[i * num_bytes:i * num_bytes + num_bytes]
        # these values are chromosomes and positions and should not be negative.
        curr_ds_value = int.from_bytes(curr_bytes, byteorder='big', signed=False)
        #if curr_ds_value == 23:
        #    curr_ds_value = 'X'
        #elif curr_ds_value == 24:
        #    curr_ds_value = 'Y'
        ds_bitstring.append(curr_ds_value)
    return ds_bitstring


def deserialize_float(dc_bitstring, block_size, num_bytes):
    """

    """
    ds_bitstring = []
    for i in range(block_size):
        curr_bytes = dc_bitstring[i * num_bytes:i * num_bytes + num_bytes]
        curr_ds_value = int.from_bytes(curr_bytes, byteorder='big', signed=True)
        # convert int back to float
        ds_float = type_handling.int_to_float(curr_ds_value)
        ds_bitstring.append(ds_float)

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
            i += 1  # skip flag byte and move to INDEL
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
