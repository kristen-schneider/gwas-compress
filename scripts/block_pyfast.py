from pyfastpfor import *
import pyfastpfor_sandbox
import generate_funnel_format
import type_handling

# in data:
#[['1', '1', '1'], ['11063', '13259', '17641'], ['T', 'G', 'G'], ['G', 'A', 'A'], ['4.213e-05', '2.984e-05', '7.127e-04'], ['4.799e-05', '2.786e-04', '8.313e-04'], ['-1.334e+00', '-1.047e+00', '-9.812e-02'], ['9.999e+00', '1.448e+00', '8.260e-01'], ['8.938e-01', '4.699e-01', '9.054e-01'], ['true', 'true', 'true']]
#[['1', '1', '1'], ['30741', '51427', '57222'], ['C', 'T', 'T'], ['A', 'G', 'C'], ['NA', 'NA', '8.637e-04'], ['NA', 'NA', '6.581e-04'], ['NA', 'NA', '6.134e-01'], ['NA', 'NA', '9.714e-01'], ['NA', 'NA', '5.277e-01'], ['NA', 'NA', 'true']]
#[['1', '1', '1'], ['58396', '62745', '63668'], ['T', 'C', 'G'], ['C', 'G', 'A'], ['0.000e+00', 'NA', '0.000e+00'], ['2.409e-04', 'NA', '2.780e-05'], ['-1.007e+00', 'NA', '-1.287e+00'], ['1.437e+00', 'NA', '4.597e+00'], ['4.833e-01', 'NA', '7.795e-01'], ['true', 'NA', 'true']]


IN_FILE = '/home/krsc0813/projects/gwas-compress/data/two_hundred_thousand.tsv'
OUT_CSV = '/home/krsc0813/projects/gwas-compress/plot_data/two_hundred_thousand.csv'
BLOCK_SIZE = 32*
NUM_COLS = 10
DELIMITER = '\t'
COL_TYPES = [1, 1, 3, 3, 2, 2, 2, 2, 2, 3]

def main():
    compression_dict = get_compression_dict()
    #write_compression_dict(compression_dict, OUT_CSV)

def write_compression_dict(compression_dict, out_f):
    o = open(out_f, 'w')
    # write header
    o.write('codec')
    for block_i in range(len(list(compression_dict.values())[0])):
        o.write(',block'+str(block_i))
    o.write('\n') 
    # write codecs and their compression ratio for each block
    for codec in compression_dict.keys():
        o.write(codec)
        for block_compression_ratio in compression_dict[codec]:
            o.write(','+str(block_compression_ratio)) 
        o.write('\n')   
    o.close()

def get_compression_dict():
    codec_list = getCodecList()
    ff = generate_funnel_format.make_all_blocks(IN_FILE, BLOCK_SIZE, NUM_COLS, DELIMITER)
    codec_dict = pyfastpfor_sandbox.codecs_compression_dict(len(ff))
    
    #single_codec_compression(ff, 'vsencoding', codec_dict)
    all_codec_compression(codec_list, ff, codec_dict)    
    
    #for c in codec_dict: print(c, codec_dict[c])
    return codec_dict
    
def all_codec_compression(codec_list, ff, codec_dict):
    for codec in codec_list:
        print(codec)
        single_codec_compression(ff, codec, codec_dict)
     
    #for c in codec_dict: print(c, codec_dict[c])

def single_codec_compression(ff, codec, codec_dict):
    for block_i in range(len(ff)):
        curr_block = ff[block_i]
        for column_i in range(len(curr_block)):
            curr_column = curr_block[column_i]
            column_type = COL_TYPES[column_i]
            typed_column = type_handling.convert_to_type(curr_column, column_type)

            # only try these codecs on integer compression
            if column_type == 1:
                #print(column_i, typed_column)
            
                #print('og: ', typed_column)
                decomp = pyfastpfor_sandbox.kristen(codec, typed_column, len(typed_column), 140*32, codec_dict, block_i)
                #print('decomp: ', decomp)
                
    #print(codec_dict)
    #arr = [1] * 200
    #pyfastpfor_test.kristen(arr)
    
if __name__ == '__main__':
    main()
