import type_handling
import serialize
import compress
import decompress
import deserialize


#DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3}
BYTE_SIZES = {1: 5, 2: 8, 3: 5}

def get_header_types(full_header, DATA_TYPE_CODE_BOOK):
    header_types = []
    for h in full_header:
        h_type = type(h[0])
        header_types.append(DATA_TYPE_CODE_BOOK[h_type])
    return header_types

def compress_header(full_header, header_types):
    '''
    '''
    num_columns = full_header[4][0]
    #header_types = [1, 3, 3, 1, 1, 1, 1]
    #header_sizes = [2, 1, num_columms, num_columns, 1, num_columns, 2]
    len_compressed_headers = []
    c_header = b''
    print(full_header)

    for h in range(len(full_header)):
        print(full_header[h])
        #serialize_data([1,1,1,1,1], type_to_bytes_code_book[1], 1)
        s_header = serialize.serialize_data(full_header[h], BYTE_SIZES[header_types[h]], header_types[h])
        print(s_header)
        curr_c_header = compress.compress_data(s_header, 0)
        print(curr_c_header)
        c_header += curr_c_header
        len_compressed_headers.append(len(curr_c_header))
    return [c_header, len_compressed_headers, num_columns]

def decompress_header(c_header_info, header_types):
    full_dc_header = []

    c_header = c_header_info[0]
    len_c_headers = c_header_info[1]
    num_columns = c_header_info[2]
    header_sizes = [2, 1, num_columns, num_columns, 1, num_columns, 2]
    #header_types = [1, 3, 3, 1, 1, 1, 1]

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

