import unittest
from scripts import ref_alt


class TestSerializationToDeserialization(unittest.TestCase):
    snpA = 'A'
    snpC = 'C'
    snpG = 'G'
    snpT = 'T'
    indel1 = 'ACGT'
    indel2 = 'AACGT'
    indel3 = 'ACCGT'
    indel4 = 'ACGGT'
    indel5 = 'ACGTT'
    indel6 = 'AACCGGTT'
    indel7 = 'AAAAGCGCGAAATTAGAGGCGGA'

    def test_snp(self):
        self.assertEqual(ref_alt.run_length_encoding(self.snpA), 11)
        self.assertEqual(ref_alt.run_length_encoding(self.snpC), 21)
        self.assertEqual(ref_alt.run_length_encoding(self.snpG), 31)
        self.assertEqual(ref_alt.run_length_encoding(self.snpT), 41)
    def test_indel(self):
        self.assertEqual(ref_alt.run_length_encoding(self.indel1), 11213141)
        self.assertEqual(ref_alt.run_length_encoding(self.indel2), 12213141)
        self.assertEqual(ref_alt.run_length_encoding(self.indel3), 11223141)
        self.assertEqual(ref_alt.run_length_encoding(self.indel4), 11213241)
        self.assertEqual(ref_alt.run_length_encoding(self.indel5), 11213142)
        self.assertEqual(ref_alt.run_length_encoding(self.indel6), 12223242)
        self.assertEqual(ref_alt.run_length_encoding(self.indel7), 143121312131134211311132213211)

if __name__ == '__main__':
    unittest.main()
