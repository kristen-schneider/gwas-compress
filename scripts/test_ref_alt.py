import unittest
from scripts import ref_alt


class TestSerializationToDeserialization(unittest.TestCase):

    snpA = 'A'*15
    snpC = 'C'*15
    snpG = 'G'*15
    snpT = 'T'*15
    snp1 = 'ACG'*5
    snp2 = 'ACT'*5
    snp3 = 'CAT'*5
    snp4 = 'CGG'*5
    snp5 = 'GTA'*5
    snp6 = 'GCC'*5
    snp7 = 'TTA'*5
    snp8 = 'TAG'*5
    snp9 = 'TTAGC'*3
    snp10 = 'GATAC'*3
    snp11 = 'CGCAT'*3
    snp12 = 'ACAAA'*3
    snp13 = 'ACGTACGTACGTCCC'
    snp14 = 'CCCCCAAAAACCCCC'
    snp15 = 'TTTCCCGGGAAATAG'
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
        self.assertEqual(ref_alt.encode_SNVs(self.snp1), 613566756)
        # 00 110100110100110100110100110100
        self.assertEqual(ref_alt.encode_SNVs(self.snp2), 886263092)
        # 00 110001110001110001110001110001
        self.assertEqual(ref_alt.encode_SNVs(self.snp3), 835132529)
        # 00 101001101001101001101001101001
        self.assertEqual(ref_alt.encode_SNVs(self.snp4), 698784361)
        # 00 001110001110001110001110001110
        self.assertEqual(ref_alt.encode_SNVs(self.snp5), 238609294)
        # 00 010110010110010110010110010110
        self.assertEqual(ref_alt.encode_SNVs(self.snp6), 374957462)
        # 00 001111001111001111001111001111
        self.assertEqual(ref_alt.encode_SNVs(self.snp7), 255652815)
        # 00 100011100011100011100011100011
        self.assertEqual(ref_alt.encode_SNVs(self.snp8), 596523235)
        # 00 011000111101100011110110001111
        self.assertEqual(ref_alt.encode_SNVs(self.snp9), 418790799)
        # 00 010011001001001100100100110010
        self.assertEqual(ref_alt.encode_SNVs(self.snp10), 321177906)
        # 00 110001100111000110011100011001
        self.assertEqual(ref_alt.encode_SNVs(self.snp11), 832333593)
        # 00 000000010000000001000000000100
        self.assertEqual(ref_alt.encode_SNVs(self.snp12), 4198404)
        # 00 010101111001001110010011100100
        self.assertEqual(ref_alt.encode_SNVs(self.snp13), 367322340)
        # 00 010101010100000000000101010101
        self.assertEqual(ref_alt.encode_SNVs(self.snp14), 357564757)
        # 00 100011000000101010010101111111
        self.assertEqual(ref_alt.encode_SNVs(self.snp15), 587375999)

    snp16 = 'A' * 25
    snp17 = 'C' * 25
    snp18 = 'G' * 25
    snp19 = 'T' * 25
    snp20 = 'T' * 40
    snp21 = 'C' * 11
    snp22 = 'ACGT'*7
    def test_encode_SNVs_greater_than_15(self):
        # 00 000000000000000000000000000000, 10 000000101000000000000000000000
        self.assertEqual(ref_alt.col_input(self.snp16), [0, 2157969408])
        # 00 010101010101010101010101010101, 10 000000101001010101010101010101
        self.assertEqual(ref_alt.col_input(self.snp17), [357913941, 2158318933])
        # 00 101010101010101010101010101010, 10 000000101010101010101010101010
        self.assertEqual(ref_alt.col_input(self.snp18), [715827882, 2158668458])
        # 00 111111111111111111111111111111, 10 000000101011111111111111111111
        self.assertEqual(ref_alt.col_input(self.snp19), [1073741823, 2159017983])
        # 00 111111111111111111111111111111, 00 111111111111111111111111111111, 10 0000001010 11111111111111111111
        self.assertEqual(ref_alt.col_input(self.snp20), [1073741823, 1073741823, 2159017983])
        # 10 0000001010 01010101010101010101, 10 0000000001 00000000000000000001
        self.assertEqual(ref_alt.col_input(self.snp21), [2158318933, 2148532225])
        # ACGTACGTACGTACG TACGTACGTA CGT
        # 00 100100111001001110010011100100, 10 0000001010 00111001001110010011, 10 0000000011 00000000000000111001
        self.assertEqual(ref_alt.col_input(self.snp22), [618980580, 2158203795, 2150629433])

    indelA = ['AAAAA']*1
    indelC = ['CCCCC']*1
    indelG = ['GGGGG']*1
    indelT = ['TTTTT']*1
    def test_encode_INDELs_only(self):
        # 11 000000010100000000000000000000
        self.assertEqual(ref_alt.col_input(self.indelA), [3226468352])
        # 11 000000010100000000000101010101
        self.assertEqual(ref_alt.col_input(self.indelC), [3226468693])
        # 11 000000010100000000001010101010
        self.assertEqual(ref_alt.col_input(self.indelG), [3226469034])
        # 11 000000010100000000001111111111
        self.assertEqual(ref_alt.col_input(self.indelT), [3226469375])

    snp_indel1 = ['A', 'A', 'A', 'AAAAA']
    snp_indel2 = ['A', 'A', 'A', 'CCCCC']
    snp_indel3 = ['A', 'C', 'T', 'G', 'GATACA']
    def test_encode_SNPs_INDEL(self):
        # 10 000000001100000000000000000000, 11 000000010100000000000000000000
        self.assertEqual(ref_alt.col_input(self.snp_indel1), [2150629376, 3226468352])
        # 10 000000001100000000000000000000, 11 000000010100000000000101010101
        self.assertEqual(ref_alt.col_input(self.snp_indel2), [2150629376, 3226468693])
        # 10 000000010000000000000010110100, 11 000000011000000000000100110010
        self.assertEqual(ref_alt.col_input(self.snp_indel3), [2151678132, 3227517234])

    snp_indel_snp1 = ['A', 'A', 'A', 'AAAAA', 'A', 'A', 'A']
    snp_indel_snp2 = ['A', 'A', 'A', 'CCCCC', 'A', 'A', 'A']
    snp_indel_snp3 = ['A', 'C', 'T', 'G', 'GATACA', 'A', 'A', 'A']
    def test_encode_SNPs_INDEL_SNPs(self):
        # 10 000000001100000000000000000000, 11 000000010100000000000000000000, 10 000000001100000000000000000000
        self.assertEqual(ref_alt.col_input(self.snp_indel_snp1), [2150629376, 3226468352, 2150629376])
        # 10 000000001100000000000000000000, 11 000000010100000000000101010101, 10 000000001100000000000000000000
        self.assertEqual(ref_alt.col_input(self.snp_indel_snp2), [2150629376, 3226468693, 2150629376])
        # 10 000000010000000000000010110100, 11 000000011000000000000100110010, 10 000000001100000000000000000000
        self.assertEqual(ref_alt.col_input(self.snp_indel_snp3), [2151678132, 3227517234, 2150629376])

    snp_indel_snp_indel1 = ['A', 'A', 'A', 'AAAAA', 'A', 'A', 'A', 'AAAAA']
    snp_indel_snp_indel2 = ['A', 'A', 'A', 'CCCCC', 'A', 'A', 'A', 'CCCCC']
    snp_indel_snp_indel3 = ['A', 'C', 'T', 'G', 'GATACA', 'A', 'A', 'A', 'GATACA']
    def test_encode_SNPs_INDEL_SNPs_INDEL(self):
        # 10 000000001100000000000000000000, 11 000000010100000000000000000000, 10 000000001100000000000000000000, 11 000000010100000000000000000000
        self.assertEqual(ref_alt.col_input(self.snp_indel_snp_indel1), [2150629376, 3226468352, 2150629376, 3226468352])
        # 10 000000001100000000000000000000, 11 000000010100000000000101010101, 10 000000001100000000000000000000, 11 000000010100000000000101010101
        self.assertEqual(ref_alt.col_input(self.snp_indel_snp_indel2), [2150629376, 3226468693, 2150629376, 3226468693])
        # 10 000000010000000000000010110100, 11 000000011000000000000100110010, 10 000000001100000000000000000000, 11 000000011000000000000100110010
        self.assertEqual(ref_alt.col_input(self.snp_indel_snp_indel3), [2151678132, 3227517234, 2150629376, 3227517234])


    junk1 = ['T', 'G', 'G', 'C', 'T', 'T', 'T', 'C', 'G', 'A',
             'CT',
             'A', 'G', 'T', 'T', 'T', 'T', 'G', 'G', 'G', 'C', 'G', 'T', 'C', 'A', 'A',
             'T', 'T', 'C', 'A', 'G', 'A', 'C', 'A', 'G', 'G', 'A',
             'AAAAAAAAAA AATATATATATATAT ATATATATATAT',
             'G', 'G', 'G', 'T', 'C', 'C', 'A', 'G', 'A', 'C', 'T', 'C', 'T', 'A', 'C', 'C',
             'G', 'T', 'T', 'C', 'A', 'T', 'C', 'C', 'C',
             'TA',
             'C', 'C', 'C', 'A', 'C', 'C', 'C', 'C', 'C', 'G',
             'ACAGGAGGGCGGG']
    # # 10 0000001010 11101001111111011000
    # # 11 0000001010 00000000000000001101
    # # 00 000001111001101010111111111000
    # # 10 0000001011 10100001001000011111
    # # 10 0000000001 00000000000000000000
    # # 11 0000001010 00000000000000000000, 00 110011001100110011001100110000, 00 000000110011001100110011001100

    def test_junk(self):
        self.assertEqual(ref_alt.col_input(self.junk1), [2158927832, 3223322637, 31895544, 2159677983,
                                                         2148532224])





if __name__ == '__main__':
    unittest.main()
