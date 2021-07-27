def get_compression_method_header(compression_method):
    """
    returns header for different methods of existing compression

    INPUT
        string of compression method (e.g. 'gzip')

    OUTPUT
        bitstring of given compression method header (common to all compressed data)
    """
    compression_method_header = b''

    # GZIP
    if compression_method == 'gzip':
        compression_method_header = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff'
    # BZ2
    elif compression_method == 'bz2':
        compression_method_header = b'BZh9'

    return compression_method_header