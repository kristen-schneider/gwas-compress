import gzip

def decompress_data(c_bitstring):
    '''
    uses python's gzip.decompress
    
    INPUTS
    c_bitstring: compressed bitstring (using python's gzip.compress)
    OUTPUTS
    decompressed bitstring (original bitstring from serialize function)
    '''
    return gzip.decompress(c_bitstring)
