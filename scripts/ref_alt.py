# https://wiki.python.org/moin/BitwiseOperators
# https://wiki.python.org/moin/BitArrays
import array
def main():
    x = assumption1(True, True, 'C'*15)
    print(x)

def col_input(column):
    """
    taken a column of indels and snps in a list and do the work...
    """
    for n in range(len(column)):
        fifteen_nucleotides = column[n:15]
        first_bit_info = get_first_bit(fifteen_nucleotides)
        first_bit = first_bit_info[0]
        SNVs_under_fifteen = first_bit_info[1]

        # fifteen SNVs in a row
        if first_bit == 0:
            # leading zeros for 15 snvs won't matter
            bitstring = encode_SNVs(fifteen_nucleotides)
        # either < 15 SNVs or INDEL
        else:
            second_bit = get_second_bit(SNVs_under_fifteen)
            # SNVs < 15
            if second_bit == 0:
                # get how many SNVs there are
                third_bit = get_num_SNVs(SNVs_under_fifteen)

            # encode INDEL


def get_first_bit(fifteen_nucleotides):
    """
    return 1 if there is an indel, and return the leading SNVs
    """
    if len(fifteen_nucleotides) != 15:
        print('incorrect input for 15 block')
        return -1
    for i in range(len(fifteen_nucleotides)):
        if len(fifteen_nucleotides[i] != 1):
            return 1, fifteen_nucleotides[0:i]
    return 0


def get_second_bit(SNVs_under_fifteen):
    """
    returns 0 if list is of SNVs and list is size < 15
    returns 1 if list is an INDEL, and returns INDEL
    """
    if len(SNVs_under_fifteen[0]) == 1:
        return 0
    elif len(SNVs_under_fifteen[0]) > 1:
        return 1, SNVs_under_fifteen[0]
    else:
        print('bad second bit calculation')
        return -1


def get_num_SNVs(SNVs_under_fifteen):
    num_SNVs = 0
    for n in range(len(SNVs_under_fifteen)):


    return len(SNVs_under_fifteen)

def shift_bit(bitstring, shift):
    """
    shifting for little endian format
    """
    return bitstring << shift


def encode_SNVs(SNVs):
    snv_bitstring = 0
    for v in range(len(SNVs)):
        # get proper bit representation for the variant
        snv = shift_bit(get_variant_number(SNVs[v]), 2*v)
        # if we are on first snv, set bitstring
        if v == 0:
            snv_bitstring = snv
        else:
            snv_bitstring = snv_bitstring | snv
    return snv_bitstring


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