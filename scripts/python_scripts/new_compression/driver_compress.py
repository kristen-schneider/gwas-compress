#### IMPORTS ####
# python_scripts imports
import cProfile
from datetime import datetime
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# kristen imports
from utils import config_arguments
import generate_header_first_half
import generate_funnel_format
import compress_funnel_format
import header_compress
# from plotting import boxplot

#### CONSTANTS ####
# DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes:4}
# AVAILABLE_COMPRESSION_METHODS = ['gzip', 'zlib', 'bz2', 'fastpfor128', 'fastpfor256']

### System Arguments ### (clean this up)
config_file = sys.argv[1]#'/home/krsc0813/projects/gwas-compress/config_files/config.ini'


def main():
    """
    0. get arguments from user to run compression according to their preferences
    1. gets beginning of header (magic number, version, delimiter, column labels, column types, num columns, gzip header)
    2. generates funnel format (list of blocks)
    3. compress data and get second half of header *depends on input data type and compression data type
    4. compress full header
    5. write compressed header
    6. write compressed data
    """
    # 1. GET ARGUMENTS
    #print('0. getting arguments...')
    get_arguments_start_time = datetime.now()

    # user should edit config.ini to reflect proper parameters
    # args = config_arguments.get_args_from_config('LOCAL', config_file)

    args = config_arguments.get_args_from_config('MENDEL', config_file)#, 'fastpfor')
    config_basename = config_file.split('/')[-1].split('_')[0]
    # included in config file
    IN_FILE = args['in_file']
    #IN_FILE = sys.argv[1]
    OUT_DIR = args['out_dir']
    BLOCK_SIZE = int(args['block_size'])
    #BLOCK_SIZE = int(sys.argv[3])
    CODECS_LIST = list(args['compression_method'].split(','))
    COMPRESSION_DATA_TYPES=list(args['input_data_type'].split(','))
    #COMPRESSION_DATA_TYPES = sys.argv[4].split(',')
    # COMPRESSION_DATA_TYPE_=args['compression_data_type']
    DATA_TYPE_BYTE_SIZES = {1: int(args['int_byte_size']),
                            2: int(args['float_byte_size']),
                            3: int(args['string_byte_size']),
                            4: int(args['string_byte_size']),
                            5: args['bytes_byte_size']}
    
    # output file made from combining user specified params
    basename_in_file = IN_FILE.split('/')[-1].split('.')[0]
    COMPRESSED_FILE = OUT_DIR + 'kristen-' + config_basename + '-' + basename_in_file + '-' + str(BLOCK_SIZE) + '.tsv'
    COMPRESSION_TIMES_FILE = OUT_DIR + 'times-' + str(BLOCK_SIZE) + '.csv'
    #print(datetime.now()-get_arguments_start_time, ' to get arguments.\n')

    # 1. GET FIRST HALF OF HEADER
    ### Magic number, version number, delimiter, column labels, column types, number columns
    #print('1. generating start of header...')
    header_first_half_START = datetime.now()
    ### work ###
    header_first_half = generate_header_first_half.get_header_first_half(IN_FILE)
    ############
    header_first_half_END = datetime.now()
    header_first_half_TIME = header_first_half_END - header_first_half_START
    #print('header: ', header_first_half)
    print('file','header_first_half',header_first_half_TIME)

    magic_number = header_first_half[0]
    version = header_first_half[1]
    delimiter = header_first_half[2]
    column_labels = header_first_half[3]
    decompression_data_types = header_first_half[4]
    number_columns = header_first_half[5]


    # 2. GET FUNNEL FORMAT
    #print('2. generating funnel format...')
    funnel_format_START = datetime.now()
    ### work ###
    funnel_format_data = generate_funnel_format.make_all_blocks(IN_FILE, BLOCK_SIZE,
                                                                number_columns, delimiter)
    ############
    funnel_format_END = datetime.now()
    funnel_format_TIME = funnel_format_END - funnel_format_START
    print('file', 'funnel_format', funnel_format_TIME)

    # 3. COMPRESS DATA, GET SECOND HALF OF HEADER
    #print('3. compressing data...')
    compress_data_START = datetime.now()
    # ### work ###
    header_second_half_info = compress_funnel_format.compress_all_blocks(CODECS_LIST,
                                                                    COMPRESSION_DATA_TYPES,
                                                                    DATA_TYPE_BYTE_SIZES,
                                                                    header_first_half,
                                                                    funnel_format_data,
                                                                    config_file.split('/')[-1].split('_')[0])
    compressed_data = header_second_half_info[0]
    header_second_half = header_second_half_info[1]
    ############
    compress_data_END = datetime.now()
    compress_data_TIME = compress_data_END - compress_data_START
    print('file', 'compress data', compress_data_TIME)


    # 4. COMPRESS HEADER
    compress_header_START = datetime.now()
    ### work ###
    full_header = header_first_half+header_second_half
    #print(full_header)
    # header types, number of elements in each header
    serialized_header_tools = header_compress.full_header_tools(DATA_TYPE_BYTE_SIZES,
                                                                 full_header)
    serialized_header_types = serialized_header_tools[0]
    serialized_header_num_elements = serialized_header_tools[1]
    serialized_header_ends = serialized_header_tools[2]
    serialized_header_data = serialized_header_tools[3]
    
    size_types = len(serialized_header_types)
    try: bytes_size_types = size_types.to_bytes(2, byteorder='big', signed=False)
    except OverflowError: print(size_types)
    size_elements = len(serialized_header_num_elements)
    try: bytes_size_num_elements = size_elements.to_bytes(2, byteorder='big', signed=False)
    except OverflowError: print(size_elements)
    size_ends = len(serialized_header_ends)
    try: bytes_size_ends = size_ends.to_bytes(2, byteorder='big', signed=False)
    except OverflowError: print(bytes_size_ends)
    size_data = len(serialized_header_data)
    try: bytes_size_data = size_data.to_bytes(4, byteorder='big', signed=False)
    except OverflowError: print(size_data)
    ############
    compress_header_END = datetime.now()
    compress_header_TIME = compress_header_END - compress_header_START
    print('file', 'compress header', compress_header_TIME)

    # ######################################################
    # ## OLD WRITE METHOD WHERE EVERYTHING WRITTEN AT END ##
    # ######################################################
    #
    # 5. WRITE COMPRESSED HEADER
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
    print('file', 'write header', write_header_TIME)
    
    # 6. WRITE COMPRESSED DATA
    #print('writing data...')
    write_data_START = datetime.now()
    ### work ###
    compressed_with_header.write(compressed_data)
    ############
    write_data_END = datetime.now()
    write_data_TIME = write_data_END - write_data_START
    print('file', 'write data', write_data_TIME)
    #print(str(write_data_TIME) + ' for data to write...\n')
    
if __name__ == '__main__':
    #import cProfile, pstats
    #profiler = cProfile.Profile()
    #profiler.enable()
    main()
    #profiler.disable()
    #stats = pstats.Stats(profiler).sort_stats('cumtime')
    #stats.print_stats()

#%load_ext snakeviz
#%snakeviz main() 
