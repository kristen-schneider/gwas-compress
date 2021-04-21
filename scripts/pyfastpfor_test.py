from pyfastpfor import *
import numpy as np

def main():
    #dan()
    col_num = 1
    arr = [11063, 13259, 17641, 30741, 51427, 57222, 58396, 62745, 63668, 64658, 65024, 65030, 69487, 69569, 73269, 77470, 79192, 85435, 91588, 108658, 139853, 533573, 541944, 542210, 564777, 565056, 565148, 565169, 566012, 567474, 567851, 568211, 569523, 569821, 570578, 601158, 604020, 610420, 615095, 643523, 646531, 651203, 668332, 672798, 672859, 691545, 692794, 693731, 706425, 706992, 707014, 707522, 713698, 713979, 714596, 714856, 715265, 715300, 715367, 715804, 715925, 717485, 717587, 718638, 719077, 720026, 720381, 720681, 721290, 721891, 722519, 723329, 723891, 726794, 728681, 729632, 729679, 730087, 730779, 731718, 731959, 732030, 732032, 732049, 732882, 733652, 733895, 734314, 734332, 734338, 734349, 734914, 734988, 735267, 735636, 735663, 735899, 736289, 736304]
    #arr = [58396, 62745, 63668]
    #arr = [100000] * 3
    out_f = '/home/krsc0813/projects/gwas-compress/plot_data/'
    kristen(col_num, arr, out_f)

def kristen(col_num, arr, out_f):
    # codecs list minus thee 4 codecs that generate an error
    #codecs_list = ['BP32', 'copy', 'fastbinarypacking16', 'fastbinarypacking32', 'fastbinarypacking8', 'fastpfor128', 'fastpfor256', 'maskedvbyte', 'newpfor', 'optpfor', 'pfor', 'pfor2008', 'simdbinarypacking', 'simdfastpfor128', 'simdfastpfor256', 'simdgroupsimple', 'simdgroupsimple_ringbuf', 'simdnewpfor', 'simdoptpfor', 'simdpfor', 'simdsimplepfor', 'simple8b', 'simple8b_rle', 'simplepfor', 'streamvbyte', 'varint', 'varintg8iu', 'varintgb', 'vbyte']
    # full codecs list
    codecs_list = ['BP32', 'copy', 'fastbinarypacking16', 'fastbinarypacking32', 'fastbinarypacking8', 'fastpfor128', 'fastpfor256', 'maskedvbyte', 'newpfor', 'optpfor', 'pfor', 'pfor2008', 'simdbinarypacking', 'simdfastpfor128', 'simdfastpfor256', 'simdgroupsimple', 'simdgroupsimple_ringbuf', 'simdnewpfor', 'simdoptpfor', 'simdpfor', 'simdsimplepfor', 'simple16', 'simple8b', 'simple8b_rle', 'simple9', 'simple9_rle', 'simplepfor', 'streamvbyte', 'varint', 'varintg8iu', 'varintgb', 'vbyte', 'vsencoding']
    
    performance_file = open(out_f+'codecs_performance-' + str(col_num) + '.tsv', 'w')
    performance_file.truncate()
    #print(col_num, arr, out_f)
    # compression method
    for c in range(len(codecs_list)):
        # in array
        #arr = [1]*200#,1,1,1,1]
        arr_size = len(arr)
        np_arr = np.array(arr, dtype = np.uint32, order = 'C')
        
        # reserve space for compression and decompression
        comp = np.zeros(arr_size+1024, dtype = np.uint32, order = 'C')
        decomp = np.zeros(arr_size, dtype = np.uint32, order = 'C')
        
        # codec: compression type
        codec = getCodec(codecs_list[c])
        
        # compress data
        comp_size = codec.encodeArray(np_arr, arr_size, comp, len(comp))
        performance_file.write(codecs_list[c] + '\t' + 
            '%g' % (float(comp_size)/arr_size) + '\n')
        #print(str(c) + '. ' + codecs_list[c] + ' compression ratio: %g' % (float(comp_size)/arr_size))
        #print(c + ': ', 'compression ratio: %g' % (float(comp_size)/arr_size))
    
        # decompress data
        #print('arr: ', np_arr)
        #print('comp: ', comp)
        #print('decomp: ', decomp)
        #assert(arr_size == codec.decodeArray(comp, comp_size, decomp, arr_size))
        #print(codecs_list[c])
        #print('arr: ', np_arr)
        #print('comp: ', comp)
        #print('decomp: ', decomp)
        #assert(np.all(decomp == np_arr))
        #print(codecs_list[c])
 
if __name__ == '__main__':
    main()
