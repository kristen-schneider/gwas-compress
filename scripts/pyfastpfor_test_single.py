from pyfastpfor import *
import numpy as np

def main():
    #dan()
    codec = 'BP32'
    arr_size = 128*32
    arr = [1]*arr_size
    buffer_size = 150*16
    #arr = np.ones(arr_size, dtype = np.uint32, order = 'C')
    #comp = np.zeros(arr_size+(16*10), dtype = np.uint32, order = 'C')
    #decomp = np.zeros(arr_size, dtype = np.uint32, order = 'C')    
    #r = codecs_compression(codec, arr, comp, decomp)
    kristen(codec, arr, arr_size, buffer_size)
    #dan()
    #dan2(codec, arr_size, buffer_size)

def kristen(codec, arr, arr_size, buffer_size):
    np_arr = np.array(arr, dtype = np.uint32, order = 'C')
    comp = np.zeros(arr_size+buffer_size, dtype = np.uint32, order = 'C')
    decomp = np.zeros(arr_size, dtype = np.uint32, order = 'C')
    codec_method = getCodec(codec)
    comp_size = codec_method.encodeArray(np_arr, arr_size, comp, len(comp))
    decomp_size = codec_method.decodeArray(comp, comp_size, decomp, arr_size)    
    print('codec: ', codec)
    print('compression ratio: ', float(comp_size)/arr_size)
    return decomp_size

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

def dan():
    arrSize = 128 * 32
    maxVal = 1000
    #inp = np.zeros(arrSize, dtype = np.uint32, order = 'C')
    inp = np.array(np.random.randint(100, maxVal, arrSize), dtype = np.uint32, order = 'C')
    print(inp)
    inpCompDecomp = np.zeros(arrSize, dtype = np.uint32, order = 'C')

    inpComp = np.zeros(arrSize + (16*1000), dtype = np.uint32, order = 'C')
    
    codec = getCodec('simple16')
    
    compSize = codec.encodeArray(inp, arrSize, inpComp, len(inpComp))
     
    print('Compression ratio: %g' % (float(compSize)/arrSize))
    
    assert(arrSize == codec.decodeArray(inpComp, compSize, inpCompDecomp, arrSize))
    assert(np.all(inpCompDecomp == inp))

def dan2(inCodec, arr, arrSize, buffer_size):
    #arrSize = 128 * 32
    #maxVal = 2048

    inp = np.array(arr, dtype = np.uint32, order = 'C')
    #inp = np.array(np.random.randint(0,10,arrSize), dtype = np.uint32, order = 'C')
    inpCompDecomp = np.zeros(arrSize, dtype = np.uint32, order = 'C')

    inpComp = np.zeros(arrSize + buffer_size, dtype = np.uint32, order = 'C')
    
    codec = getCodec(inCodec)
    
    compSize = codec.encodeArray(inp, arrSize, inpComp, len(inpComp))
     
    print('Compression ratio: %g' % (float(compSize)/arrSize))
    
    assert(arrSize == codec.decodeArray(inpComp, compSize, inpCompDecomp, arrSize))
    assert(np.all(inpCompDecomp == inp))



if __name__ == '__main__':
    main()
