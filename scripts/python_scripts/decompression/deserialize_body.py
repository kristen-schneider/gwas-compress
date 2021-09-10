import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


from utils import type_handling
import struct
import numpy as np

# when float data is NA, int data is [0,-999]
# when string data is NA, int data is -1

def deserialize_list(dc_bitstring, block_size, compression_data_type, decompression_data_type, num_bytes, chrm):
    """
    deserializes data for one column. incoming data is all in form of integers,
     but we must return values that match original data

    INPUT
        dc_bitstring = decompressed bitstring for one column
        block_size = number of rows in a block (size of output column)
        data_type = type of data this column was compressed as (1,2,3,4)
        num_bytes = number of bytes that is associated with this data type

    OUTPUT
        ds_bitstring = deserialized data for one column (e.g. [1,1,1,1,1]
    """
    ds_bitstring = []
    if compression_data_type == 1:
        ds_bitstring = deserialize_int(dc_bitstring, block_size, num_bytes, chrm)
    elif compression_data_type == 2:
        ds_bitstring = deserialize_float(dc_bitstring, block_size, num_bytes)
    elif compression_data_type == 3:
        ds_bitstring = deserialize_string(dc_bitstring)#, num_bytes)
    elif compression_data_type == 4:
        ds_bitstring = dc_bitstring
    else:
        print('invalid data type: ', data_type)
        return -1
    return ds_bitstring

def deserialize_list_fastpfor(dc_bitstring):
    ds_bitstring = np.frombuffer(dc_bitstring, dtype=np.uint32)
    return ds_bitstring 

def deserialize_int(dc_bitstring, block_size, num_bytes, chrm):
    """
    takes serialized integer data and converts to integers.
    accounts for X and Y chromosomes being 23 and 24, respectfully
    """
    ds_bitstring = []
    # ds_bitstring = np.frombuffer(dc_bitstring, dtype=np.uint32)
    #for every piece of data in a given block
    for i in range(block_size):
        curr_bytes = dc_bitstring[i * num_bytes:i * num_bytes + num_bytes]
        #print(i, curr_bytes)
        #these values are chromosomes and positions and should not be negative.
        # curr_ds_value = np.frombuffer(curr_bytes, dtype=np.uint32)
        curr_ds_value = b''
        #print(np.frombuffer(dc_bitstring, dtype=np.uint32))
        if curr_ds_value == 23:
           curr_ds_value = 'X'
        elif curr_ds_value == 24:
           curr_ds_value = 'Y'
        else:
            curr_ds_value = int.from_bytes(curr_bytes, byteorder='big', signed=False)
        ds_bitstring.append(curr_ds_value)
    return ds_bitstring

def deserialize_int_fastpfor(dc_bitstring, block_size, num_bytes, chrm):
    """
    takes serialized integer data and converts to integers.
    accounts for X and Y chromosomes being 23 and 24, respectfully
    """
    ds_bitstring = np.frombuffer(dc_bitstring, dtype=np.uint32)
    return ds_bitstring


def deserialize_float(dc_bitstring, block_size, num_bytes):
    """

    """
    ds_bitstring = []
    num_elements = int(len(dc_bitstring)/num_bytes)
    for i in range(num_elements):
        curr_bytes = dc_bitstring[i * num_bytes:i * num_bytes + num_bytes]
        curr_ds_value = int.from_bytes(curr_bytes, byteorder='big', signed=True)
        ds_bitstring.append(curr_ds_value)
     
    return ds_bitstring


def deserialize_string(dc_bitstring):
    split_string = dc_bitstring.decode("utf-8").replace('\x00\x00', '\x00').replace('\x00', ' ').strip().split(' ')
    return dc_bitstring.decode("utf-8")

#print(b'\x0011063\x00\x0013259\x00\x0017641\x00'.decode("utf-8").replace('\x00\x00', '\x00').replace('\x00', ' ').strip().split(' ')
