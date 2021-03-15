import gzip

def compress_data(s_bitstring, time):
    '''
    uses python's gzip.compress to compress a serialized bitstring
    
    INPUTS
    s_bitstring: serialized bitstring from the serialize_data method in serialize.py
    time = mtime argument for gzip.compress
    OUTPUTS
    c_bitstring = compressed bitstring (using python's gzip.compress() function)
    
    '''

    c_bitstring = gzip.compress(s_bitstring, mtime=time) 
    return c_bitstring

