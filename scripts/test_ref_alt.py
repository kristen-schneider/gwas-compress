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

    def test_snp(self):
        self.assertEqual(ref_alt.run_length_encoding(self.snpA), 11)
    def test_indel(self):
        self.assertEqual(ref_alt.run_length_encoding(self.indel1), 11213141)

if __name__ == '__main__':
    unittest.main()
