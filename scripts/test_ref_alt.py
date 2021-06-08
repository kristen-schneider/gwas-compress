import unittest
from scripts import ref_alt


class TestSerializationToDeserialization(unittest.TestCase):
    snpA = 'A'*15
    snpC = 'C'*15
    snpG = 'G'*15
    snpT = 'T'*15
    mix1 = 'ACG'*5
    mix2 = 'ACT'*5


    def test_assumption1(self):
        fifteen_SNVs_bool = True
        SNVs_bool = True

        # 00 000000000000000000000000000000
        self.assertEqual(ref_alt.assumption1(fifteen_SNVs_bool, SNVs_bool, self.snpA), 0)
        # 00 010101010101010101010101010101
        self.assertEqual(ref_alt.assumption1(fifteen_SNVs_bool, SNVs_bool, self.snpC), 357913941)
        # 00 101010101010101010101010101010
        self.assertEqual(ref_alt.assumption1(fifteen_SNVs_bool, SNVs_bool, self.snpG), 715827882)
        # 00 111111111111111111111111111111
        self.assertEqual(ref_alt.assumption1(fifteen_SNVs_bool, SNVs_bool, self.snpT), 1073741823)
        # 00 000110000110000110000110000110
        self.assertEqual(ref_alt.assumption1(fifteen_SNVs_bool, SNVs_bool, self.mix1), 102261126)
        # 00 000111000111000111000111000111
        self.assertEqual(ref_alt.assumption1(fifteen_SNVs_bool, SNVs_bool, self.mix1), 119304647)

    # def test_indel(self):
    #     self.assertEqual(ref_alt.run_length_encoding(self.indel1), 11213141)

if __name__ == '__main__':
    unittest.main()
