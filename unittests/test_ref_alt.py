import unittest
from scripts import ref_alt


class TestEncodeRefAltToInt(unittest.TestCase):

    def test_encode_SNVs(self):
        # 001101 00000000000000000000000000
        self.assertEqual(ref_alt.encode_SNVs('A'*13, 13, 0), 872415232)
        # 001101 01010101010101010101010101
        self.assertEqual(ref_alt.encode_SNVs('C'*13, 13, 0), 894784853)
        # 001101 10101010101010101010101010
        self.assertEqual(ref_alt.encode_SNVs('G'*13, 13, 0), 917154474)
        # 001101 11111111111111111111111111
        self.assertEqual(ref_alt.encode_SNVs('T'*13, 13, 0), 939524095)


    indelA = 'AAAAA'*1
    indelC = 'CCCCC'*1
    indelG = 'GGGGG'*1
    indelT = 'TTTTT'*1
    def test_encode_INDELs(self):
        # 1 00000000101 00000000000000000000
        self.assertEqual(ref_alt.encode_INDEL(self.indelA), [2152726528])
        # 1 00000000101 00000000000101010101
        self.assertEqual(ref_alt.encode_INDEL(self.indelC), [2152726869])
        # 1 00000000101 00000000001010101010
        self.assertEqual(ref_alt.encode_INDEL(self.indelG), [2152727210])
        # 1 00000000101 00000000001111111111
        self.assertEqual(ref_alt.encode_INDEL(self.indelT), [2152727551])

    snp_indel1 = ['A', 'A', 'A', 'AAAAA']
    snp_indel2 = ['A', 'A', 'A', 'CCCCC']
    snp_indel3 = ['A', 'C', 'T', 'G', 'GATACA']
    def test_encode_SNP_INDEL(self):
        # 0 00011 00000000000000000000000000, 1 00000000101 00000000000000000000
        self.assertEqual(ref_alt.encode_column(self.snp_indel1), [201326592, 2152726528])
        # 0 00011 00000000000000000000000000, 1 00000000101 00000000000101010101
        self.assertEqual(ref_alt.encode_column(self.snp_indel2), [201326592, 2152726869])
        # 0 00100 00000000000000000010110100, 1 00000000110 00000000000100110010
        self.assertEqual(ref_alt.encode_column(self.snp_indel3), [268435636, 2153775410])

    snp_indel_snp1 = ['A', 'A', 'A', 'AAAAA', 'A', 'A', 'A']
    snp_indel_snp2 = ['A', 'A', 'A', 'CCCCC', 'A', 'A', 'A']
    snp_indel_snp3 = ['A', 'C', 'T', 'G', 'GATACA', 'A', 'A', 'A']
    def test_encode_SNPs_INDEL_SNPs(self):
        # 0 00011 00000000000000000000000000, 1 00000000101 00000000000000000000, 0 00011 00000000000000000000000000
        self.assertEqual(ref_alt.encode_column(self.snp_indel_snp1), [201326592, 2152726528, 201326592])
        # 0 00011 00000000000000000000000000, 1 00000000101 00000000000101010101, 0 00011 00000000000000000000000000
        self.assertEqual(ref_alt.encode_column(self.snp_indel_snp2), [201326592, 2152726869, 201326592])
        # 0 00100 00000000000000000010110100, 1 00000000110 00000000000100110010, 0 00100 00000000000000000010110100
        self.assertEqual(ref_alt.encode_column(self.snp_indel_snp3), [268435636, 2153775410, 201326592])

    snp_indel_snp_indel1 = ['A', 'A', 'A', 'AAAAA', 'A', 'A', 'A', 'AAAAA']
    snp_indel_snp_indel2 = ['A', 'A', 'A', 'CCCCC', 'A', 'A', 'A', 'CCCCC']
    snp_indel_snp_indel3 = ['A', 'C', 'T', 'G', 'GATACA', 'A', 'A', 'A', 'GATACA']
    def test_encode_SNPs_INDEL_SNPs_INDEL(self):
        # 0 00011 00000000000000000000000000, 1 00000000101 00000000000000000000, 0 00011 00000000000000000000000000, 1 00000000101 00000000000000000000
        self.assertEqual(ref_alt.encode_column(self.snp_indel_snp_indel1), [201326592, 2152726528, 201326592, 2152726528])
        # 0 00011 00000000000000000000000000, 1 00000000101 00000000000101010101, 0 00011 00000000000000000000000000, 1 00000000101 00000000000101010101
        self.assertEqual(ref_alt.encode_column(self.snp_indel_snp_indel2), [201326592, 2152726869, 201326592, 2152726869])
        # 0 00100 00000000000000000010110100, 1 00000000110 00000000000100110010, 0 00100 00000000000000000010110100, 1 00000000110 00000000000100110010
        self.assertEqual(ref_alt.encode_column(self.snp_indel_snp_indel3), [268435636, 2153775410, 201326592, 2153775410])


    junk1 = ['T', 'G', 'G', 'C', 'T', 'T', 'T', 'C', 'G', 'A',
             'CT',
             'A', 'G', 'T', 'T', 'T', 'T', 'G', 'G', 'G', 'C', 'G', 'T', 'C', 'A', 'A',
             'T', 'T', 'C', 'A', 'G', 'A', 'C', 'A', 'G', 'G', 'A',
             'AAAAAAAAAAAATATATATATATATATATATATATAT',
             'G', 'G', 'G', 'T', 'C', 'C', 'A', 'G', 'A', 'C', 'T', 'C', 'T', 'A', 'C',
             'C', 'G', 'T', 'T', 'C', 'A', 'T', 'C', 'C', 'C',
             'TA',
             'C', 'C', 'C', 'A', 'C', 'C', 'C', 'C', 'C', 'G',
             'ACAGGAGGGCGGG']

    # 0 01010 00000000100111111101101011
    # 1 00000000010 00000000000000001101
    # 0 01101 01111001101010111111111000
    # 0 01101 00101000010010000111110000
    # 1 00000100101 00000000000000000000, 0 01101 11001100110011001100110000, 0 01101 00110011001100110011001100, 0 00001 00000000000000000000000011
    # 0 01101 11011101001000010111101010
    # 0 01100 00010101110001111110010100
    # 1 00000000010 00000000000000000011
    # 0 01010 00000010010101010100010101
    # 1 00000001101 01101010001010000100, 0 00011 00000000000000000000101010

    def test_junk(self):
        self.assertEqual(ref_alt.encode_column(self.junk1), [671252331, 2149580813, 904310776, 882975216,
                                                         2186280960, 926102320, 885837004, 67108867,
                                                         930383338, 811016084, 2149580803, 671700245,
                                                         2161549956, 201326634])





if __name__ == '__main__':
    unittest.main()