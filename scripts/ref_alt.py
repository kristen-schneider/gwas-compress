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
                list_ints.append(start_bitstring | SNV_bitstring)

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
            INDEL_bitstring = encode_INDEL(INDEL)
            full_bitstring = start_bitstring | len_INDEL | INDEL_bitstring
            list_ints.append(full_bitstring)

    return list_ints



def long_col_input(column):
    """
    taken a full column of ref/alt bases as a list and return a list of integers
    """
    ref_alt_ints = []

    num_fifteen_nucleotides_blocks = int(math.ceil(len(column)/15))
    print(num_fifteen_nucleotides_blocks)
    start_fifteen = 0
    stop_fifteen = 15
    for n in range(num_fifteen_nucleotides_blocks):
        fifteen_nucleotides = column[start_fifteen:stop_fifteen]
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
            bitstring = shift_bit(first_bit, 1) | second_bit
            num_fifteen_nucleotides_blocks += 1

            # only SNVs < 15
            if second_bit == 0:
                # get how many SNVs there are
                third_bit = get_num_SNVs(SNVs_under_fifteen)
                bitstring = shift_bit(bitstring, 10) | third_bit
                SNVs_bitstring = encode_SNVs(SNVs_under_fifteen)
                bitstring = shift_bit(bitstring, 20) | SNVs_bitstring

            # INDEL
            elif second_bit == 1:
                bitstring = bitstring
            else:
                print('bad second bit')
                return -1
        ref_alt_ints.append(bitstring)
        start_fifteen = stop_fifteen
        stop_fifteen += 15
    return ref_alt_ints


def get_first_bit(fifteen_nucleotides):
    """
    return 1 if there is an indel, and return the leading SNVs
    """
    for i in range(len(fifteen_nucleotides)):
        if len(fifteen_nucleotides[i]) != 1:
            return 1, fifteen_nucleotides[0:i]
    return 0, []


def get_second_bit(SNVs_under_fifteen):
    """
    returns 0 if list is of SNVs and list is size < 15
    returns 1 if list is an INDEL, and returns INDEL
    """
    if len(SNVs_under_fifteen[0]) == 1:
        return 0,
    elif len(SNVs_under_fifteen[0]) > 1:
        return 1, SNVs_under_fifteen[0]
    else:
        print('bad second bit calculation')
        return -1


def get_num_SNVs(SNVs_under_fifteen):
    """
    returns number of SNVs in a list if it is less than 15
    """
    num_SNVs = 0
    for n in range(len(SNVs_under_fifteen)):
        if len(SNVs_under_fifteen[n]) == 1:
            num_SNVs += 1
        else:
            return num_SNVs

    return num_SNVs


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
    indel_bitstring = 0
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