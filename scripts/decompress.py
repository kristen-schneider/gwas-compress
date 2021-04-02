import gzip
import zlib

def decompress_data(compression_method, c_bitstring):
    '''
    decompress a compressed bitstring using specified compression method

    INPUT
    compression_method: e.g. gzip, zlib, etc...
    c_bitstring = serialized bitstring from the serialize_data method in serialize.py

    OUTPUT
    dc_bitstring = compressed bitstring

    '''
    # switch statement seems more appropriate here
    # GZIP
    if compression_method == 1:
        c_bitstring = gzip_decompress(c_bitstring)
    # ZLIB
    elif compression_method == 2:
        c_bitstring = zlib_decompress(c_bitstring)

    return c_bitstring

def gzip_decompress(c_bitstring):
    '''
    uses python's gzip.decompress to decompressed a compressed, serialized bitstring
    
    INPUT
    c_bitstring = compressed bitstring (using python's gzip.compress)
    
    OUTPUT
    dc_bitstring = decompressed bitstring (original bitstring from serialize function)
    
    '''

    dc_bitstring = gzip.decompress(c_bitstring)
    return dc_bitstring


def zlib_decompress(c_bitstring):
    '''
    uses python's zlib.decompress to decompressed a compressed, serialized bitstring

    INPUT
    c_bitstring = compressed bitstring (using python's gzip.compress)

    OUTPUT
    dc_bitstring = decompressed bitstring (original bitstring from serialize function)

    '''

    dc_bitstring = zlib.decompress(c_bitstring)
    return dc_bitstring
