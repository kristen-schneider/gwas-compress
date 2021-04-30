from pyfastpfor import *
import numpy as np
import csv

def main():
    #dan()
    codec = 'simple8b_rle'
    arr_size = 128*32
    arr = [1]*arr_size
    buffer_size = 100*32
    num_blocks = 1
    out_csv = '/home/krsc0813/projects/gwas-compress/scripts/TEST.csv'
    
    codec_dict = codecs_compression_dict(num_blocks)
    kristen(codec, arr, arr_size, buffer_size, codec_dict, 0)

def kristen(codec, arr, arr_size, buffer_size, codec_dict, block_i):
    # prepare output file
    np_arr = np.array(arr, dtype = np.uint32, order = 'C')
    comp = np.zeros(arr_size+buffer_size, dtype = np.uint32, order = 'C')
    decomp = np.zeros(2*sfarr_size, dtype = np.uint32, order = 'C')
    codec_method = getCodec(codec)
    comp_size = codec_method.encodeArray(np_arr, arr_size, comp, len(comp))
    decomp_size = codec_method.decodeArray(comp, comp_size, decomp, arr_size)    
    #print('codec: ', codec)
    #print('arr: ', np_arr)
   
    compression_ratio = float(comp_size)/arr_size
    #print(codec, compression_ratio)
    try: codec_dict[codec][block_i] = compression_ratio
    except KeyError: print('cannot find codec ', codec)
    
    #print('compression ratio: ', float(comp_size)/arr_size)
   
    return decomp_size


def codecs_compression_dict(num_blocks):
    codec_dict = dict()
    for codec in getCodecList():
        codec_dict[codec] = [0]*num_blocks
    return codec_dict

if __name__ == '__main__':
    main()
