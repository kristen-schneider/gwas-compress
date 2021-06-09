import unittest
from scripts import ref_alt


class TestSerializationToDeserialization(unittest.TestCase):
    snpA = 'A'*15
    snpC = 'C'*15
    snpG = 'G'*15
    snpT = 'T'*15
    mix1 = 'ACG'*5
    mix2 = 'ACT'*5
    mix3 = 'CAT'*5
    mix4 = 'CGG'*5
    mix5 = 'GTA'*5
    mix6 = 'GCC'*5
    mix7 = 'TTA'*5
    mix8 = 'TAG'*5
    mix9 = 'TTAGC'*3
    mix10 = 'GATAC'*3
    mix11 = 'CGCAT'*3
    mix12 = 'ACAAA'*3
    mix13 = 'ACGTACGTACGTCCC'
    mix14 = 'CCCCCAAAAACCCCC'
    mix15 = 'TTTCCCGGGAAATAG'
    mix16 = 'A'*25
    mix17 = 'C'*25
    mix18 = 'G'*25
    mix19 = 'T'*25

    def test_encode_SNVs_length_15(self):
        # 00 000000000000000000000000000000
        self.assertEqual(ref_alt.encode_SNVs(self.snpA), 0)
        # 00 010101010101010101010101010101
        self.assertEqual(ref_alt.encode_SNVs(self.snpC), 357913941)
        # 00 101010101010101010101010101010
        self.assertEqual(ref_alt.encode_SNVs(self.snpG), 715827882)
        # 00 111111111111111111111111111111
        self.assertEqual(ref_alt.encode_SNVs(self.snpT), 1073741823)
        # 00 100100100100100100100100100100
        self.assertEqual(ref_alt.encode_SNVs(self.mix1), 613566756)
        # 00 110100110100110100110100110100
        self.assertEqual(ref_alt.encode_SNVs(self.mix2), 886263092)
        # 00 110001110001110001110001110001
        self.assertEqual(ref_alt.encode_SNVs(self.mix3), 835132529)
        # 00 101001101001101001101001101001
        self.assertEqual(ref_alt.encode_SNVs(self.mix4), 698784361)
        # 00 001110001110001110001110001110
        self.assertEqual(ref_alt.encode_SNVs(self.mix5), 238609294)
        # 00 010110010110010110010110010110
        self.assertEqual(ref_alt.encode_SNVs(self.mix6), 374957462)
        # 00 001111001111001111001111001111
        self.assertEqual(ref_alt.encode_SNVs(self.mix7), 255652815)
        # 00 100011100011100011100011100011
        self.assertEqual(ref_alt.encode_SNVs(self.mix8), 596523235)
        # 00 011000111101100011110110001111
        self.assertEqual(ref_alt.encode_SNVs(self.mix9), 418790799)
        # 00 010011001001001100100100110010
        self.assertEqual(ref_alt.encode_SNVs(self.mix10), 321177906)
        # 00 110001100111000110011100011001
        self.assertEqual(ref_alt.encode_SNVs(self.mix11), 832333593)
        # 00 000000010000000001000000000100
        self.assertEqual(ref_alt.encode_SNVs(self.mix12), 4198404)
        # 00 010101111001001110010011100100
        self.assertEqual(ref_alt.encode_SNVs(self.mix13), 367322340)
        # 00 010101010100000000000101010101
        self.assertEqual(ref_alt.encode_SNVs(self.mix14), 357564757)
        # 00 100011000000101010010101111111
        self.assertEqual(ref_alt.encode_SNVs(self.mix15), 587375999)

    def test_encode_SNVs_greater_than_15(self):
        # 00 000000000000000000000000000000, 01 000000101000000000000000000000
        self.assertEqual(ref_alt.col_input(self.mix16), [0, 1084227584])
        # 00 010101010101010101010101010101, 01 000000101001010101010101010101
        self.assertEqual(ref_alt.col_input(self.mix17), [357913941, 1084577109])
        # 00 101010101010101010101010101010, 01 000000101010101010101010101010
        self.assertEqual(ref_alt.col_input(self.mix18), [715827882, 1084926634])
        # 00 111111111111111111111111111111, 01 000000101011111111111111111111
        self.assertEqual(ref_alt.col_input(self.mix19), [1073741823, 1085276159])

if __name__ == '__main__':
    unittest.main()
