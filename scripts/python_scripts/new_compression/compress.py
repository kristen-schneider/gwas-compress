import gzip
import zlib
import bz2
from pyfastpfor import *
import fpzip
import zfpy
import numpy as np
from datetime import datetime
import sys


def compress_bitstring(serialized_bitstring, codec):
    """
    compress a serialized bitstring using specified compression method

    INPUT
        compression_method: e.g. gzip, zlib, etc...
        s_bitstring = serialized bitstring from the serialize_data method in serialize_body.py

    OUTPUT
        c_bitstring = compressed bitstring

    """

    # GZIP
    if codec == 'gzip':
        compressed_bitstring = gzip_compress(serialized_bitstring, 0)
        header_size = 10

    # ZLIB
    elif codec == 'zlib':
        compressed_bitstring = zlib_compress(serialized_bitstring)
        header_size = 0

    # BZ2
    elif codec == 'bz2':
        compressed_bitstring = bz2_compress(serialized_bitstring)
        header_size = 4
    else: return None
    return compressed_bitstring[header_size:]

def compress_numpy_array(typed_column, codec):
    """
    compress a serialized bitstring using specified compression method

    INPUT
        compression_method: e.g. gzip, zlib, etc...
        s_bitstring = serialized bitstring from the serialize_data method in serialize_body.py

    OUTPUT
        c_bitstring = compressed bitstring

    """
    # PYFAST-integer compression
    if codec in getCodecList():
        compressed_numpy_array = pyfast_compress(typed_column, codec)
        compressed_bitstring = compressed_numpy_array.tobytes(order='C')
    # fpzip-floating point compression
    elif codec == 'fpzip':
        compressed_bitstring = fpzip_compress(typed_column)
    # zfpy-floating point or integer compression
    elif codec == 'zfpy':
        compressed_bitstring = zfpy_compress(typed_column)
    else:
        print('cannot identify numpy-based codec: ', codec)
        compressed_bitstring = None
    return compressed_bitstring

def gzip_compress(s_bitstring, time):
    '''
    uses python_scripts's gzip.compress to compress a serialized bitstring

    INPUT
        s_bitstring = serialized bitstring from the serialize_data method in serialize_body.py
        time = mtime argument for gzip.compress

    OUTPUT
        c_bitstring = compressed bitstring (using python_scripts's gzip.compress() function)

    '''

    compressed_bitstring = gzip.compress(s_bitstring, mtime=time)
    return compressed_bitstring


def zlib_compress(s_bitstring):
    '''
    uses python_scripts's zlib.compress to compress a serialized bitstring

    INPUT
        s_bitstring = serialized bitstring from the serialize_data method in serialize_body.py

    OUTPUT
        c_bitstring = compressed bitstring (using python_scripts's zlib.compress() function)

    '''

    compressed_bitstring = zlib.compress(s_bitstring)
    return compressed_bitstring


def bz2_compress(s_bitstring):
    '''
    uses python_scripts's zlib.compress to compress a serialized bitstring

    INPUT
        s_bitstring = serialized bitstring from the serialize_data method in serialize_body.py

    OUTPUT
        c_bitstring = compressed bitstring (using python_scripts's zlib.compress() function)

    '''

    compressed_bitstring = bz2.compress(s_bitstring)
    return compressed_bitstring

def pyfast_compress(typed_column, codec):
    """
    compresses a single column of data using pyfastpfor codecs
    INPUT
        typed_column = column as proper type (list of ints, rather than strings)
        codec = method of compression for given column (one of the 33 codecs)

    OUTPUT
        compressed_column = compressed data
    """
    column_i_BEFORE = sys.getsizeof(typed_column)
    column_i_START = datetime.now()
    ### work ###
    # convert input array to numpy array
    numpy_array = np.array(typed_column, dtype=np.uint32, order='C')
    np_arr_size = numpy_array.size
    buffer_size = 3 * 32
    # allocate space for compressed data
    comp_arr = np.zeros(np_arr_size + buffer_size, dtype=np.uint32, order='C')
    # get codec method from pyfastpfor and use it for compression
    codec_method = getCodec(codec)
    comp_arr_size = codec_method.encodeArray(numpy_array, np_arr_size, comp_arr, len(comp_arr))
    ############
    column_i_END = datetime.now()
    column_i_TIME = column_i_END - column_i_START
    # print(column_i_TIME, 'for column with codec ', codec, ' to compress')
    column_i_AFTER = sys.getsizeof(comp_arr[0:comp_arr_size])
    column_i_RATIO = float(column_i_BEFORE / column_i_AFTER)

    return comp_arr[0:comp_arr_size]

def fpzip_compress(typed_column):
    """
    compresses floats with fpzip codec.
    """
    # converts all data to floats (can take in integers, but will convert).
    numpy_array = np.array(typed_column, dtype=np.float32, order='C')
    compressed_bitstring = fpzip.compress(numpy_array, precision=0, order='C')
    return compressed_bitstring

def zfpy_compress(typed_column):
    """
    compresses floats and integers with fpzip codec.
    """
    # converts all data to floats (can take in integers, but will convert).
    numpy_array = np.array(typed_column, dtype=np.float32, order='C')
    compressed_bitstring = zfpy.compress_numpy(numpy_array)
    return compressed_bitstring

# print(compress_numpy_array([1,2,3,4], 'zfpy'))
# print(compress_numpy_array([1,2,3,4], 'fpzip'))
# print(compress_numpy_array([1,2,3,4], 'fastpfor128'))

