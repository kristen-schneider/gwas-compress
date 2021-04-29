from pyfastpfor import *
import numpy as np
import csv

def main():
    #dan()
    codec = 'simple8b_rle'
    arr_size = 128*32
    arr = [1]*arr_size
    buffer_size = 15*16
    num_blocks = 1
    out_csv = '/home/krsc0813/projects/gwas-compress/scripts/TEST.csv'
    csv_codec_column(getCodecList(), out_csv, num_blocks)
    kristen(codec, arr, arr_size, buffer_size, out_csv)

def kristen(codec, arr, arr_size, buffer_size, out_csv):
    # prepare output file
    np_arr = np.array(arr, dtype = np.uint32, order = 'C')
    comp = np.zeros(arr_size+buffer_size, dtype = np.uint32, order = 'C')
    decomp = np.zeros(32+arr_size, dtype = np.uint32, order = 'C')
    codec_method = getCodec(codec)
    comp_size = codec_method.encodeArray(np_arr, arr_size, comp, len(comp))
    decomp_size = codec_method.decodeArray(comp, comp_size, decomp, arr_size)    
    #print('codec: ', codec)
    #print('arr: ', np_arr)
    
    compression_ratio = float(comp_size)/arr_size
    #with open(out_csv, 'w') as o:
    #    writer = csv.writer(o, lineterminator='\n')
        #writer.write
        #row = next(writer)
        #print(row)
        #row.append()
        #if first_block
        #print('compression ratio: ', float(comp_size)/arr_size)
   
    #print('decomp arr: ', decomp)
    return decomp_size


def csv_codec_column(codec_list, out_csv, num_blocks):
    # generate header
    header = generate_header(num_blocks)
    # write header
    with open(out_csv, 'w') as o:
        o.truncate(0)
        csv_writer = csv.writer(o, lineterminator='\n')
        csv_writer.writerow(header)
    o.close()
    with open(out_csv, 'a') as o:
        csv_writer = csv.writer(o, lineterminator='\n')
        for codec in codec_list:
            csv_writer.writerow([codec])

def generate_header(num_blocks):
    header = ['codec']
    for i in range(num_blocks):
        header.append('block-'+str(i))
    return header 

if __name__ == '__main__':
    main()
