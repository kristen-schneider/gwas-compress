from pyfastpfor import *
import numpy as np

def main():
    #dan()
    kristen()

def kristen():
    # codecs list
    ['BP32', 'copy', 'fastbinarypacking16', 'fastbinarypacking32', 'fastbinarypacking8', 'fastpfor128', 'fastpfor256', 'maskedvbyte', 'newpfor', 'optpfor', 'pfor', 'pfor2008', 'simdbinarypacking', 'simdfastpfor128', 'simdfastpfor256', 'simdgroupsimple', 'simdgroupsimple_ringbuf', 'simdnewpfor', 'simdoptpfor', 'simdpfor', 'simdsimplepfor', 'simple16', 'simple8b', 'simple8b_rle', 'simple9', 'simple9_rle', 'simplepfor', 'streamvbyte', 'varint', 'varintg8iu', 'varintgb', 'vbyte', 'vsencoding']
    codecs_list = getCodecList()
    
    # in array
    arr = [1]*200#,1,1,1,1]
    arr_size = len(arr)
    np_arr = np.array(arr, dtype = np.uint32, order = 'C')
    
    comp = np.zeros(arr_size+1024, dtype = np.uint32, order = 'C')
    decomp = np.zeros(arr_size, dtype = np.uint32, order = 'C')
   
    # compression method
    for c in range(len(codecs_list)):
        # codec: compression type
        #print(c)
        codec = getCodec(codecs_list[c])
        
        # compress data
        comp_size = codec.encodeArray(np_arr, arr_size, comp, len(comp))
        print(str(c) + '. ' + codecs_list[c] + 'Compression ratio: %g' % (float(comp_size)/arr_size))

        # decompress data
        #print('arr: ', np_arr)
        #print('comp: ', comp)
        #print('decomp: ', decomp)
        #assert(arr_size == codec.decodeArray(comp, comp_size, decomp, arr_size))
        #print('arr: ', np_arr)
        #print('comp: ', comp)
        #print('decomp: ', decomp)
        #assert(np.all(decomp == np_arr))
 
    #codec = getCodec('simdbinarypacking')

    # Compress data
    #comp_size = codec.encodeArray(np_arr, arr_size, comp, len(comp))
    #compSize = codec.encodeArray(inp, len(inp), inpCompDecomp, len(inpCompDecomp)) 

    #print('Compression ratio: %g' % (float(comp_size)/arr_size))

    # Decompress data
    #print('arr: ', np_arr)
    #print('comp: ', comp)
    #print('decomp: ', decomp)
    #assert(arr_size == codec.decodeArray(comp, comp_size, decomp, arr_size))
    #print('arr: ', np_arr)
    #print('comp: ', comp)
    #print('decomp: ', decomp)
    #assert(np.all(decomp == np_arr))
    # compression method
    #for c in codecs_list:
    #    print(c)
    #    codec = getCodec(c)
    
    

def dan():
    arr = [1]*200#,1,1,1,1]
    arrSize = len(arr)
    maxVal = 20
    # 1. Example without data differencing

    # All arrays the library use must be contiguous-memory C-style numpy arrays
    #inp = np.array(np.random.randint(0, maxVal, arrSize), dtype = np.uint32, order = 'C')
    inp = np.array(arr, dtype = np.uint32, order = 'C')
    #rinp = np.array(np.random.randint(0, maxVal, arrSize), dtype = np.uint32, order = 'C')
    inpCompDecomp = np.zeros(arrSize, dtype = np.uint32, order = 'C')

    # To be on the safe side, let's reserve plenty of additional memory:
    # sometimes the size of compressed data is not smaller than the size 
    # of the original one
    inpComp = np.zeros(arrSize, dtype = np.uint32, order = 'C')

    # Obtain a codec by name
    codec = getCodec('simdbinarypacking')
    print(codec)
    # Compress data
    compSize = codec.encodeArray(inp, arrSize, inpComp, len(inpComp))
    #compSize = codec.encodeArray(inp, len(inp), inpCompDecomp, len(inpCompDecomp)) 

    print('Compression ratio: %g' % (float(compSize)/arrSize))

    # Decompress data
    print('inp: ', len(inp), inp)
    print('inpCompDecomp: ', len(inpCompDecomp), inpCompDecomp)
    print('inpComp: ', len(inpComp), inpComp)
    
    assert(arrSize == codec.decodeArray(inpComp, compSize, inpCompDecomp, arrSize))
    assert(np.all(inpCompDecomp == inp))

    print('arr size decomp: ', arrSize)
    print('inp: ', len(inp), inp)
    print('inpCompDecomp: ', len(inpCompDecomp), inpCompDecomp)
    print('inpComp: ', len(inpComp), inpComp)
if __name__ == '__main__':
    main()
