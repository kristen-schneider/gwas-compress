import unittest
import ref-alt.py

class TestSerializationToDeserialization(unittest.TestCase):
    def test_snp(self):

    def test_indel(self):

        # serialize_list(column_list, num_bytes_per_val, data_type)
        self.assertEqual(serialize.serialize_list([1, 1, 1, 1, 1], 1, type_to_bytes_code_book[1]), self.I_s)