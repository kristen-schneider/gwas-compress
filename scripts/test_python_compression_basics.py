# imports

#import compress
import unittest
import gzip
import os
import python_compression_basics

'''
https://www.w3.org/Graphics/PNG/RFC-1951
https://tools.ietf.org/rfc/rfc1951.txt
https://tools.ietf.org/rfc/rfc1952.txt
http://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art001
https://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art053
'''

# Testing python gzip functionality
class TestPythonGZ(unittest.TestCase):

    # toy test files
    BASE_TEXT = 'abcde12345'
    #BASE_TEXT = 'adsoifjoasiefjlskdfj;lsdkjf'
    REG_FILE = '/Users/kristen/Desktop/compression_sandbox/reg_test.txt'
    GZ_FILE = '/Users/kristen/Desktop/compression_sandbox/test.txt.gz'
    #GZ_FILE = '/Users/kristen/Desktop/compression_sandbox/ryan.txt.gz'


    # genome test files
    GWAS_GZ_FILE = '/Users/kristen/Desktop/compression_sandbox/data/100000-gwas.tsv.gz'


    #for i in python_compression_basics.python_gz_compress(BASE_TEXT): print(i)
    def test_get_base_text(self):
        print('...testing base text from non gzipped file...')
        self.assertEqual(python_compression_basics.get_base_text(self.REG_FILE), self.BASE_TEXT)


    # test valid gzip file with gzip.open()    
    def test_python_gz_open(self):
        print('...testing read gzip file...')
        self.assertEqual(python_compression_basics.python_gz_open(self.GZ_FILE), 0)         # valid gzip file
        self.assertEqual(python_compression_basics.python_gz_open(self.REG_FILE), 1)     # invalid gzip file

# test first four bytes of header
    # *might need to change test for bytes 3 and 4 if we see differnt compression methods or flags
    def test_python_gz_compress(self):
        print('...testing first four bytes of compressed string...31 139 8 0...')
        self.assertEqual(python_compression_basics.python_gz_compress(self.BASE_TEXT)[0], 31)    #ID1 --> gz format          
        self.assertEqual(python_compression_basics.python_gz_compress(self.BASE_TEXT)[1], 139)   #ID2 --> gz format
        self.assertEqual(python_compression_basics.python_gz_compress(self.BASE_TEXT)[2], 8)     #deflate compression method
        self.assertEqual(python_compression_basics.python_gz_compress(self.BASE_TEXT)[3], 0)     #flags (none, default)

    # testing decompression of a string back into base text
    def test_python_gz_decompress(self):
        print('...testing decompression of a string back into base text...')
        pc_text = python_compression_basics.python_gz_compress(self.BASE_TEXT)
        self.assertEqual(python_compression_basics.python_gz_decompress(pc_text), self.BASE_TEXT)

    # return content from 
    def test_cmnd_gz_to_text(self):
        print('...testing decompression of data from commandline gzip back into base text...')
        content = python_compression_basics.cmnd_gz_read(self.GZ_FILE)
        self.assertEqual(python_compression_basics.cmnd_gz_to_text(content), self.BASE_TEXT)



    #def test_compress(self):   
        # gzip test.txt | xxd -b (prints binary representation of file):
        # gzip test.txt | xxd 
        # bytearray.fromhex("7279616e2e74787400").decode()         
        # "{0:08b}".format(int('1b', 16))
        #python_gzip = gzip.compress(bytes("adsoifjoasiefjlskdfj;lsdkjf","utf-8"))
        #print('n', 'cmdline', 'python')
        #for i in range(max(len(cmdline_gzip), len(python_gzip))):
        #    print(i, end=' ')
        #    try: print(int(cmdline_gzip[i], 16), end=' ')
        #    except IndexError: print('-')
        #    try: print(python_gzip[i])
        #    except IndexError: print('-')

if __name__ == '__main__':
    unittest.main()

