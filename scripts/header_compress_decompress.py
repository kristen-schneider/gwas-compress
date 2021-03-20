import type_handling
import serialize
import compress
import decompress
import deserialize


DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3}
BYTE_SIZES = {1: 5, 2: 8, 3: 5}

def get_header_types(full_header, DATA_TYPE_CODE_BOOK):
    header_types = []
    for h in full_header:
        if type(h) == list : h_type = type(h[0])
        else: h_type = type(h)
        header_types.append(DATA_TYPE_CODE_BOOK[h_type])
    return header_types

def compress_header(full_header, header_types):
    '''
    '''
    num_columns = full_header[5]

    len_compressed_h = []
    c_full_header = b''

    for h in range(len(full_header)):
        current_h = full_header[h] # one element of header
        s_current_h = b''

        # serialize a list and a single value differently
        if type(current_h) == list:
            s_current_h = serialize.serialize_list(current_h, header_types[h], BYTE_SIZES[header_types[h]])
        else:
            s_current_h = serialize.serialize_data(current_h, header_types[h], BYTE_SIZES[header_types[h]])

        c_current_h = compress.compress_data(s_current_h, 0)
        len_compressed_h.append(len(c_current_h))

        c_full_header += c_current_h
    return [c_full_header, len_compressed_h, num_columns]

def decompress_header(c_full_header, header_types):
    full_dc_header = []

    c_header = c_full_header[0]
    len_c_headers = c_full_header[1]
    num_columns = c_full_header[2]

    header_sizes = [1, 1, 1, num_columns, num_columns, 1]

    start = 0
    for l in range(len(len_c_headers)):
        curr_len_c_header = len_c_headers[l]
        curr_num_cols_c_header = header_sizes[l]
        curr_data_type_c_header = header_types[l]
        curr_num_bytes_c_header = BYTE_SIZES[curr_data_type_c_header]
        # decompress
        ds_header = decompress.decompress_data(c_header[start:start+curr_len_c_header])
        start += curr_len_c_header

        # deserialize
        #deserialize_data(dc_bitstring, block_size, data_type, num_bytes)
        dc_header = deserialize.deserialize_data(ds_header, curr_num_cols_c_header, curr_data_type_c_header, curr_num_bytes_c_header)
        full_dc_header.append(dc_header)

    return full_dc_header


header = [1, 1, '\t', ['chr', 'position', 'other'], [1,1,3], 3]
header_types = get_header_types(header, DATA_TYPE_CODE_BOOK)
c_full_header = compress_header(header, header_types)
# for h in c_full_header:
#     print(h)
dc_full_header = decompress_header(c_full_header, header_types)
print(dc_full_header)