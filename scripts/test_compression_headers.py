# imports
import unittest
import random
import serialize
import compress
import decompress
import deserialize
import numpy as np

# DEFINED (should be same for all files)
type_to_bytes_code_book = {1: 5, 2: 8, 3: 5}


#
class TestCorrectHeader(unittest.TestCase):
    I = [1]*10
    RI = (random.randint(0,22) for i in range(100))

    # 10 bytes
    gzip_header = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff'
    zlib_header = b''


    def test_gzip_header(self):
        self.assertEqual(compress.compress_data(
            1,
            serialize.serialize_list(
                self.I,
                1,
                type_to_bytes_code_book[1]), 0)[0][0:len(self.gzip_header)],
                         self.gzip_header)
        self.assertEqual(compress.compress_data(
                                1,
                                serialize.serialize_list(
                                    self.I,
                                    1,
                                    type_to_bytes_code_book[1]),0)[1],
                         len(self.gzip_header))
        self.assertEqual(compress.compress_data(
            1,
            serialize.serialize_list(
                self.RI,
                1,
                type_to_bytes_code_book[1]), 0)[0][0:len(self.gzip_header)],
                         self.gzip_header)
        self.assertEqual(compress.compress_data(
            1,
            serialize.serialize_list(
                self.RI,
                1,
                type_to_bytes_code_book[1]), 0)[1],
                         len(self.gzip_header))

    def test_zlib_header(self):
        self.assertEqual(compress.compress_data(
            2,
            serialize.serialize_list(
                self.I,
                1,
                type_to_bytes_code_book[1]), 0)[0][0:len(self.zlib_header)],
                         self.zlib_header)
        self.assertEqual(compress.compress_data(
            2,
            serialize.serialize_list(
                self.I,
                1,
                type_to_bytes_code_book[1]), 0)[1],
                         len(self.zlib_header))
        self.assertEqual(compress.compress_data(
            2,
            serialize.serialize_list(
                self.RI,
                1,
                type_to_bytes_code_book[1]), 0)[0][0:len(self.zlib_header)],
                         self.zlib_header)
        self.assertEqual(compress.compress_data(
            2,
            serialize.serialize_list(
                self.RI,
                1,
                type_to_bytes_code_book[1]), 0)[1],
                         len(self.zlib_header))

    def test_zlib_header(self):
        self.assertEqual(compress.compress_data(
            2,
            serialize.serialize_list(
                self.I,
                1,
                type_to_bytes_code_book[1]), 0)[0][0:len(self.zlib_header)],
                         self.zlib_header)
        self.assertEqual(compress.compress_data(
            2,
            serialize.serialize_list(
                self.I,
                1,
                type_to_bytes_code_book[1]), 0)[1],
                         len(self.zlib_header))
        self.assertEqual(compress.compress_data(
            2,
            serialize.serialize_list(
                self.RI,
                1,
                type_to_bytes_code_book[1]), 0)[0][0:len(self.zlib_header)],
                         self.zlib_header)
        self.assertEqual(compress.compress_data(
            2,
            serialize.serialize_list(
                self.RI,
                1,
                type_to_bytes_code_book[1]), 0)[1],
                         len(self.zlib_header))


if __name__ == '__main__':
    unittest.main()