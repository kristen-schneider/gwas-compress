import gzip
import zlib
import bz2
import fpzip
import zfpy

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
        dc_bitstring = gzip_decompress(c_bitstring)
    # ZLIB
    elif compression_method == 'zlib':
        dc_bitstring = zlib_decompress(c_bitstring)
    # BZ2
    elif compression_method == 'bz2':
        dc_bitstring = bz2_decompress(c_bitstring)
    # FPZIP
    elif compression_method == 'fpzip':
        dc_bitstring = fpzip_decompress(c_bitstring)
    # ZFPY
    elif compression_method == 'zfpy':
        dc_bitstring = zfpy_decompress(c_bitstring)
    return dc_bitstring

def gzip_decompress(c_bitstring):
    """
    uses python_scripts's gzip.decompress to decompressed a compressed, serialized bitstring

    INPUT
        c_bitstring = compressed bitstring (using python_scripts's gzip.compress)

    OUTPUT
        dc_bitstring = decompressed bitstring (original bitstring from serialize function)
    """
    gzip_header=b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff'
    dc_bitstring = gzip.decompress(gzip_header+c_bitstring)
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
    bz2_header = b'BZh9'
    dc_bitstring = bz2.decompress(bz2_header+c_bitstring)
    return dc_bitstring


def fpzip_decompress(c_bitstring):
    """
    uses fpzip's decompress method to decompress a numpy array and return only the given array.

    INPUT
        c_bitstring: compressed bitstring
    OUTPUT
        np_arry = numpy array of data (converted to 1D list)
    """
    np_arr = fpzip.decompress(c_bitstring)
    return np_arr.tolist()[0][0][0]


def zfpy_decompress(c_bitstring):
    """
    """
    np_arr = zfpy.decompress_numpy(c_bitstring)
    return np_arr.tolist()
