import unittest
from scripts import string_int

class TestEncodeRefAltToInt(unittest.TestCase):

    def test_encode_SNVs(self):
        # 001101 00000000000000000000000000
        self.assertEqual(string_int.encode_SNVs('A'*13, 13, 0), 872415232)

class TestDecodeIntToRefAlt(unittest.TestCase):
    def test_decode_SNVs(self):
        self.assertEqual(string_int.decode_snv(201326635), ['T','G','G'])

    def test_decode_INDEL(self):
        self.assertEqual(string_int.decode_indel([2151678180]), 'ACGT')
        self.assertEqual(string_int.decode_indel([2150629419]), 'TGG')
        self.assertEqual(string_int.decode_indel([2150546155, 335545018]), 'TGGTGGTGGTGGTGG')

