# https://wiki.python.org/moin/BitwiseOperators
# https://wiki.python.org/moin/BitArrays
import array
def main():
    x = assumption1(True, True, 'C'*15)
    print(x)


def assumption1(fifteen_SNVs_bool, SNVs_bool, SNVs):
    # 1. 1 bit: fifteen consecutive snps
    # 2. 1 bit: snv or indel
    # 3.a. 30 bits: snvs (up to 15)
    # 3.b.i 10 bits: length of indel OR SNVs
    # 3.b.ii 20 bits: snvs (up to 10)

    # assumptions for round 1 is that we pack 16 snvs into one int.
    # assume always 00
    bitstring = bits_one_two(fifteen_SNVs_bool, SNVs_bool)
    if fifteen_SNVs_bool:
        # move over 30 bits
        bitstring = bitstring
        SNVs_bitsting = encode_SNVs(SNVs)
        bitstring = bitstring | SNVs_bitsting

    return bitstring

def bits_one_two(fifteen_SNVs_bool, SNVs_bool):
    # if first bit is zero, we know second bit
    if fifteen_SNVs_bool:
        # set first bit
        bitstring = first_bit(fifteen_SNVs_bool)

        # shift over 1. second bit is set as zero automatically
        bitstring = shift_bit(bitstring, 1)

    # else we do not know second bit
    else:
        # set first bit
        bitstring = first_bit(fifteen_SNVs_bool)

        # shift over 1.
        bitstring = shift_bit(bitstring, 1)
        # set second bit
        bitstring = bitstring | second_bit(SNVs_bool)

    return bitstring

def first_bit(fifteen_snvs_bool):
    """
    if there are fifteen snvs in a row, we want to return 0.
    the first bit of our bitstring can be 0.
    else we return 1.
    the first bit of our bitstring can be 1.
    """
    if fifteen_snvs_bool:
        return 0
    else:
        return 1

def second_bit(snv_bool):
    """
    if we are looking at more snvs (less than 15), return 0.
    the second bit of our bitstring can be 0.
    else we return 1.
    the second bit of our bitstring can be 1.
    """
    if snv_bool:
        return 0
    else:
        return 1

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
        # # if we are on last snv, no not shift, just return
        # elif v == 14:
        #     snv_bitstring = snv_bitstring | snv
        #     return snv_bitstring
        # if we are in middle, shift bitstring
        else:
            # shift bitstring
            # snv_bitstring = shift_bit(snv_bitstring, 2*v)
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

if __name__ == '__main__':
        main()