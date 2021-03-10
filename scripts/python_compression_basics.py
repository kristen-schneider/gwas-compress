import gzip
import os
import binascii
from binascii import unhexlify

BASE_TEXT = 'abcde12345'
REG_FILE = '/Users/kristen/Desktop/compression_sandbox/reg_test.txt'
#GZ_FILE = '/Users/kristen/Desktop/compression_sandbox/test.txt.gz'
GZ_FILE = '/Users/kristen/Desktop/compression_sandbox/ryan.txt.gz'
BIG_GZ_FILE = '/Users/kristen/Desktop/compression_sandbox/data/compress_columns_out_file.txt.gz'

GZ_FILE_CONTENTS = b'\x1f\x8b\x08\x08\xe6\x0f\x40\x60\x00\x03\x74\x65\x73\x74\x2e\x74\x78\x74\x00\x4b\x4c\x4a\x4e\x49\x35\x34\x32\x36\x31\xe5\x02\x00\x7e\x52\xd1\x50\x0b\x00\x00\x00'


def main():
    print('running python_compression_basics main.py...')
    #x = python_gz_open('/Users/kristen/Desktop/compression_sandbox/test.txt.gz')
    #print(get_base_text(REG_FILE))
    #print(x)
    #cd = python_gz_compress(BASE_TEXT)
    #print(type(cd), cd)
    #print(type(gzip.decompress(cd)), gzip.decompress(cd))
    #cmnd_gz_to_hex(GZ_FILE)
    #print(gzip.decompress(cd).decode('utf-8'))
    #h=cmnd_gz_to_hex(GZ_FILE)
    #print(h)
    #print(cmnd_gz_hex_to_text(h))
    #for i in os.path.splitext(GZ_FILE)[0].split('/')[-1]: print(i)
    
def get_base_text(f):
    '''
    return text from original file

    INPUTS
    f: uncompressed file
    OUTPUTS
    return string which is concattenated version of all lines in file.
        
    '''
    base_text = ''
    f_open = open(f, 'r')
    for line in f_open:
        print(line)
        base_text += line        
    
    f_open.close()
    return base_text
    

def python_gz_open(f_gz):
    '''
    checks if python's gzip library will open and read the gzipped file
    
    INPUTS
    f_gz: gzip compressed file 
    OUTPUTS
    return 0 if gzip.read can open file
    return 1 if gzip.read throws OSError
    
    '''
    try:
        f_open = gzip.open(f_gz, 'rb')
        f_open.read(1)
        f_open.close()
    except OSError:     
        f_open.close()
        return 1
    return 0


def python_gz_compress(s):
    '''
    uses python's gzip.compress function
    >> 1-2: ID1, ID2
    >> 3: compression
    >> 4: flags
    >> 5-8: time stamp
    >> 9: extra flagis
    >> 10: os
    
    INPUTS
    s: string         
    OUTPUTS:
    return bytes object of compressed data for a string
    '''
    return gzip.compress(bytes(s, 'utf-8'))

def bytes_decompress(b):
    '''
    uses python's gzip.decompress function
    
    INPUTS
    b: bytes object
    OUTPUTS
    string format of decompressed 
    '''
    return gzip.decompress(b).decode('utf-8').rstrip()

# returns hex of command line gzipped file
def cmnd_gz_read(f_gz):
    '''
    reads commandline gzipped file
    
    INPUTS
    f_gz: command line gzip compressed file
    OUTPUTS
    bytes object of compressed data
    '''
    with open(f_gz, 'rb') as f_open:
        content = f_open.read()
        print(type(content), content)
    return content



    


# run main
if __name__=='__main__': main()
