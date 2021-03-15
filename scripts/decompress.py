import gzip

def decompress_data(c_bitstring):
    '''
    uses python's gzip.decompress to decompressed a compressed, serialized bitstring
    
    INPUTS
    c_bitstring: compressed bitstring (using python's gzip.compress)
    
    OUTPUTS
    decompressed bitstring (original bitstring from serialize function)
    
    '''

    dc_bitstring = gzip.decompress(c_bitstring)
    return dc_bitstring
