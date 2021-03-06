# imports
import unittest
import numpy as np

import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from new_compression import serialize
from new_compression import compress
from decompression import decompress
from decompression import deserialize

# DEFINED (should be same for all files)
type_to_bytes_code_book = {1: 5, 2: 8, 3: 5}


# data_type_code_book = {int: 1, float: 2, str: 3}


# Testing serialization --> compression --> decompression --> deserialization
class TestSerializationToDeserialization(unittest.TestCase):
    # block_size = 5
    block_size = 5
    mtime = 0  # for reproducibility we choose mtime = 0 for unittests
    int_type = 0
    str_type = 1
    float_type = 2
    column_data_types = []

    # integer data
    I = [['1', '1', '1', '1', '1']]
    I_s = b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01'
    I_c = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xffc````d\xc0B\x00\x00s \xa8\xa5\x19\x00\x00\x00'
    I_dc = b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01'
    I_ds = [[1, 1, 1, 1, 1]]

    # float data
    F = [['1.2', '3.45', '-6.78e+00', '9.000e-05', '0.1234e+05']]
    F_s = b'?\xf3333333@\x0b\x99\x99\x99\x99\x99\x9a\xc0\x1b\x1e\xb8Q\xeb\x85\x1f?\x17\x97\xcc9\xff\xd6\x0f@\xc8\x1a\x00\x00\x00\x00\x00'
    F_c = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff\xb3\xffl\x0c\x06\x0e\xdc3A`\xd6\x01i\xb9\x1d\x81\xaf[\xe5\xed\xc5\xa7\x9f\xb1\xfc\x7f\x8d\xdf\xe1\x84\x14\x03\x08\x00\x00\xb4\xd3\xa4b(\x00\x00\x00'
    F_dc = b'?\xf3333333@\x0b\x99\x99\x99\x99\x99\x9a\xc0\x1b\x1e\xb8Q\xeb\x85\x1f?\x17\x97\xcc9\xff\xd6\x0f@\xc8\x1a\x00\x00\x00\x00\x00'
    F_ds = [[1.2, 3.45, -6.78e+00, 9.000e-05, 0.1234e+05]]

    # float data with NA values
    NA = [['1.2', '3.45', 'NA', 'NA', '0.1234e+05']]
    NA_s = b'?\xf3333333@\x0b\x99\x99\x99\x99\x99\x9a\x7f\xf8\x00\x00\x00\x00\x00\x00\x7f\xf8\x00\x00\x00\x00\x00\x00@\xc8\x1a\x00\x00\x00\x00\x00'
    NA_c = b"\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff\xb3\xffl\x0c\x06\x0e\xdc3A`V\xfd\x0f\x060\x80\xd1\x0e'\xa4\xc04\x00\xa8\xb8\xa1\x81(\x00\x00\x00"
    NA_dc = b'?\xf3333333@\x0b\x99\x99\x99\x99\x99\x9a\x7f\xf8\x00\x00\x00\x00\x00\x00\x7f\xf8\x00\x00\x00\x00\x00\x00@\xc8\x1a\x00\x00\x00\x00\x00'
    NA_ds = [[1.2, 3.45, np.nan, np.nan, 0.1234e+05]]

    # string data
    S = [['A', 'C', 'T', 'G', 'A']]
    S_s = b'ACTGA'
    S_c = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xffst\x0eqw\x04\x00\x9f_F\xff\x05\x00\x00\x00'
    S_dc = b'ACTGA'
    S_ds = [['A', 'C', 'T', 'G', 'A']]

    s_bug = [['chr', 'pos', 'ref', 'alt', 'af_cases_EUR', 'af_controls_EUR', 'beta_EUR', 'se_EUR', 'pval_EUR',
              'low_confidence_EUR']]

    # integer and string data
    IS = [['1', '1', '1', '1', '1'], ['A', 'C', 'T', 'G', 'A']]
    IS_s = b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01ACTGA'
    IS_c = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xffc````d\xc0B8:\x87\xb8;\x02\x00\xca.\x1d\xe5\x1e\x00\x00\x00'
    IS_dc = b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01ACTGA'
    IS_ds = [[1, 1, 1, 1, 1], ['A', 'C', 'T', 'G', 'A']]

    # header-like data
    # i think i am goign to decompress this a little different. just use decompress_data and go one header list at a time
    HEADER = [[1, 1], ['\t'], ['chr', 'pos', 'ref', 'alt'], [1, 1, 3, 3], [4]]
    HEADER_s = b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\tchrposrefalt\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x03\x00\x00\x00\x00\x03\x00\x00\x00\x00\x04'
    HEADER_c = b"\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xffc````d\x00\x11\x9c\xc9\x19E\x05\xf9\xc5E\xa9i\x899%\x0cpa\x10\xc1\x0c'X\x00\x96\xa7\xc7\x860\x00\x00\x00"
    HEADER_dc = b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\tchrposrefalt\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x03\x00\x00\x00\x00\x03\x00\x00\x00\x00\x04'
    HEADER_ds = [[1, 1], ['\t'], ['chr', 'pos', 'ref', 'alt'], [1, 1, 3, 3], [4]]

    # def test_bug(self):
    #     self.assertEqual(serialize.serialize_list_columns(self.bug, type_to_bytes_code_book), self.bug_s)
    #     self.assertEqual(compress.compress_data(self.bug_s, self.mtime), self.bug_c)
    #     self.assertEqual(decompress.decompress_data(self.bug_c), self.bug_dc) 
    #     self.assertEqual(deserialize.deserialize_block_bitstring(self.bug_dc, 1, self.data_types, type_to_bytes_code_book), self.bug_ds)

    def test_serialize(self):

        # serialize_list(column_list, num_bytes_per_val, data_type)
        self.assertEqual(serialize.serialize_list([1, 1, 1, 1, 1], 1, type_to_bytes_code_book[1]), self.I_s)
        self.assertEqual(
            serialize.serialize_list([1.2, 3.45, -6.78e+00, 9.000e-05, 0.1234e+05], 2, type_to_bytes_code_book[2]),
            self.F_s)
        self.assertEqual(
            serialize.serialize_list([1.2, 3.45, np.nan, np.nan, 0.1234e+05], 2, type_to_bytes_code_book[2]), self.NA_s)
        self.assertEqual(serialize.serialize_list(['A', 'C', 'T', 'G', 'A'], 3, type_to_bytes_code_book[3]), self.S_s)


    def test_compress(self):
        # compress_data(s_bitstring, time)
        self.assertEqual(compress.compress_bitstring(self.I_s, self.mtime), self.I_c)
        self.assertEqual(compress.compress_bitstring(self.F_s, self.mtime), self.F_c)
        self.assertEqual(compress.compress_bitstring(self.NA_s, self.mtime), self.NA_c)
        self.assertEqual(compress.compress_bitstring(self.S_s, self.mtime), self.S_c)
        self.assertEqual(compress.compress_bitstring(self.IS_s, self.mtime), self.IS_c)

    def test_decompress(self):
        # decompress_data(c_bitstring)
        self.assertEqual(decompress.decompress_data(self.I_c), self.I_dc)
        self.assertEqual(decompress.decompress_data(self.F_c), self.F_dc)
        self.assertEqual(decompress.decompress_data(self.NA_c), self.NA_dc)
        self.assertEqual(decompress.decompress_data(self.S_c), self.S_dc)
        self.assertEqual(decompress.decompress_data(self.IS_c), self.IS_dc)

    def test_deserialize(self):
        # deserialize_data(dc_bitstring, block_size, data_type, num_bytes)
        self.assertEqual(deserialize.deserialize_list(self.I_dc, self.block_size, 1, type_to_bytes_code_book[1]), self.I_ds[0])
        self.assertEqual(deserialize.deserialize_list(self.F_dc, self.block_size, 2, type_to_bytes_code_book[2]), self.F_ds[0])
        self.assertEqual(deserialize.deserialize_list(self.S_dc, self.block_size, 3, type_to_bytes_code_book[3]), self.S_ds[0])


if __name__ == '__main__':
    unittest.main()
