from pyfastpfor import *
import numpy as np

def main():
    #dan()
    codec = 'simple8b_rle'
    arr_size = 128*32
    arr = [1]*arr_size
    buffer_size = 15*16
    #arr = np.ones(arr_size, dtype = np.uint32, order = 'C')
    #comp = np.zeros(arr_size+(16*10), dtype = np.uint32, order = 'C')
    #decomp = np.zeros(arr_size, dtype = np.uint32, order = 'C')    
    #r = codecs_compression(codec, arr, comp, decomp)
    #kristen(codec, arr, arr_size, buffer_size)
    dan(codec)
    #dan2(codec, arr, arr_size, buffer_size)

def kristen(codec, arr, arr_size, buffer_size):
    np_arr = np.array(arr, dtype = np.uint32, order = 'C')
    comp = np.zeros(arr_size+buffer_size, dtype = np.uint32, order = 'C')
    decomp = np.zeros(32+arr_size, dtype = np.uint32, order = 'C')
    codec_method = getCodec(codec)
    comp_size = codec_method.encodeArray(np_arr, arr_size, comp, len(comp))
    decomp_size = codec_method.decodeArray(comp, comp_size, decomp, arr_size)    
    print('codec: ', codec)
    print('arr: ', np_arr)
    print('compression ratio: ', float(comp_size)/arr_size)
    print('decomp arr: ', decomp)
    return decomp_size

def dan(curr_codec):
    arrSize = 128 * 32
    maxVal = 2048
    inp = np.array(np.random.randint(0, maxVal, arrSize), dtype = np.uint32, order = 'C')
    inpCompDecomp = np.zeros(32+arrSize, dtype = np.uint32, order = 'C')
    inpComp = np.zeros(arrSize + (1024), dtype = np.uint32, order = 'C')
    
    codec = getCodec(curr_codec)
    
    compSize = codec.encodeArray(inp, arrSize, inpComp, len(inpComp))
     
    print('Compression ratio: %g' % (float(compSize)/arrSize))
   
    codec.decodeArray(inpComp, compSize, inpCompDecomp, arrSize) 
    #assert(arrSize == codec.decodeArray(inpComp, compSize, inpCompDecomp, arrSize))
    #assert(np.all(inpCompDecomp == inp))
    #print('inpCompDecomp: ', len(inpCompDecomp), inpCompDecomp)

def dan2(curr_codec):
    arrSize = 128 * 32
    maxVal = 2048
    inp = np.ones(arrSize, dtype = np.uint32, order = 'C')
    #inp = np.zeros(arrSize, dtype = np.uint32, order = 'C')
    #inp = np.array(np.random.randint(0, maxVal, arrSize), dtype = np.uint32, order = 'C')
    #print('inp: ', len(inp), inp)
    inpCompDecomp = np.zeros(32+arrSize, dtype = np.uint32, order = 'C')
    inpComp = np.zeros(arrSize + (1024), dtype = np.uint32, order = 'C')
    
    codec = getCodec(curr_codec)
    
    compSize = codec.encodeArray(inp, arrSize, inpComp, len(inpComp))
    #print('inpComp: ', len(inpComp), inpComp)
     
    print('Compression ratio: %g' % (float(compSize)/arrSize))
   
    codec.decodeArray(inpComp, compSize, inpCompDecomp, arrSize) 
    #assert(arrSize == codec.decodeArray(inpComp, compSize, inpCompDecomp, arrSize))
    #assert(np.all(inpCompDecomp == inp))
    #print('inpCompDecomp: ', len(inpCompDecomp), inpCompDecomp)



if __name__ == '__main__':
    main()
