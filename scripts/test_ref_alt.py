import unittest
from scripts import ref_alt


class TestEncodeRefAltToInt(unittest.TestCase):

    def test_encode_SNVs(self):
        # 001101 00000000000000000000000000
        self.assertEqual(ref_alt.encode_SNVs('A'*13, 13), 872415232)
        # 001101 01010101010101010101010101
        self.assertEqual(ref_alt.encode_SNVs('C'*13, 13), 894784853)
        # 001101 10101010101010101010101010
        self.assertEqual(ref_alt.encode_SNVs('G'*13, 13), 917154474)
        # 001101 11111111111111111111111111
        self.assertEqual(ref_alt.encode_SNVs('T'*13, 13), 939524095)


    indelA = 'AAAAA'*1
    indelC = 'CCCCC'*1
    indelG = 'GGGGG'*1
    indelT = 'TTTTT'*1
    def test_encode_INDELs(self):
        # 1 00101 00000000000000000000000000
        self.assertEqual(ref_alt.encode_INDEL(self.indelA), [2483027968])
        # 1 00101 00000000000000000101010101
        self.assertEqual(ref_alt.encode_INDEL(self.indelC), [2483028309])
        # 1 00101 00000000000000001010101010
        self.assertEqual(ref_alt.encode_INDEL(self.indelG), [2483028650])
        # 1 00101 00000000000000001111111111
        self.assertEqual(ref_alt.encode_INDEL(self.indelT), [2483028991])

    snp_indel1 = ['A', 'A', 'A', 'AAAAA']
    snp_indel2 = ['A', 'A', 'A', 'CCCCC']
    snp_indel3 = ['A', 'C', 'T', 'G', 'GATACA']
    def test_encode_SNP_INDEL(self):
        # 0 00011 00000000000000000000000000, 1 00101 00000000000000000000000000
        self.assertEqual(ref_alt.encode_column(self.snp_indel1), [201326592, 2483027968])
        # 0 00011 00000000000000000000000000, 1 00101 00000000000000000101010101
        self.assertEqual(ref_alt.encode_column(self.snp_indel2), [201326592, 2483028309])
        # 0 00100 00000000000000000010110100, 1 00110 00000000000000000100110010
        self.assertEqual(ref_alt.encode_column(self.snp_indel3), [268435636, 2550137138])

    snp_indel_snp1 = ['A', 'A', 'A', 'AAAAA', 'A', 'A', 'A']
    snp_indel_snp2 = ['A', 'A', 'A', 'CCCCC', 'A', 'A', 'A']
    snp_indel_snp3 = ['A', 'C', 'T', 'G', 'GATACA', 'A', 'A', 'A']
    def test_encode_SNPs_INDEL_SNPs(self):
        # 0 00011 00000000000000000000000000, 1 00101 00000000000000000000000000, 0 00011 00000000000000000000000000
        self.assertEqual(ref_alt.encode_column(self.snp_indel_snp1), [201326592, 2483027968, 201326592])
        # 0 00011 00000000000000000000000000, 1 00101 00000000000000000101010101, 0 00011 00000000000000000000000000
        self.assertEqual(ref_alt.encode_column(self.snp_indel_snp2), [201326592, 2483028309, 201326592])
        # 0 00100 00000000000000000010110100, 1 00110 00000000000000000100110010, 0 00100 00000000000000000010110100
        self.assertEqual(ref_alt.encode_column(self.snp_indel_snp3), [268435636, 2550137138, 201326592])
    #
    # snp_indel_snp_indel1 = ['A', 'A', 'A', 'AAAAA', 'A', 'A', 'A', 'AAAAA']
    # snp_indel_snp_indel2 = ['A', 'A', 'A', 'CCCCC', 'A', 'A', 'A', 'CCCCC']
    # snp_indel_snp_indel3 = ['A', 'C', 'T', 'G', 'GATACA', 'A', 'A', 'A', 'GATACA']
    # def test_encode_SNPs_INDEL_SNPs_INDEL(self):
    #     # 10 000000001100000000000000000000, 11 000000010100000000000000000000, 10 000000001100000000000000000000, 11 000000010100000000000000000000
    #     self.assertEqual(ref_alt.col_input(self.snp_indel_snp_indel1), [2150629376, 3226468352, 2150629376, 3226468352])
    #     # 10 000000001100000000000000000000, 11 000000010100000000000101010101, 10 000000001100000000000000000000, 11 000000010100000000000101010101
    #     self.assertEqual(ref_alt.col_input(self.snp_indel_snp_indel2), [2150629376, 3226468693, 2150629376, 3226468693])
    #     # 10 000000010000000000000010110100, 11 000000011000000000000100110010, 10 000000001100000000000000000000, 11 000000011000000000000100110010
    #     self.assertEqual(ref_alt.col_input(self.snp_indel_snp_indel3), [2151678132, 3227517234, 2150629376, 3227517234])
    #
    #
    # junk1 = ['T', 'G', 'G', 'C', 'T', 'T', 'T', 'C', 'G', 'A',
    #          'CT',
    #          'A', 'G', 'T', 'T', 'T', 'T', 'G', 'G', 'G', 'C', 'G', 'T', 'C', 'A', 'A',
    #          'T', 'T', 'C', 'A', 'G', 'A', 'C', 'A', 'G', 'G',
    #          'A',
    #          'AAAAAAAAAAAATATATATATATATATATATATATAT',
    #          'G', 'G', 'G', 'T', 'C', 'C', 'A', 'G', 'A', 'C', 'T', 'C', 'T', 'A', 'C',
    #          'C', 'G', 'T', 'T', 'C', 'A', 'T', 'C', 'C', 'C',
    #          'TA',
    #          'C', 'C', 'C', 'A', 'C', 'C', 'C', 'C', 'C', 'G',
    #          'ACAGGAGGGCGGG']
    # # 10 0000001010 00100111111101101011
    # # 11 0000000010 00000000000000001101
    # # 00 000001111001101010111111111000
    # # 10 0000001010 10100001001000011111
    # # 10 0000000001 00000000000000000000
    # # 11 0000100101 00000000000000000000, 00 110011001100110011001100110000, 00 000000110011001100110011001100
    # # 00 010011011101001000010111101010
    # # 10 0000001010 01010111000111111001
    # # 11 0000000010 000000000000000000011
    # # 10 0000001010 10010101010100010101
    # # 11 0000001010 01101010001010000100, 10 0000000011 00000000000000101010
    #
    # def test_junk(self):
    #     # [2158133099, 3223322637, 31895544, 2158629407,
    #     #  2148532224, 3260022784, 858993456, 13421772,
    #     #  326403562, 2158326265, 6446645251, 2158581013,
    #     #  3232146052, 2150629418]
    #
    #     # [2158133099, 3223322637, 31895544, 2158629407,
    #     #  2148532224, 3260022784, 858993456, 3355443,
    #     #  326403562, 2158326265, 3223322627, 2158581013,
    #     #  3235291780, 42]
    #
    #     self.assertEqual(ref_alt.col_input(self.junk1), [2158133099, 3223322637, 31895544, 2158629407,
    #                                                      2148532224, 3231711232, 858993456, 13421772,
    #                                                      326403562, 2158326265, 6446645251, 2158581013,
    #                                                      3232146052, 2150629418])





if __name__ == '__main__':
    unittest.main()
