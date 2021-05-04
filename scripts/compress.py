import gzip
import zlib
import bz2

def compress_data(compression_method, s_bitstring, time):
    '''
    compress a serialized bitstring using specified compression method
    
    INPUT
    compression_method: e.g. gzip, zlib, etc...
    s_bitstring = serialized bitstring from the serialize_data method in serialize.py
    time = optional: mtime argument for gzip.compress
    
    OUTPUT
    c_bitstring = compressed bitstring
    
    '''
    # switch statement seems more appropriate here
    # GZIP
    if compression_method == 1:
        c_bitstring = gzip_compress(s_bitstring, time)
        header = 10
    # ZLIB
    elif compression_method == 2:
        c_bitstring = zlib_compress(s_bitstring)
        header = 0
    # BZ2
    elif compression_method == 3:
        c_bitstring = bz2_compress(s_bitstring)
        header = 4

    return c_bitstring, header

def gzip_compress(s_bitstring, time):
    '''
    uses python's gzip.compress to compress a serialized bitstring

    INPUT
    s_bitstring = serialized bitstring from the serialize_data method in serialize.py
    time = mtime argument for gzip.compress

    OUTPUT
    c_bitstring = compressed bitstring (using python's gzip.compress() function)

    '''

    c_bitstring = gzip.compress(s_bitstring, mtime=time)
    return c_bitstring

def zlib_compress(s_bitstring):
    '''
    uses python's zlib.compress to compress a serialized bitstring

    INPUT
    s_bitstring = serialized bitstring from the serialize_data method in serialize.py

    OUTPUT
    c_bitstring = compressed bitstring (using python's zlib.compress() function)

    '''

    c_bitstring = zlib.compress(s_bitstring)
    return c_bitstring

def bz2_compress(s_bitstring):
    '''
    uses python's zlib.compress to compress a serialized bitstring

    INPUT
    s_bitstring = serialized bitstring from the serialize_data method in serialize.py

    OUTPUT
    c_bitstring = compressed bitstring (using python's zlib.compress() function)

    '''

    c_bitstring = zlib.compress(s_bitstring)
    return c_bitstring

