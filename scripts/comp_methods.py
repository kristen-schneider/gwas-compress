import generate_funnel_format
import struct
import gzip
import fpzip
import zfpy
import numpy as np
import compress_column
import serialize_body



def main():
'''
take in string ff data and test differnt compression methods on each column to see what is going on.

'''
    ff = generate_funnel_format.make_all_blocks('/home/krsc0813/projects/gwas-compress/data/in/ten_thousand.tsv',
                                                 10000, 10, '\t')
    
    for block in range(len(ff)):
        print('BLOCK ', block+1)
        for fc in range(4, 9):
            print('column ', fc)
            str_float_column = ff[block][fc]
            int_list = []
            for d in str_float_column:
                int_list.append(float_to_int(d))
            
            print('gzip: ', len(gzip_copression(int_list)))
            print('fpzip: ', len(fpzip_compression(int_list)))
            print('zfpy: ', len(zfpy_compression(int_list)))
            fastp_np = int_fastp_compression(int_list)
            print('fastp fpzip: ', len(fpzip_compression(fastp_np)))
            print('fastp zfpy: ', len(zfpy_compression(fastp_np)))
            print('int/fastpfor: ', len(int_fastp_compression(int_list)))       
            print('int to bytes: ', len(int_fastp_compression(int_list).tobytes(order='C')))
    #str_data = ['4.213e-05', '2.984e-05', '7.127e-04']
    #data = [4.213e-05, 2.984e-05, 7.127e-04]
    #print('gzip: ', gzip_copression(data))
    #print('fpzip: ', fpzip_compression(data))
    #print('int/fastpfor: ', int_fastp_compression(str_data))

def gzip_copression(data):
    serialized_bytes = b''
    for d in data:
        serialized_bytes+=bytearray(struct.pack("f", d))
    compressed_bytes = gzip.compress(serialized_bytes)
    return compressed_bytes

def fpzip_compression(data):
    np_data = np.array(data, dtype=np.float32)
    compressed_bytes = fpzip.compress(np_data, precision=0, order='C')
    data_again = fpzip.decompress(compressed_bytes, order='C')
    return compressed_bytes

def zfpy_compression(data):
    np_data = np.array(data, dtype=np.float32)
    compressed_bytes = zfpy.compress_numpy(np_data)
    return compressed_bytes

def int_fastp_compression(data):
    #int_list = []
    #for d in data:
    #    int_list.append(float_to_int(d))
        
    compressed_data = compress_column.compress_single_column_pyfast(data, 'fastpfor128') 
    return compressed_data   

def float_to_int(float_data):
    """
    converts a data type of float to a list of integers which can reconstruct the float

    INPUT
        float_data: data in float form (e.g. 4.213e-05)

    OUTPUT
        int_data: large integer with little endian formatting number:
        base  exp -/+
        00000 000 0
    """
    # 000000000 - little endian
    float_as_int = 0
    if float_data == 'NA':
        # choose a value that is not seen in data
        float_as_int = 999
    else:
        # base, base_sign, exponent, exponent_sign
        # 00000, 0, 00, 0,

        base_exponent = float_data.split('e')
        base = float(base_exponent[0])
        exponent = int(base_exponent[1])

        # BASE
        # base number gets proper space (e.g. 4.213 --> 42130)
        # have to do this in two steps because
        # rounding is lossy with python multiplication
        # if we just did *100000000 we would get junk in the last 4 digits
        float_as_int += abs(int(base*10000))
        float_as_int *= 10000

        # BASE SIGN
        # is number negative or positive?
        base_sign = 1  # positive
        if float(base) < 0: base_sign = 0  # negative
        float_as_int += base_sign * 1000

        # EXPONENT
        # exponents must be < 100
        # otherwise the placement of the exponent bleeds into the base/base sign
        float_as_int += abs(exponent) * 10

        # EXPONENT SIGN
        if exponent > 0: float_as_int += 1

    return float_as_int

if __name__ == '__main__': main()

# data = np.array([1.233,2.33,3.222,4.334], dtype=np.float32) # up to 4d float or double array
# # Compress data losslessly, interpreting the underlying buffer in C (default) or F order.
# compressed_bytes = fpzip.compress(data, precision=0, order='C') # returns byte string
# # Back to 3d or 4d float or double array, decode as C (default) or F order.
# data_again = fpzip.decompress(compressed_bytes, order='C')
#
# print(data)
# print(compressed_bytes)
# print(data_again)
