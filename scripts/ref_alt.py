from collections import OrderedDict

ref_alt_file = '/home/krsc0813/projects/gwas-compress/data/ref-alt-all.tsv'
#ref_alt_file = '/Users/kristen/Desktop/compression_sandbox/toy_data_in/ref-alt.tsv'
def main():
    print_long(ref_alt_file)
    print_long('/home/krsc0813/projects/gwas-compress/data/ref-alt-int.tsv')

def print_long(f_name):
    f = open(f_name, 'r')
    for line in f:
        A = line.rstrip().split()
        ref = A[0]
        alt = A[1]

        if len(ref) > 400 or len(alt) > 400: print('ref: ', ref, 'alt: ', alt)

def base_rle():
    header = ''
    f = open(ref_alt_file, 'r')
    print('ref','ref_i','alt','alt_i')
    for line in f:
        ref = ''
        alt = ''
        i_ref = 0
        i_alt = 0
        if header == '': header = line
        else:
            A = line.rstrip().split()
            ref = A[0]
            alt = A[1]
            i_ref = run_length_encoding(ref)
            i_alt = run_length_encoding(alt)
            print(i_ref, i_alt)

def run_length_encoding(indel):
    rle = ''
    prev_b = ''
    i_count = 1

    for b in indel:
        # first base
        if rle == '':
            i = base_to_int(b)
            rle += str(i)
        else:
            if b == prev_b:
                i_count += 1
            else:
                rle += str(i_count)
                i_count = 1
                
                i = base_to_int(b)
                rle += str(i)
                
        prev_b = b
    rle += str(i_count)
    
    return int(rle)

        
def base_to_int(base):
    i = None
    if base == 'A': i = 1
    elif base == 'C': i = 2
    elif base == 'G': i = 3
    elif base == 'T': i = 4
    else: print(base, 'not a valid base')
    return i

def get_maximums():
    header = ''
    max_len_ref = 0
    max_ref = ''
    max_len_alt = 0
    max_alt = ''

    f = open(ref_alt_file, 'r')
    for line in f:
        if header == '': header = line
        else:
            A = line.rstrip().split()
            ref = A[0]
            alt = A[1]
            
            if len(ref) > max_len_ref:
                max_len_ref = len(ref)
                max_ref = ref
            if len(alt) > max_len_alt:
                max_len_alt = len(alt)
                max_alt = alt
    print('ref: ', max_ref, max_len_ref)
    print('alt: ', max_alt, max_len_alt)
    


 
    

if __name__ == '__main__':
    main()
