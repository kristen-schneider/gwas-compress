# https://wiki.python.org/moin/BitwiseOperators
# https://wiki.python.org/moin/BitArrays
import math
def main():
    # data = ['C']*15
    data = ['C', 'T', 'T', 'GATACA']
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

        # encountered an INDEL
        else:
            # handle any SNVs we have collected
            if len(SNVs) > 0:
                start_bitstring = shift_bit(1, 30)
                len_SNVs = shift_bit(len(SNVs), 20)
                SNV_bitstring = encode_SNVs(SNVs)
                full_bitstring = start_bitstring | len_SNVs | SNV_bitstring
                list_ints.append(full_bitstring)

            # handle INDEL we encountered
            INDEL = row
            start_bitstring = shift_bit(3, 30)
            len_INDEL = shift_bit(len(INDEL), 20)
            INDEL_bitstring_info = encode_INDEL(INDEL)
            head_bitstring = start_bitstring | len_INDEL | INDEL_bitstring_info[0]
            tail_bitstrings = INDEL_bitstring_info[1:]
            # INDEL_bitstring = [head_bitstring]
            # for t in tail_bitstrings: INDEL_bitstring.append(t)
            list_ints.append(head_bitstring)
            for t in tail_bitstrings: list_ints.append(t)

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
    indel_bitstring = [0,1,1]
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

def assumption1(SNVs):
    # 1. 1 bit: fifteen consecutive snps
    # 2. 1 bit: snv or indel
    # 3.a. 30 bits: snvs (up to 15)
    # 3.b.i 10 bits: length of indel OR SNVs
    # 3.b.ii 20 bits: snvs (up to 10)

    # assumptions for round 1 is that we pack 16 snvs into one int.
    # assume always 00
    bitstring = 00
    SNVs_bitsting = encode_SNVs(SNVs)
    bitstring = bitstring | SNVs_bitsting

    return bitstring

if __name__ == '__main__':
        main()