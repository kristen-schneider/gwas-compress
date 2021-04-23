from pyfastpfor import *
import numpy as np

def main():
    #dan()
    codec = 'simple16'
    arr = [1]*128
    r = codecs_compression(codec, arr)

def codecs_compression(codec,arr):
    # array to numpy array
    arr_size = len(arr)
    np_arr = np.array(arr, dtype = np.uint32, order = 'C')
    
    # reserve space for compression and decompression
    comp = np.zeros(arr_size+(16*10), dtype = np.uint32, order = 'C')
    decomp = np.zeros(arr_size, dtype = np.uint32, order = 'C')
    
    # codec: compression type
    codec_method = getCodec(codec)
    # BUG
    #print('arr: ', arr)
    #print('comp: ', comp)
    #print('decomp: ', decomp)
    
    # compression
    comp_size = codec_method.encodeArray(np_arr, arr_size, comp, len(comp))
    # BUG
    #print('arr: ', arr)
    #print('comp: ', comp)
    #print('decomp: ', decomp)
    
    # decompression
    codec_method.decodeArray(comp, comp_size, decomp, arr_size)
    # BUG
    #print('arr: ', arr)
    #print('comp: ', comp)
    #print('decomp: ', decomp)

    #return decomp

if __name__ == '__main__':
    main()
