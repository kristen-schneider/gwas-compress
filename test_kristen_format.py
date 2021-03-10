# imports
#import compress
import unittest
import gzip

# Testing gzip functionality
class TestGZ(unittest.TestCase):
    def test_compress(self):
        # https://www.w3.org/Graphics/PNG/RFC-1951
        # https://tools.ietf.org/rfc/rfc1951.txt
        # https://tools.ietf.org/rfc/rfc1952.txt
        # http://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art001
        # https://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art053

        base_text = "adsoifjoasiefjlskdfj;lsdkjf"
        
        # gzip test.txt | xxd -b (prints binary representation of file):
                
            # 00011111 10001011 # ID1, ID2 --> to identify the file as being in gzip format
            # 00001000 # "deflate" compression method, customarily used by gzip
            # 00001000 # flags, 08 --> null-terminated name string follows the header
            # 01010011 10011110 00111110 01100000 # time stamp
            # 00000000 # extra flags
            # 00000011 # operating system 
            # 01110010 01111001 01100001 01101110 00101110 01110100 01111000 01110100 00000000 # null terminating name string which follows the header
            
            # 1-bit block, 2-bit encoding, 14-bit pre-header(5-bit length of literals tree, 5-bit length of distance tree, initial huffman key)
            # 01001011 01001100 00101001 (split by reading L->R, but then individual peices are read R->L.
            #       0, block = not last [a single bit indicating whether or not this block is the last block (1 = yes, 0 = no),
            #       10, encoding = fixed huffman codes [two bits indicating the block type: 00 = uncompressed, 01 = compressed using fixed Huffman codes
            #                                           10 = compressed using dynamic Huffman codes, 11 = invalid]            
            #       14-bit preheader:   
            #           01011, huffman-literal = 26
            #           01001, huffman-distance = 18
            #           1000, initial huffman key = 1
            #           * = (1+4)*3 = 15 bits of code length declarations
            #       next * bits (last 7 from previous byte: 0101001 + 11001110
            #           010 4   16
            #           100 1   17
            #           111 7   18
            #           001 4   0
            #           110 3   8
            # huffman decoding on this data
            # 11001111 01001100 11001011 11001010 01001111 00101100
            # 11001110 01001100 01001101 11001011 11001010 00101001
            # 11001110 01001110 01001001 11001011 10110010 11001110
            # 00101001 01001110 11001001 11001110 01001010 11100011
            # 00000010 00000000 11000000 01111011 00110011 10000000
            # 00011100 00000000 00000000 00000000
            #
            
        # gzip test.txt | xxd 
        cmdline_gzip = [b'1f', b'8b', # ID1, ID2 --> to identify the file as being in gzip format 
                        b'08', # "deflate" compression method, customarily used by gzip
                        b'08', # flags, 08 --> null-terminated name string follows the header
                        b'00', b'9d', b'3e', b'60', # time stamp
                        b'00', # extra flags
                        b'03', # operating system
                        # AFT
                        b'72', b'79', b'61', b'6e', b'2e', b'74', b'78', b'74', b'00',  # null terminating name string which follows the header
                                                                                        # bytearray.fromhex("7279616e2e74787400").decode()         
                        # AFTER 
                        # After these first 19 bytes, bit ordering begins to matter..
                        # The block format is a single bit indicating whether or not this block is the last block (1 = yes, 0 = no),
                        #   and two bits indicating the block type: 00 = uncompressed, 01 = compressed using fixed Huffman codes, 
                    
                        b'4b', b'4c', b'29', b'ce', 
                        b'cf', b'4c', b'cb', b'ca', b'4f', b'2c', b'ce',
                        b'4c', b'4d', b'cb', b'ca', b'29', b'ce', b'4e', b'49', b'cb', b'b2',
                        b'ce', b'29', b'4e', b'c9', b'ce', b'4a', b'e3', b'02', b'00', b'c0',
                        b'7b', b'33', b'80', b'1c', b'00', b'00', b'00']
        python_gzip = gzip.compress(bytes("adsoifjoasiefjlskdfj;lsdkjf","utf-8"))
        print('cmdline', len(cmdline_gzip))
        print('python', len(python_gzip))
        #self.assertEqual(len(gzip_cdata),len(cdata))
        print('n', 'cmdline', 'python')
        for i in range(max(len(cmdline_gzip), len(python_gzip))):
            print(i, end=' ')
            try: print(int(cmdline_gzip[i], 16), end=' ')
            except IndexError: print('-')
            try: print(python_gzip[i])
            except IndexError: print('-')

if __name__ == '__main__':
    unittest.main()
