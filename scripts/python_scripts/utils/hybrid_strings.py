# https://wiki.python.org/moin/BitwiseOperators
# https://wiki.python.org/moin/BitArrays
import math
def main():
    #assumption1('/Users/kristen/Desktop/compression_sandbox/toy_data_in/ref-alt.tsv')
    assumption1('/home/krsc0813/projects/gwas-compress/scripts/ref-alt-cols.txt')
    # data = ['T', 'G', 'G', 'C', 'T', 'T', 'T', 'C', 'G', 'A',
    #          'CT',
    #          'A', 'G', 'T', 'T', 'T', 'T', 'G', 'G', 'G', 'C', 'G', 'T', 'C', 'A', 'A',
    #          'T', 'T', 'C', 'A', 'G', 'A', 'C', 'A', 'G', 'G', 'A',
    #          'AAAAAAAAAAAATATATATATATATATATATATATAT',
    #          'G', 'G', 'G', 'T', 'C', 'C', 'A', 'G', 'A', 'C', 'T', 'C', 'T', 'A', 'C',
    #          'C', 'G', 'T', 'T', 'C', 'A', 'T', 'C', 'C', 'C',
    #          'TA',
    #          'C', 'C', 'C', 'A', 'C', 'C', 'C', 'C', 'C', 'G',
    #          'ACAGGAGGGCGGG']
    # # data = ['A', 'A', 'A', 'AAAAA']
    # x = encode_column(data)
    # print(x)

def encode_column(column):
    """
    SNV
    1      
    0 0000000000000000000000000000000
    --snvs
    --snv base

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

    for row in column:
        # only SNV
        if len(row) == 1:
            SNV_bitstring = encode_SNV(row, 1)
            all_ints.append(SNV_bitstring)

        # encountered an INDEL
        else:
            INDEL = row
            INDEL_bitstring_list = encode_INDEL(INDEL)
            for i in INDEL_bitstring_list:
                all_ints.append(i)

    return all_ints


def shift_bit(bitstring, shift):
    """
    shifting for little endian format
    """
    return bitstring << shift


def encode_SNV(SNV, length):
    """
    given a list of SNVs, convert to int
    """
    SNV_bitstring = 0

    # flag to specify SNVs
    SNV_flag = shift_bit(0, 31)

    # encode a single SNV
    snv = shift_bit(get_variant_number(SNV), 0) | SNV_bitstring
    SNV_bitstring = SNV_bitstring | snv

    return SNV_flag | SNV_bitstring

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

    full_indel_length = len(INDEL)

    num_ints = math.ceil(int(len(INDEL) - 10) / 13) + 1
    #print(INDEL, num_ints)

    # first ten bases
    first_ten = encode_first_ten_indel(full_indel_length, INDEL[0:10])
    indel_ints.append(first_ten)

    # remaining bases
    start = 10
    end = 23
    if full_indel_length > 10:
        num_ints = math.ceil((full_indel_length-10)/13)
        for i in range(num_ints):
            curr_thirteen = INDEL[start:end]
            curr_thirteen_encoded = encode_remaining_indel(len(curr_thirteen), curr_thirteen)
            indel_ints.append(curr_thirteen_encoded)
            start = end
            end += 13

    return indel_ints

def encode_first_ten_indel(full_indel_length, first_ten_bases):
    SNV_bitstring = 0
    INDEL_flag = shift_bit(1, 31)
    SNV_length = shift_bit(full_indel_length, 20)

    for v in range(len(first_ten_bases)):
        # get proper bit representation for the variant
        snv = shift_bit(get_variant_number(first_ten_bases[v]), 2 * v) | SNV_bitstring
        SNV_bitstring = SNV_bitstring | snv

    return INDEL_flag | SNV_length | SNV_bitstring

def encode_remaining_indel(length_segment, segment):
    SNV_bitstring = 0
    SNV_length = shift_bit(length_segment, 26)

    for b in range(len(segment)):
        # get proper bit representation for the variant
        snv = shift_bit(get_variant_number(segment[b]), 2 * b) | SNV_bitstring
        SNV_bitstring = SNV_bitstring | snv

    return SNV_length | SNV_bitstring


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
        print('not a proper base', base)
        return -1

def decode_int_to_string(int_list):
    """
    SNV
    1 5     26
    0 00000 00000000000000000000000000
    --snvs
    --length of snv (can be up to 13)
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

    returns list of bases
    """
    snv_bases = []
    curr_indel_bases = None
    SNV_INDEL = False
    for i in range(len(int_list)):
        curr_integer = int_list[i]

        if curr_integer == 1 and SNV_INDEL:
            snv_bases.append('True')
        elif curr_integer == 0 and SNV_INDEL:
            snv_bases.append('False')
        else:
            SNV_INDEL = True
            type_flag = shift_bit_decoding(curr_integer, 31)

            if type_flag == 0:
                curr_snv_bases = decode_snv(curr_integer)
                if curr_snv_bases != None: snv_bases.append(curr_snv_bases)

            elif type_flag == 1:
                # 2047 = 011111111111
                num_int_for_indel = shift_bit_decoding(curr_integer, 20) & 2047
                indel_ints = int_list[i:i+num_int_for_indel]
                curr_indel_bases = decode_indel(indel_ints)
                if curr_indel_bases != None: snv_bases.append(curr_indel_bases)

            else:
                print('not an indel or snv...')
            SNV_INDEL = False

    return snv_bases

def decode_snv(curr_integer):
    snv_base = get_base_from_binary(curr_integer)
    return snv_base

def decode_indel(indel_ints):
    """

    """
    INDEL = ''
    for i in range(len(indel_ints)):
        # first integer is different than rest
        if i == 0:
            first_int = indel_ints[i]
            first_int_length = first_int & 4194304
            # 1048575 = 00000000000011111111111111111111
            encoded_indel_first_int = first_int & 1048575

            for base_bits in range(first_int_length):
                curr_base_binary = encoded_indel_first_int & 3
                encoded_indel_first_int = shift_bit_decoding(encoded_indel_first_int, 2)
                indel_base = get_base_from_binary(curr_base_binary)
                INDEL+=indel_base

        # all other ints
        else:
            curr_int = indel_ints[i]
            # 63 = 111111
            num_bases_curr_int = shift_bit_decoding(curr_int, 26) & 63

            # 67108863 = 00000011111111111111111111111111
            encoded_indel_first_int = curr_int & 67108863

            for base_bits in range(num_bases_curr_int):
                curr_base_binary = encoded_indel_first_int & 3
                encoded_indel_first_int = shift_bit_decoding(encoded_indel_first_int, 2)
                indel_base = get_base_from_binary(curr_base_binary)
                INDEL += indel_base

    if len(INDEL) > 0: return INDEL


def shift_bit_decoding(bitstring, shift):
    """
    shifts bit to right
    """
    return bitstring >> shift

def get_base_from_binary(binary):
    if (binary == 00):
        return 'A'
    elif (binary == 1):
        return 'C'
    elif (binary == 2):
        return 'G'
    elif (binary == 3):
        return 'T'
    else:
        print('not a proper binary value', binary)
        return -1



if __name__ == '__main__':
        main()
