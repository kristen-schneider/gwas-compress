def main():
    # 1.
    get_variant_number('A')

def packed_bit():
    return 0
def single_encoded_bit():
    return

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

def print_bit_array_element_be(bit_array_element, size):
    output = []
    for i in range(1, size + 1):
        output.append(get_bit(bit_array_element, i, size))

    print (' '.join([str(x) for x in output]))

def get_bit(bit_array_element, n, size):
    return (bit_array_element >> (size - n)) & 1


def set_element_bit(bit_array_element, i, size):
    # stores the bit array element as the result of an OR with the old bit array and the new bit array with the new bit added
    bit_array_element = bit_array_element | (1 << (size - i))
    return bit_array_element

def set_bit(B, i, element_size):
    # chooses which element we want (i.e. chooses one of: 00000000 00000000 00000000)
    curr_element = (i - 1) / element_size
    # chooses which bit in our element (i.e. chooses one of: 00000000)
    curr_i = i - curr_element * element_size;

    B[curr_element] = set_element_bit(B[curr_element], curr_i, element_size)

# def misc():
#     for individual in genotype_file:
#         # in order to grab the variants, you must manipulate the row (i.e. separate by some delimited character
#         this_row = individual.split(" ")
#         # print individual
#
#         # go through each variant for each individual
#         v = 1
#         for variant in this_row:
#             # get the index value that corresponds to what kind of zygosity this is (i.e. 0 = homo ref, 1 = het, ...)
#             genotype_array_num = get_genotype_array_num(variant.rstrip())
#             # print variant.rstrip(), ": ", genotype_array_num
#             # print i, current_indiv
#             # extra_step = current_indiv[0]
#             # print extra_step
#             # bit_array_for_selected_zygosity = extra_step[genotype_array_num]
#             # print bit_array_for_selected_zygosity
#             # print bit_array_for_selected_zygosity[0]
#             # print v
#
#             # gt_to_change = current_indiv[genotype_array_num]
#             # print B[i][genotype_array_num]
#             set_bit(B[i][genotype_array_num], v, bit_size)
#             v += 1
#         #	print current_indiv, "\n\n"
#         #	B[i] = current_individual
#         # print "\n"
#         i += 1


if __name__ == '__main__':
        main()