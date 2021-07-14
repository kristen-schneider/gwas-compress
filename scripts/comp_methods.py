import generate_funnel_format
import type_handling
import compress_column
import serialize_body
import packed_strings

import struct
import gzip
import fpzip
import zfpy
import numpy as np



def main():
    '''
    take in string ff data and test different
    compression methods on each column to see what is going on.
    '''
    print('funnel format computing...')
    ff = generate_funnel_format.make_all_blocks('/home/krsc0813/projects/gwas-compress/data/in/ten_thousand.tsv',
                                                 10000, 10, '\t')
    print('funnel format complete.')
    
    out_f_dir = '/home/krsc0813/projects/gwas-compress/plot_data/compression_methods/'    

    all_f = open(out_f_dir+'all_methods_test.tsv', 'a')
    all_f.truncate(0)
    all_f.write('gzip(int)\tgzip(string)\tfpzip\tzfpy\tfastpfor128\t')
    all_f.write('\n')
    
    # for each block
    for block in range(len(ff)):
        all_f.write('BLOCK ' + str(block+1) + '\n')
        
        # for each column
        for c in range(len(ff[0])):
            str_column = ff[block][c]  # column as string data
                        
            print('integer conversion...')
            int_column = []     # column as int data
            # int columns
            if c < 2:
                for s in str_column:
                    int_column.append(type_handling.int_to_int(s))    
            # float columns
            elif c > 3 and c < 9:
                for s in str_column:
                    int_column.append(type_handling.float_to_int(s))
            # true/false columns
            elif c == 9:
                for s in str_column:
                    int_column.append(type_handling.string_to_int(s))        
            # ref/alt columns
            else:
                int_column = packed_strings.encode_column(str_column)
            print('integer conversion complete.')
            
            #fastp_np = fastp_compression(int_column)
            all_f.write(str(len(gzip_compression(int_column, 1)))+'\t')
            all_f.write(str(len(gzip_compression(str_column, 3)))+'\t') 
            all_f.write(str(len(fpzip_compression(int_column)))+'\t')
            all_f.write(str(len(zfpy_compression(int_column)))+'\t')
            all_f.write(str(len(fastp_compression(int_column).tobytes(order='C')))+'\n')
            #print('gzip: ', len(gzip_copression(int_column)))
            #print('fpzip: ', len(fpzip_compression(int_column)))
            #print('zfpy: ', len(zfpy_compression(int_column)))
            # print('fastp fpzip: ', len(fpzip_compression(fastp_np)))
            # print('fastp zfpy: ', len(zfpy_compression(fastp_np)))
            # print('int/fastpfor: ', len(int_fastp_compression(int_list)))
            #print('int to bytes: ', len(int_fastp_compression(int_column).tobytes(order='C')))
        
        all_f.write('\n')

    
    #str_data = ['4.213e-05', '2.984e-05', '7.127e-04']
    #data = [4.213e-05, 2.984e-05, 7.127e-04]
    #print('gzip: ', gzip_copression(data))
    #print('fpzip: ', fpzip_compression(data))
    #print('int/fastpfor: ', int_fastp_compression(str_data))

def gzip_compression(data, data_type):
    serialized_bytes = b''
    for d in data:
        serialized_bytes+=serialize_body.serialize_list(data, data_type, 4)
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

def fastp_compression(data):
    #int_list = []
    #for d in data:
    #    int_list.append(float_to_int(d))
        
    compressed_data = compress_column.compress_single_column_pyfast(data, 'fastpfor128') 
    return compressed_data   

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
