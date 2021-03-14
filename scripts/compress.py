import gzip
import serialize


def compress_data(s_bitstring, t):
    '''
    uses python's gzip.compress
    
    INPUTS
    s_bitstring: serialized bitstring from the serialize_data method in serialize.py
    OUTPUTS
    compressed bitstring (using python's gzip.compress() function)
    '''
    return gzip.compress(s_bitstring, mtime=t)

#A=[1,1,1,1,1]
#A_s = serialize.serialize_data(A,5)
#A_c = compress_data(A_s, 0)

#print(A_s)
#print(A_c)
#print(gzip.compress(A_s, mtime=0))
