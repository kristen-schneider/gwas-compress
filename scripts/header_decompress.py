# IMPORTS
import decompress
import deserialize


DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes:4}
DATA_TYPE_BYTE_SIZES = {1: 5, 2: 8, 3: 5, 4:None}

def decompress_header(header_types, header_num_elements, header_ends, header_data):
    full_ds_header = []

    #dc_full_header = decompress.decompress_data(c_full_header)

    # deserialize header by piece
    curr_h_start = 0
    for h in range(len(header_types)):
        curr_h_type = header_types[h]
        curr_h_num_elements = header_num_elements[h]
        curr_h_end = header_ends[h]
        curr_h = header_data[curr_h_start:curr_h_end]

        ds_curr_h = deserialize.deserialize_data(curr_h, curr_h_num_elements, curr_h_type, DATA_TYPE_BYTE_SIZES[curr_h_type], h)
        if len(ds_curr_h) == 1: full_ds_header.append(ds_curr_h[0])
        else: full_ds_header.append(ds_curr_h)
        curr_h_start = curr_h_end


    return full_ds_header


# header = [1, 1, '\t', ['chr', 'position', 'other'], [1.00,12.12,3e+05], 3]
# full_header_tools(header)
# for h in c_full_header:
#     print(h)
# dc_full_header = decompress_header(c_full_header)
# print(dc_full_header)