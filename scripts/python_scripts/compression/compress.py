import gzip
import zlib
import bz2

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
        c_bitstring = gzip_compress(serialized_bitstring, 0)

    # ZLIB
    elif codec == 'zlib':
        c_bitstring = zlib_compress(serialized_bitstring)
        header_size = 0

    # BZ2
    elif codec == 'bz2':
        c_bitstring = bz2_compress(serialized_bitstring)
        header_size = 4

    return c_bitstring[header_size:]

def gzip_compress(s_bitstring, time):
    '''
    uses python_scripts's gzip.compress to compress a serialized bitstring

    INPUT
        s_bitstring = serialized bitstring from the serialize_data method in serialize_body.py
        time = mtime argument for gzip.compress

    OUTPUT
        c_bitstring = compressed bitstring (using python_scripts's gzip.compress() function)

    '''

    c_bitstring = gzip.compress(s_bitstring, mtime=time)
    return c_bitstring


def zlib_compress(s_bitstring):
    '''
    uses python_scripts's zlib.compress to compress a serialized bitstring

    INPUT
        s_bitstring = serialized bitstring from the serialize_data method in serialize_body.py

    OUTPUT
        c_bitstring = compressed bitstring (using python_scripts's zlib.compress() function)

    '''

    c_bitstring = zlib.compress(s_bitstring)
    return c_bitstring


def bz2_compress(s_bitstring):
    '''
    uses python_scripts's zlib.compress to compress a serialized bitstring

    INPUT
        s_bitstring = serialized bitstring from the serialize_data method in serialize_body.py

    OUTPUT
        c_bitstring = compressed bitstring (using python_scripts's zlib.compress() function)

    '''

    c_bitstring = bz2.compress(s_bitstring)
    return c_bitstring
