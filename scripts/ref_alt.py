# https://wiki.python.org/moin/BitwiseOperators
# https://wiki.python.org/moin/BitArrays
import math
def main():
    # assumption1('/Users/kristen/Desktop/compression_sandbox/toy_data_in/ref-alt.tsv')
    # data = ['AAAAA']*1
    data = ['T', 'G', 'G', 'C', 'T', 'T', 'T', 'C', 'G', 'A',
             'CT',
             'A', 'G', 'T', 'T', 'T', 'T', 'G', 'G', 'G', 'C', 'G', 'T', 'C', 'A', 'A',
             'T', 'T', 'C', 'A', 'G', 'A', 'C', 'A', 'G', 'G',
             'A']
    x = col_input(data)
    print(x)

def col_input(column):
    """
    takes a full column of ref/alt bases and finds an element to encode; and then encodes it
        1. 15 SNVs in a row
        2. < 15 SNVs in a row
        3. INDEL
    returns list of integers
    """
    list_ints = []
    SNVs = []
    for row in column:
        # only SNV
        if len(row) == 1:
            SNVs.append(row)
            # 15 SNVs in a row
            if len(SNVs) == 15:
                SNV_bitstring = encode_SNVs(SNVs)
                start_bitstring = shift_bit(0, 30)
                full_bitstring = start_bitstring | SNV_bitstring
                list_ints.append(full_bitstring)
                SNVs = []

        # encountered an INDEL
        else:
            # handle any SNVs we have collected
            if len(SNVs) > 0:
                start_bitstring = shift_bit(2, 30)
                len_SNVs = shift_bit(len(SNVs), 20)
                SNV_bitstring = encode_SNVs(SNVs)
                full_bitstring = start_bitstring | len_SNVs | SNV_bitstring
                list_ints.append(full_bitstring)
                SNVs = []

            # handle INDEL we encountered
            INDEL = row
            INDEL_bitstring_info = encode_INDEL(INDEL)
            # first bitstring will need to include data about how long the INDEL is and such (for decoding)
            head_bitstring = INDEL_bitstring_info[0]
            tail_bitstrings = INDEL_bitstring_info[1:]
            list_ints.append(head_bitstring)
            for t in tail_bitstrings: list_ints.append(t)
    # handle any SNVs left
    if len(SNVs) > 0:
        start_bitstring = shift_bit(2, 30)
        len_SNVs = shift_bit(len(SNVs), 20)
        SNV_bitstring = encode_SNVs(SNVs)
        full_bitstring = start_bitstring | len_SNVs | SNV_bitstring
        list_ints.append(full_bitstring)

    return list_ints


def shift_bit(bitstring, shift):
    """
    shifting for little endian format
    """
    return bitstring << shift


def encode_SNVs(SNVs):
    """
    given a list of SNVs, convert to int
    """
    snv_bitstring = 0
    for v in range(len(SNVs)):
        # get proper bit representation for the variant
        snv = shift_bit(get_variant_number(SNVs[v]), 2*v) | snv_bitstring
        # if we are on first snv, set bitstring
        if v == 0:
            snv_bitstring = snv
        else:
            snv_bitstring = snv_bitstring | snv
    return snv_bitstring


def encode_INDEL(INDEL):
    indel_bitstring = []
    start_indel = 0
    end_indel = 10
    start_bitstring = shift_bit(3, 30)
    len_INDEL = shift_bit(len(INDEL), 20)
    if len(INDEL) > 10:
        num_ints = math.ceil(int(len(INDEL)-10)/16) + 1
        for i in range(num_ints):
            # take first ten and add, then take 16 at a time
            if i == 0:
                first_ten = INDEL[start_indel:end_indel]
                first_ten_bitstring = encode_SNVs(first_ten)
                indel_bitstring.append(start_bitstring | len_INDEL | first_ten_bitstring)
            else:
                INDEL = INDEL[start_indel:end_indel]
                start_bitstring = shift_bit(0, 30)
                indel_bitstring.append(start_bitstring | encode_SNVs(INDEL))
            start_indel = end_indel
            end_indel += 16

    else:
        start_bitstring = shift_bit(3, 30)
        # treat it as a list of SNPs
        x = len(INDEL)
        len_INDEL = shift_bit(len(INDEL), 20)
        indel_bitstring.append(start_bitstring | len_INDEL | encode_SNVs(INDEL))
    return indel_bitstring


def get_variant_number(base):
    if (base == 'A'):
        return 0
    elif (base == 'C'):
        return 1
    elif (base == 'G'):
        return 2
    elif (base == 'T'):
        return 3
    else:
        print('not a proper base')
        return -1

ref_alt_txt = ''
def assumption1(ref_alt_txt):
    # 1. 1 bit: fifteen consecutive snps
    # 2. 1 bit: snv or indel
    # 3.a. 30 bits: snvs (up to 15)
    # 3.b.i 10 bits: length of indel OR SNVs
    # 3.b.ii 20 bits: snvs (up to 10)

    # assumptions for round 1 is that we pack 16 snvs into one int.
    f = open(ref_alt_txt, 'r')
    all_refs = []
    all_alts = []
    for line in f:
        A = line.rstrip().split()
        ref = A[0]
        all_refs.append(ref)
        alt = A[1]
        all_alts.append(alt)
    int_refs = col_input(all_refs)
    int_alts = col_input(all_alts)
    print('reference as str: ', len(all_refs), all_refs)
    print('reference as int: ', len(int_refs), int_refs)
    print('alternate as str: ', len(all_alts), all_alts)
    print('alternate as int: ', len(int_alts), int_alts)



if __name__ == '__main__':
        main()
