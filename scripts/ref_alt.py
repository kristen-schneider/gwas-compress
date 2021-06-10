# https://wiki.python.org/moin/BitwiseOperators
# https://wiki.python.org/moin/BitArrays
import math
def main():
    # assumption1('/Users/kristen/Desktop/compression_sandbox/toy_data_in/ref-alt.tsv')
    # data = ['T', 'G', 'G', 'C', 'T', 'T', 'T', 'C', 'G', 'A',
    #          'CT',
    #          'A', 'G', 'T', 'T', 'T', 'T', 'G', 'G', 'G', 'C', 'G', 'T', 'C', 'A', 'A',
    #          'T', 'T', 'C', 'A', 'G', 'A', 'C', 'A', 'G', 'G',
    #          'A',
    #          'AAAAAAAAAAAATATATATATATATATATATATATAT',
    #          'G', 'G', 'G', 'T', 'C', 'C', 'A', 'G', 'A', 'C', 'T', 'C', 'T', 'A', 'C',
    #          'C', 'G', 'T', 'T', 'C', 'A', 'T', 'C', 'C', 'C',
    #          'TA',
    #          'C', 'C', 'C', 'A', 'C', 'C', 'C', 'C', 'C', 'G',
    #          'ACAGGAGGGCGGG']
    data = 'AAA'
    x = col_input(data)
    print(x)

def col_input(column):
    """
    SNV
    1 5     26
    0 00000 00000000000000000000000000
    --snvs
    --length of snv
    --snv bases

    INDEL
    ** first int **
    1 11          20
    1 00000000000 00000000000000000000
    --indels
    --length of full indel (need this to see how many ints are used)
    --indels

    ** rest of ints **
    6      26
    000000 000000000000000000000000
    --length of bases
    --bases

    returns list of integers which represents a column of ref or alt bases (snvs and indels)
    """

    all_ints = []   # to return at end

    SNVs = []   # start collecting SNVs
    for row in column:
        # only SNV
        if len(row) == 1:
            SNVs.append(row)

            # if we achieve 13 SNVs in a row, encode them and move on
            if len(SNVs) == 13:
                # flag to specify SNVs
                SNV_flag = shift_bit(0, 31)
                # SNV length here is 13
                SNV_length = shift_bit(len(SNVs), 26)
                # encode all 13 SNVS
                SNV_bitstring = encode_SNVs(SNVs)
                # final int
                full_SNV_bitstring = SNV_flag | SNV_length | SNV_bitstring
                all_ints.append(full_SNV_bitstring)
                SNVs = []

        # encountered an INDEL
        else:
            # handle any SNVs we have collected
            all_ints.append(encode_SNVs(SNVs))
            SNVs = []

            # handle INDEL we encountered
            INDEL = row
            INDEL_bitstring_info = encode_INDEL(INDEL)

            # # first bitstring will need to include data about how long the INDEL is and such (for decoding)
            # head_bitstring = INDEL_bitstring_info[0]
            # tail_bitstrings = INDEL_bitstring_info[1:]
            # all_ints.append(head_bitstring)
            # for t in tail_bitstrings: all_ints.append(t)
    # handle any SNVs left
    if len(SNVs) > 0:
        all_ints.append(encode_SNVs(SNVs))
        SNVs = []
    else:
        print('invalid length of SNVs')

    return all_ints


def shift_bit(bitstring, shift):
    """
    shifting for little endian format
    """
    return bitstring << shift


def encode_SNVs(SNVs):
    """
    given a list of SNVs, convert to int
    """
    SNV_bitstring = 0

    # flag to specify SNVs
    SNV_flag = shift_bit(0, 31)
    # SNV length here is 13
    SNV_length = shift_bit(len(SNVs), 26)

    SNVs = []
    for v in range(len(SNVs)):
        # get proper bit representation for the variant
        snv = shift_bit(get_variant_number(SNVs[v]), 2*v) | SNV_bitstring
        # if we are on first snv, set bitstring
        if v == 0:
            SNV_bitstring = snv
        else:
            SNV_bitstring = SNV_bitstring | snv

    return SNV_flag | SNV_length | SNV_bitstring

# def encode_under_fifteen_SNVs(SNVs):
#     list_ints = []
#     if len(SNVs) <= 10:
#         start_bitstring = shift_bit(2, 30)
#         len_SNVs = shift_bit(len(SNVs), 20)
#         SNV_bitstring = encode_SNVs(SNVs)
#         full_bitstring = start_bitstring | len_SNVs | SNV_bitstring
#         list_ints.append(full_bitstring)
#     elif len(SNVs) > 10 and len(SNVs) <= 15:
#         # 1-10
#         first_ten = SNVs[0:10]
#         start_ten = shift_bit(2, 30)
#         len_ten = shift_bit(len(first_ten), 20)
#         ten_bitstring = encode_SNVs(first_ten)
#         full_ten = start_ten | len_ten | ten_bitstring
#         list_ints.append(full_ten)
#         # 10-end
#         last_snv = SNVs[10:]
#         start_last = shift_bit(2, 30)
#         len_last = shift_bit(len(last_snv), 20)
#         last_bitstring = encode_SNVs(last_snv)
#         full_last = start_last | len_last | last_bitstring
#         list_ints.append(full_last)
#     return list_ints

def encode_INDEL(INDEL):
    """
    ** first int **
    1 11          20
    1 00000000000 00000000000000000000
    --indels
    --length of full indel (need this to see how many ints are used)
    --indels

    ** rest of ints **
    6      26
    000000 000000000000000000000000
    --length of bases
    --bases
    """
    # list of integers which encode full indel
    indel_ints = []
    # first ten
    start_indel = 0
    end_indel = 10

    len_full_INDEL = shift_bit(len(INDEL), 20)

    num_ints = math.ceil(int(len(INDEL) - 10) / 13) + 1
    for i in range(num_ints):
        # first 10 bases are encoded differently than rest
        if i == 1:
            first_ten_bases = INDEL[start_indel:end_indel]
            INDEL_flag = shift_bit(1, 31)
            first_ten_encoding = encode_SNVs(first_ten_bases)
            indel_ints.append(INDEL_flag | len_full_INDEL | first_ten_encoding)

        # all other bases are encoded with length in 6 bits and then room for 13 bases (26 bits)
        else:
            # next 13 bases
            curr_segment = INDEL[start_indel:end_indel]
            curr_segment_encode = encode_SNVs(curr_segment)
            indel_ints.append(curr_segment_encode)

        start_indel = end_indel
        end_indel += 13
    return indel_ints


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
