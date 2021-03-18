import gzip

def decompress_data(c_bitstring):
    '''
    uses python's gzip.decompress to decompressed a compressed, serialized bitstring
    
    INPUT
    c_bitstring = compressed bitstring (using python's gzip.compress)
    
    OUTPUT
    dc_bitstring = decompressed bitstring (original bitstring from serialize function)
    
    '''

    dc_bitstring = gzip.decompress(c_bitstring)
    return dc_bitstring
