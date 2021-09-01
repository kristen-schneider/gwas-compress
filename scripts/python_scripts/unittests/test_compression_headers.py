# imports
import unittest
import random
import numpy as np

import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from new_compression import serialize
from new_compression import compress
from decompression import decompress
from decompression import deserialize

# DEFINED (should be same for all files)
type_to_bytes_code_book = {1: 5, 2: 8, 3: 5}


#
class TestCorrectHeader(unittest.TestCase):
    I = [1]*10
    RI = (random.randint(0,22) for i in range(100))

    # 10 bytes
    gzip_header = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff'
    zlib_header = b''
    bz2_header = b'BZh9'


    def test_gzip_header(self):
        self.assertEqual(compress.compress_bitstring(
            1,
            serialize.serialize_list(
                self.I,
                1,
                type_to_bytes_code_book[1]), 0)[0][0:len(self.gzip_header)],
                         self.gzip_header)
        self.assertEqual(compress.compress_bitstring(
            1,
            serialize.serialize_list(
                self.I,
                1,
                type_to_bytes_code_book[1]),0)[1], len(self.gzip_header))

        self.assertEqual(compress.compress_bitstring(
            1,
            serialize.serialize_list(
                self.RI,
                1,
                type_to_bytes_code_book[1]), 0)[0][0:len(self.gzip_header)],
                         self.gzip_header)
        self.assertEqual(compress.compress_bitstring(
            1,
            serialize.serialize_list(
                self.RI,
                1,
                type_to_bytes_code_book[1]), 0)[1],
                         len(self.gzip_header))

    def test_zlib_header(self):
        self.assertEqual(compress.compress_bitstring(
            2,
            serialize.serialize_list(
                self.I,
                1,
                type_to_bytes_code_book[1]), 0)[0][0:len(self.zlib_header)],
                         self.zlib_header)
        self.assertEqual(compress.compress_bitstring(
            2,
            serialize.serialize_list(
                self.I,
                1,
                type_to_bytes_code_book[1]), 0)[1],
                         len(self.zlib_header))
        self.assertEqual(compress.compress_bitstring(
            2,
            serialize.serialize_list(
                self.RI,
                1,
                type_to_bytes_code_book[1]), 0)[0][0:len(self.zlib_header)],
                         self.zlib_header)
        self.assertEqual(compress.compress_bitstring(
            2,
            serialize.serialize_list(
                self.RI,
                1,
                type_to_bytes_code_book[1]), 0)[1],
                         len(self.zlib_header))

    def test_bz2_header(self):
        self.assertEqual(compress.compress_bitstring(
            3,
            serialize.serialize_list(
                self.I,
                1,
                type_to_bytes_code_book[1]), 0)[0][0:len(self.bz2_header)],
                         self.bz2_header)
        self.assertEqual(compress.compress_bitstring(
            3,
            serialize.serialize_list(
                self.I,
                1,
                type_to_bytes_code_book[1]), 0)[1],
                         len(self.bz2_header))
        self.assertEqual(compress.compress_bitstring(
            3,
            serialize.serialize_list(
                self.RI,
                1,
                type_to_bytes_code_book[1]), 0)[0][0:len(self.bz2_header)],
                         self.bz2_header)
        self.assertEqual(compress.compress_bitstring(
            3,
            serialize.serialize_list(
                self.RI,
                1,
                type_to_bytes_code_book[1]), 0)[1],
                         len(self.bz2_header))


if __name__ == '__main__':
    unittest.main()