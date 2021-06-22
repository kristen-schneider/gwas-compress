import math

def encode_column(column):
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
    for bases in column:
        # handle TRUE/FALSE/NA strings different than REF/ALT strings
        if bases.lower() == 'true' or bases.lower() == 'false' or bases.lower() == 'na':
            all_ints = true_false_na(column)

        # handle SNVs/INDELs
        else:
            # only SNV
            if len(bases) == 1:
                SNVs.append(bases)

                # if we achieve 13 SNVs in a row, encode them and move on
                if len(SNVs) == 13:
                    SNV_bitstring = encode_SNVs(SNVs, len(SNVs), 0)
                    all_ints.append(SNV_bitstring)
                    SNVs = []

            # encountered an INDEL
            else:
                # handle any SNVs we have collected
                if len(SNVs) > 0:
                    all_ints.append(encode_SNVs(SNVs, len(SNVs),0))
                    SNVs = []

                # handle INDEL we encountered
                INDEL = bases
                INDEL_bitstring_list = encode_INDEL(INDEL)
                for i in INDEL_bitstring_list:
                    all_ints.append(i)

    # handle any SNVs left
    if len(SNVs) > 0:
        all_ints.append(encode_SNVs(SNVs, len(SNVs),0))
        SNVs = []

    return all_ints

def true_false_na(column):
    """
    encodes true as 1, false as 0, NA as -1
    """
    int_column = []
    for d in column:
        if d.lower() == 'true':
            int_column.append(1)
        elif d.lower() == 'false':
            int_column.append(0)
        elif d.lower() == 'na':
            int_column.append(-1)
        else:
            print('invalid t/f/na data')
            return -1
    return int_column


def shift_bit_encoding(bitstring, shift):
    """
    shifts bit to left
    shifting for little endian format
    """
    return bitstring << shift


def encode_SNVs(SNVs, length, INDEL_ten_flag):
    """
    given a list of SNVs, convert to int
    """
    SNV_bitstring = 0

    # flag to specify SNVs
    SNV_flag = shift_bit_encoding(0, 31)

    if INDEL_ten_flag:
        SNV_length = shift_bit_encoding(length, 20)
    else:
        SNV_length = shift_bit_encoding(length, 26)

    for v in range(len(SNVs)):
        # get proper bit representation for the variant
        snv = shift_bit_encoding(get_variant_number(SNVs[v]), 2 * v) | SNV_bitstring
        SNV_bitstring = SNV_bitstring | snv

    return SNV_flag | SNV_length | SNV_bitstring


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

    len_full_INDEL = len(INDEL)

    num_ints = math.ceil(int(len(INDEL) - 10) / 13) + 1
    #print(INDEL, num_ints)
    for i in range(num_ints):
        # first 10 bases are encoded differently than rest
        if i == 0:
            first_ten_bases = INDEL[start_indel:end_indel]
            INDEL_flag = shift_bit_encoding(1, 31)
            first_ten_encoding = encode_SNVs(first_ten_bases, len_full_INDEL, 1)
            indel_ints.append(INDEL_flag | first_ten_encoding)

        # all other bases are encoded with length in 6 bits and then room for 13 bases (26 bits)
        else:
            # next 13 bases
            curr_segment = INDEL[start_indel:end_indel]
            curr_segment_encode = encode_SNVs(curr_segment, len(curr_segment), 0)
            indel_ints.append(curr_segment_encode)

        start_indel = end_indel
        end_indel += 13
    return indel_ints

def get_variant_number(base):
    """
    converts back from
    """
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

    SNV_INDEL = False
    for i in range(len(int_list)):
        curr_integer = int_list[i]
        if curr_integer == 1 and not SNV_INDEL:
            snv_bases.append('True')
        elif curr_integer == 0 and not SNV_INDEL:
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
                if curr_indel_bases != None: snv_bases.append(indel_bases)

            else:
                print('not an indel or snv...')

    return snv_bases

def decode_snv(curr_integer):
    snv_bases = []
    num_snvs = shift_bit_decoding(curr_integer, 26)

    # 67108863 = 00000011111111111111111111111111
    encoded_snv_bases = curr_integer & 67108863

    for base_bits in range(num_snvs):
        curr_snv_binary = encoded_snv_bases & 3
        encoded_snv_bases = shift_bit_decoding(encoded_snv_bases, 2)
        snv_base = get_base_from_binary(curr_snv_binary)
        snv_bases.append(snv_base)
    if len(snv_bases) > 0: return snv_bases

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
