from pyfastpfor import *
import numpy as np

def main():
    #dan()
    codec = 'simple16'
    arr = [1]*128
    arr_size = len(arr)
    comp_size = arr_size+(16*(10*arr_size))
    print(arr_size, comp_size)
    comp = np.zeros(comp_size, dtype = np.uint32, order = 'C')
    decomp = np.zeros(arr_size, dtype = np.uint32, order = 'C')
    #r = codecs_compression(codec, arr, comp, decomp)
    loop_arr_size(codec)

def loop_arr_size(codec):
    for s in range(1, 16*5, 16):
        arr = [1]*s
        arr_size = len(arr)
        comp_size = arr_size + (16*(10*arr_size))
        comp = np.zeros(comp_size, dtype = np.uint32, order = 'C')
        decomp = np.zeros(arr_size, dtype = np.uint32, order = 'C')
        codecs_compression(codec, arr, comp, decomp)

def codecs_compression(codec, arr, comp, decomp):
    print(codec) 
    # array to numpy array
    arr_size = len(arr)
    np_arr = np.array(arr, dtype = np.uint32, order = 'C')
    # reserve space for compression and decompression
    #comp = np.zeros(arr_size+(16*10), dtype = np.uint32, order = 'C')
    #decomp = np.zeros(arr_size, dtype = np.uint32, order = 'C')
    
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
