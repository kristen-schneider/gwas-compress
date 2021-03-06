# IMPORTS
import deserialize_header
from utils import type_handling

#
# DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes:4}
# DATA_TYPE_BYTE_SIZES = {1: 5, 2: 8, 3: 5, 4:None}

def get_full_header(data_type_byte_sizes, OUT_FILE):
    """
    opens out file and returns full header

    INPUT

    OUTPUT

    """
    compressed_file = open(OUT_FILE, 'rb')
    #content = compressed_file.read()
    STOP_HEADER = False

    HEADER_TOOLS = []
    HEADER_TYPES = None
    HEADER_NUM_ELEMENTS = None
    HEADER_ENDS = None
    HEADER_DATA = None

    total_bytes_read = 0
    while not STOP_HEADER:
        # get 3 sizes first (2 bytes each)
        if len(HEADER_TOOLS) < 3:
            num_bytes_to_read = 2

            header_types_size = compressed_file.read(num_bytes_to_read)
            ds_header_types_size = deserialize_header.deserialize_int(header_types_size, 1, 2, 0)[0]
            HEADER_TOOLS.append(ds_header_types_size)
            total_bytes_read += num_bytes_to_read

            header_elements_size = compressed_file.read(num_bytes_to_read)
            ds_header_elements_size = deserialize_header.deserialize_int(header_elements_size, 1, 2, 0)[0]
            HEADER_TOOLS.append(ds_header_elements_size)
            total_bytes_read += num_bytes_to_read

            header_ends_size = compressed_file.read(num_bytes_to_read)
            ds_header_ends_size = deserialize_header.deserialize_int(header_ends_size, 1, 2, 0)[0]
            HEADER_TOOLS.append(ds_header_ends_size)
            total_bytes_read += num_bytes_to_read
        
        elif len(HEADER_TOOLS) == 3:
            num_bytes_to_read = 4
            header_data_size = compressed_file.read(num_bytes_to_read)
            ds_header_data_size = deserialize_header.deserialize_int(header_data_size, 1, 4, 0)[0]
            HEADER_TOOLS.append(ds_header_data_size)
            total_bytes_read += num_bytes_to_read

        elif HEADER_TYPES == None:
            num_bytes_to_read = HEADER_TOOLS[0]

            header_types = compressed_file.read(num_bytes_to_read)
            ds_header_types = deserialize_header.deserialize_int(header_types,
                                                                 int(num_bytes_to_read/data_type_byte_sizes[1]),
                                                                 data_type_byte_sizes[1],
                                                                 0)
            HEADER_TYPES = ds_header_types
            total_bytes_read += num_bytes_to_read

        elif HEADER_NUM_ELEMENTS == None:
            num_bytes_to_read = HEADER_TOOLS[1]

            header_elements = compressed_file.read(num_bytes_to_read)
            ds_header_elements = deserialize_header.deserialize_int(header_elements,
                                                                    int(num_bytes_to_read/data_type_byte_sizes[1]),
                                                                    data_type_byte_sizes[1],
                                                                    0)
            HEADER_NUM_ELEMENTS = ds_header_elements
            total_bytes_read += num_bytes_to_read

        elif HEADER_ENDS == None:
            num_bytes_to_read = HEADER_TOOLS[2]

            header_ends = compressed_file.read(num_bytes_to_read)
            ds_header_ends = deserialize_header.deserialize_int(header_ends,
                                                                int(num_bytes_to_read/data_type_byte_sizes[1]),
                                                                data_type_byte_sizes[1],
                                                                0)
            HEADER_ENDS = ds_header_ends
            total_bytes_read += num_bytes_to_read


        elif HEADER_DATA == None:
            num_bytes_to_read = HEADER_TOOLS[3]
            header_data = compressed_file.read(num_bytes_to_read)
            ds_header_data = decompress_header(data_type_byte_sizes,
                                                HEADER_TYPES,
                                                HEADER_NUM_ELEMENTS,
                                                HEADER_ENDS,
                                                header_data)
            HEADER_DATA = ds_header_data
            total_bytes_read += num_bytes_to_read
            #STOP_HEADER = True

        else: STOP_HEADER = True
        # if header_ends_size == b'': STOP_HEADER = True
    compressed_file.close()
    return total_bytes_read, HEADER_DATA


def decompress_header(data_type_byte_sizes, header_types, header_num_elements, header_ends, header_data):
    full_ds_header = []

    #dc_full_header = decompress.decompress_data(c_full_header)

    # deserialize header by piece
    curr_h_start = 0
    for h in range(len(header_types)):
        curr_h_type = header_types[h]
        curr_h_num_elements = header_num_elements[h]
        curr_h_end = header_ends[h]
        curr_h = header_data[curr_h_start:curr_h_end]

        ds_curr_h = deserialize_header.deserialize_list(curr_h, curr_h_num_elements, curr_h_type, data_type_byte_sizes[curr_h_type], h)
        #if len(ds_curr_h) == 1: full_ds_header.append(ds_curr_h[0])
        #else: full_ds_header.append(ds_curr_h)
        full_ds_header.append(ds_curr_h)
        curr_h_start = curr_h_end


    return full_ds_header
