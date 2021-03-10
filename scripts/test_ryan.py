# imports
#import compress
import unittest
import gzip


# Testing gzip functionality
class TestGZ(unittest.TestCase):
    def test_compress(self):
        #
        # 1f 8b Standard GZIP declaration
        # 08    Compression method: 0x08 represents GZIP
        # 08    Flags (see below)
        # a2 42 b8 4d   Timestamp
        # 00    Extra flags
        # 03    Operating System
        # Figure 2: standard 10-byte GZIP header
        # The flags byte, byte 4, is interpreted as shown in table 1. In the
        # case of the attachment displayed in figure 1, only bit 8 is set,
        # indicating that a null-terminated name string follows the header.
        # Bit mask (in big-endian format)       Meaning
        # 00000001      Text follows            b01
        # 00000010      Header CRC follows      b02
        # 00000100      "Extra" follows         b04
        # 00001000      Name follows            b08
        # 00010000      Comment follows         b10
        # Table 1: Flag bit meanings
        # In essence, the flags byte indicates that the header can be followed
        # by up to five null- terminated strings, which must at least be
        # skipped over before the actual gzipped-proper content appears. In
        # this case, it is the 9-byte ASCII-encoded string:
        # 67  75  6e  7a  69  70 2e  63  00
        base_text = "adsoifjoasiefjlskdfj;lsdkjf"
        gzip_cdata = [b'1f', b'8b',  # Standard GZIP declaration
                      b'08', # Compression method: 0x08 represents GZIP
                      b'08', # Flags  -> Name follows
                      b'04', b'82', b'3e', b'60', b'00', b'03', b'74', b'65', b'73', b'74', b'2e', b'74', b'78', b'74', b'00',
                      b'4b', b'4c', b'29', b'ce', b'cf', b'4c', b'cb', b'ca',
                      b'4f', b'2c', b'ce', b'4c', b'4d', b'cb', b'ca', b'29', b'ce',
                      b'4e', b'49', b'cb', b'b2', b'ce', b'29', b'4e', b'c9', b'ce',
                      b'4a', b'e3', b'02', b'00', b'c0', b'7b', b'33', b'80', b'1c',
                      b'00', b'00', b'00']
        cdata = gzip.compress(bytes("adsoifjoasiefjlskdfj;lsdkjf","utf-8"))
        #self.assertEqual(len(gzip_cdata),len(cdata))
        for i in range(len(cdata)):
            print(i,int(gzip_cdata[i],16), cdata[i])

if __name__ == '__main__':
    unittest.main()
