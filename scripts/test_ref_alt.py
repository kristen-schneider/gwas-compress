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

    def test_assumption1(self):
        fifteen_SNVs_bool = True
        SNVs_bool = True

        # 00 000000000000000000000000000000
        self.assertEqual(ref_alt.assumption1(self.snpA), 0)
        # 00 010101010101010101010101010101
        self.assertEqual(ref_alt.assumption1(self.snpC), 357913941)
        # 00 101010101010101010101010101010
        self.assertEqual(ref_alt.assumption1(self.snpG), 715827882)
        # 00 111111111111111111111111111111
        self.assertEqual(ref_alt.assumption1(self.snpT), 1073741823)
        # 00 100100100100100100100100100100
        self.assertEqual(ref_alt.assumption1(self.mix1), 613566756)
        # 00 110100110100110100110100110100
        self.assertEqual(ref_alt.assumption1(self.mix2), 886263092)
        # 00 110001110001110001110001110001
        self.assertEqual(ref_alt.assumption1(self.mix3), 835132529)
        # 00 101001101001101001101001101001
        self.assertEqual(ref_alt.assumption1(self.mix4), 698784361)
        # 00 001110001110001110001110001110
        self.assertEqual(ref_alt.assumption1(self.mix5), 238609294)
        # 00 010110010110010110010110010110
        self.assertEqual(ref_alt.assumption1(self.mix6), 374957462)
        # 00 001111001111001111001111001111
        self.assertEqual(ref_alt.assumption1(self.mix7), 255652815)
        # 00 100011100011100011100011100011
        self.assertEqual(ref_alt.assumption1(self.mix8), 596523235)
        # 00 011000111101100011110110001111
        self.assertEqual(ref_alt.assumption1(self.mix9), 418790799)
        # 00 010011001001001100100100110010
        self.assertEqual(ref_alt.assumption1(self.mix10), 321177906)
        # 00 110001100111000110011100011001
        self.assertEqual(ref_alt.assumption1(self.mix11), 832333593)
        # 00 000000010000000001000000000100
        self.assertEqual(ref_alt.assumption1(self.mix12), 4198404)
        # 00 010101111001001110010011100100
        self.assertEqual(ref_alt.assumption1(self.mix13), 367322340)
        # 00 010101010100000000000101010101
        self.assertEqual(ref_alt.assumption1(self.mix14), 357564757)
        # 00 100011000000101010010101111111
        self.assertEqual(ref_alt.assumption1(self.mix15), 587375999)


if __name__ == '__main__':
    unittest.main()
