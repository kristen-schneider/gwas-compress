# IMPORTS
import sys
from datetime import datetime

# import arguments
import config_arguments
import generate_header_first_half
import generate_funnel_format
import funnel_format_compress
import header_compress

# CONSTANTS
DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes:4}
DATA_TYPE_BYTE_SIZES = {1: 5, 2: 8, 3: 5, 4:None}
COMPRESSION_METHOD_CODE_BOOK = {'gzip':1, 'zlib':2}

print('starting script')
#print(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
# PARAMETERS
args = config_arguments.get_args_from_config()

IN_FILE = args['in_file']
OUT_DIR = args['out_file']
BLOCK_SIZE = args['block_size']
#COMPRESSION_METHOD = COMPRESSION_METHOD_CODE_BOOK[args.c]
COMPRESSION_METHOD = ['gzip', 'gzip', 'gzip', 'gzip', 'gzip', 'gzip', 'gzip', 'gzip', 'gzip', 'gzip']
COMPRESSED_FILE = OUT_DIR + 'kristen-' + str(COMPRESSION_METHOD[0]) + '-' + str(BLOCK_SIZE) + '.tsv'
DATA_FILE = OUT_DIR + 'plot-' + str(COMPRESSION_METHOD[0]) + '-' + str(BLOCK_SIZE) + '.csv'
MTIME = args.t
if MTIME == None: MTIME = 0

# IN FILE
#'/Users/kristen/Desktop/compression_sandbox/toy_data/
# FIJI: '/scratch/Users/krsc0813/gwas-compress/data/test-gwas-data/test.tsv'

# OUT FILE
# '/Users/kristen/Desktop/compression_sandbox/toy_data/'
# FIJI: '/scratch/Users/krsc0813/gwas-compress/data/compressed/'

def main():
    # 1. GET FIRST HALF OF HEADER
    ### Magic number, version number, delimiter, column labels, column types, number columns, gzip header
    ### [1,1,'\t',['chr', 'pos', 'ref', 'alt', 'af_cases_EUR', 'af_controls_EUR', 'beta_EUR', 'se_EUR', 'pval_EUR', 'low_confidence_EUR'],[1, 1, 3, 3, 2, 2, 2, 2, 2, 3],10,b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff']
    print('generating start of header...')
    header_first_half_START = datetime.now()
    ### work ###
    header_first_half = generate_header_first_half.get_header_data(IN_FILE, DATA_TYPE_CODE_BOOK, COMPRESSION_METHOD_CODE_BOOK['gzip'])
    ############
    header_first_half_END = datetime.now()
    header_first_half_TIME = header_first_half_END - header_first_half_START
    print(str(header_first_half_TIME) + ' for header start to compute...\n')

    magic_number = header_first_half[0]
    version = header_first_half[1]
    delimiter = header_first_half[2]
    column_labels = header_first_half[3]
    column_types = header_first_half[4]
    number_columns = header_first_half[5]
    gzip_header = header_first_half[6]

    # 2. GET FUNNEL FORMAT
    ### list of blocks [[block1][block2]...[blockn]]
    ### --> a block is a list of columns: block1 = [[col1], [co2]...[colm]]
    ### -----> a column is a list of string values: col1 = ['1','1','1','1','1']
    print('generating funnel format...')
    funnel_format_START = datetime.now()
    ### work ###
    funnel_format_data = generate_funnel_format.make_all_blocks(IN_FILE, BLOCK_SIZE, number_columns, delimiter)
    ############
    funnel_format_END = datetime.now()
    funnel_format_TIME = funnel_format_END - funnel_format_START
    print(str(funnel_format_TIME) + ' for funnel format to compute...\n')

    # 3. COMPRESS DATA, GET SECOND HALF OF HEADER
    print('compressing data...')
    compress_data_START = datetime.now()
    ### work ###
    serialize_compress_data = funnel_format_compress.compress_all_blocks(DATA_TYPE_CODE_BOOK, DATA_TYPE_BYTE_SIZES,
                                                                         COMPRESSION_METHOD, COMPRESSION_METHOD_CODE_BOOK, MTIME,
                                                                         header_first_half, funnel_format_data)
    header_second_half = serialize_compress_data[0]
    compressed_data = serialize_compress_data[1]
    column_compression_times = serialize_compress_data[2]
    df = open(DATA_FILE, 'w')
    for cctime in column_compression_times:
        df.write(cctime)
        df.write(',')
        df.write(str(column_compression_times[cctime]))
        df.write(',\n')
    df.close()

    ############
    compress_data_END = datetime.now()
    compress_data_TIME = compress_data_END - compress_data_START
    print(str(compress_data_TIME) + ' for full compression to complete...\n')

    # 4. COMPRESS HEADER
    print('compressing header...')
    compress_header_START = datetime.now()
    ### work ###
    full_header = header_first_half+header_second_half
    print(full_header)
    # header types, number of elements in each header
    serialized_header_tools = header_compress.full_header_tools(DATA_TYPE_CODE_BOOK, DATA_TYPE_BYTE_SIZES, full_header)
    serialized_header_types = serialized_header_tools[0]
    serialized_header_num_elements = serialized_header_tools[1]
    serialized_header_ends = serialized_header_tools[2]
    serialized_header_data = serialized_header_tools[3]

    size_types = len(serialized_header_types)
    bytes_size_types = size_types.to_bytes(2, byteorder='big', signed=False)
    size_elements = len(serialized_header_num_elements)
    bytes_size_num_elements = size_elements.to_bytes(2, byteorder='big', signed=False)
    size_ends = len(serialized_header_ends)
    bytes_size_ends = size_ends.to_bytes(2, byteorder='big', signed=False)
    size_data = len(serialized_header_data)
    bytes_size_data = size_data.to_bytes(2, byteorder='big', signed=False)
    ############
    compress_header_END = datetime.now()
    compress_header_TIME = compress_header_END - compress_header_START
    print(str(compress_header_TIME) + ' for header to compress...\n')


    # 5. WRITE COMPRESSED HEADER
    print('writing header...')
    write_header_START = datetime.now()
    ### work ###
    compressed_with_header = open(COMPRESSED_FILE, 'wb')
    # write how many bytes are needed to store types, ends, and data (CONSTANT FIRST 4 BYTES)
    compressed_with_header.write(bytes_size_types)
    compressed_with_header.write(bytes_size_num_elements)
    compressed_with_header.write(bytes_size_ends)
    compressed_with_header.write(bytes_size_data)

    # write header types and header ends (serialized)
    compressed_with_header.write(serialized_header_types)
    compressed_with_header.write(serialized_header_num_elements)
    compressed_with_header.write(serialized_header_ends)

    # write header (serialized)
    compressed_with_header.write(serialized_header_data)
    ############
    write_header_END = datetime.now()
    write_header_TIME = write_header_END - write_header_START
    print(str(write_header_TIME) + ' for header to write...\n')

    # 6. WRITE COMPRESSED DATA
    print('writing data...')
    write_data_START = datetime.now()
    ### work ###
    compressed_with_header.write(compressed_data)
    ############
    write_data_END = datetime.now()
    write_data_TIME = write_data_END - write_data_START
    print(str(write_data_TIME) + ' for data to write...\n')

if __name__ == '__main__':
    main()
