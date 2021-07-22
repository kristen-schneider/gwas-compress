import gzip
import zlib
import bz2

def decompress_data(compression_method, c_bitstring):
    """
    decompress a compressed bitstring using specified compression method

    INPUT
        compression_method: e.g. gzip, zlib, etc...
        c_bitstring = serialized bitstring from the serialize_data method in serialize_body.py

    OUTPUT
        dc_bitstring = compressed bitstring
    """
    # GZIP
    if compression_method == 'gzip':
        c_bitstring = gzip_decompress(c_bitstring)
    # ZLIB
    elif compression_method == 'zlib':
        c_bitstring = zlib_decompress(c_bitstring)
    # BZ2
    elif compression_method == 'bz2':
        c_bitstring = bz2_decompress(c_bitstring)

    return c_bitstring

def gzip_decompress(c_bitstring):
    """
    uses python_scripts's gzip.decompress to decompressed a compressed, serialized bitstring

    INPUT
        c_bitstring = compressed bitstring (using python_scripts's gzip.compress)

    OUTPUT
        dc_bitstring = decompressed bitstring (original bitstring from serialize function)
    """

    dc_bitstring = gzip.decompress(c_bitstring)
    return dc_bitstring


def zlib_decompress(c_bitstring):
    """
    uses python_scripts's zlib.decompress to decompressed a compressed, serialized bitstring

    INPUT
        c_bitstring = compressed bitstring (using python_scripts's gzip.compress)

    OUTPUT
        dc_bitstring = decompressed bitstring (original bitstring from serialize function)
    """

    dc_bitstring = zlib.decompress(c_bitstring)
    return dc_bitstring

def bz2_decompress(c_bitstring):
    """
    uses python_scripts's bz2.decompress to decompressed a compressed, serialized bitstring

    INPUT
        c_bitstring = compressed bitstring (using python_scripts's bz2.compress)

    OUTPUT
        dc_bitstring = decompressed bitstring (original bitstring from serialize function)
    """

    dc_bitstring = bz2.decompress(c_bitstring)
    return dc_bitstring
