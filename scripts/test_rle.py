import unittest
import ref-alt.py

class TestSerializationToDeserialization(unittest.TestCase):
    def test_snp(self):

    def test_indel(self):
        indel1 = 'ACGT'
        indel2 = 'AACGT'
        indel3 = 'ACCGT'
        indel4 = 'ACGGT'
        indel5 = 'ACGTT'
        indel6 = 'AACCGGTT'
        indel7 ='AAAAGCGCGAAATTAGAGGCGGA'
        self.assertEqual(ref)

if __name__ == '__main__':
    unittest.main()
