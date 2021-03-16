# imports
import file_header
import funnel_format
import serialize
import compress
import decompress
import deserialize
import driver
import unittest
import math

# Testing serialization --> compression --> decompression --> deserialization
class TestSerializationToDeserialization(unittest.TestCase):
    
    num_columns = 5
    mtime = 0   # for reproducibility we choose mtime = 0 for unittests
    int_type = 0
    str_type = 1
    float_type = 2
    num_bytes_int = 5
    num_bytes_str = 5
    num_bytes_float = 8
    
    A = [[1,1,1,1,1]]
    A_s = b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01'
    A_c = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xffc````d\xc0B\x00\x00s \xa8\xa5\x19\x00\x00\x00'
    A_dc = b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01'
    A_ds = [[1,1,1,1,1]]
    
    B = [['A', 'C', 'T', 'G', 'A']]
    B_s = b'ACTGA'
    B_c = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xffst\x0eqw\x04\x00\x9f_F\xff\x05\x00\x00\x00'
    B_dc = b'ACTGA'
    B_ds = [['A', 'C', 'T', 'G', 'A']]

    AB = [[1,1,1,1,1], ['A', 'C', 'T', 'G', 'A']]
    AB_s = b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01ACTGA'
    AB_c = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xffc````d\xc0B8:\x87\xb8;\x02\x00\xca.\x1d\xe5\x1e\x00\x00\x00' 
    AB_dc =  b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01ACTGA'
    AB_ds = [[1,1,1,1,1], ['A', 'C', 'T', 'G', 'A']]
   
    C = [[1.2, 3.45, 67.8, 9.000, 0.12345]]
    #D = scientific notation...    

    def test_serialize(self):
        self.assertEqual(serialize.serialize_data(self.A[0], self.num_bytes_int), self.A_s)
        self.assertEqual(serialize.serialize_list_columns(self.A, [self.num_bytes_int]), self.A_s)
        self.assertEqual(serialize.serialize_data(self.B[0], self.num_bytes_str), self.B_s)
        self.assertEqual(serialize.serialize_list_columns(self.B, [self.num_bytes_str]), self.B_s)
        self.assertEqual(serialize.serialize_list_columns(self.AB, [self.num_bytes_int, self.num_bytes_str]), self.AB_s)

 
    def test_compress(self):        
        self.assertEqual(compress.compress_data(self.A_s, self.mtime), self.A_c)
        self.assertEqual(compress.compress_data(serialize.serialize_data(self.A[0], self.num_bytes_int), self.mtime), self.A_c)
        self.assertEqual(compress.compress_data(self.B_s, self.mtime), self.B_c)
        self.assertEqual(compress.compress_data(serialize.serialize_data(self.B[0], self.num_bytes_str), self.mtime), self.B_c)
        self.assertEqual(compress.compress_data(self.AB_s, self.mtime), self.AB_c)
        self.assertEqual(compress.compress_data(serialize.serialize_list_columns(self.AB, [self.num_bytes_int, self.num_bytes_str]), self.mtime), self.AB_c) 

    def test_decompress(self):
        self.assertEqual(decompress.decompress_data(self.A_c), self.A_dc)
        self.assertEqual(decompress.decompress_data(compress.compress_data(serialize.serialize_data(self.A[0], self.num_bytes_int), self.mtime)), self.A_dc)
        self.assertEqual(decompress.decompress_data(self.B_c), self.B_dc)
        self.assertEqual(decompress.decompress_data(compress.compress_data(serialize.serialize_data(self.B[0], self.num_bytes_str), self.mtime)), self.B_dc)
        self.assertEqual(decompress.decompress_data(self.AB_c), self.AB_dc)
        self.assertEqual(decompress.decompress_data(compress.compress_data(serialize.serialize_list_columns(self.AB, [self.num_bytes_int, self.num_bytes_str]), self.mtime)), self.AB_dc)
         
    def test_deserialize(self):
        # deserialize_data(dc_bitstring, val_type, num_bytes)
        self.assertEqual(deserialize.deserialize_data(self.A_dc, self.int_type, self.num_bytes_int), self.A_ds)
    #    self.assertEqual(deserialize.deserialize_data(decompress.decompress_data(compress.compress_data(serialize.serialize_data(self.A, self.num_bytes_int), self.mtime)), self.int_type, self.num_bytes_int), self.A_ds)
    #    self.assertEqual(deserialize.deserialize_data(self.B_dc, self.str_type, self.num_bytes_str), self.B_ds)
    #    self.assertEqual(deserialize.deserialize_data(decompress.decompress_data(compress.compress_data(serialize.serialize_data(self.B, self.num_bytes_str), self.mtime)), self.str_type, self.num_bytes_str), self.B_ds)
    #    # deserialize_list_bitstrings(dc_bitstring, num_columns, lengths_of_bitstrings, val_types_of_bitstrings, num_bytes_list)
    #    self.assertEqual(deserialize.deserialize_list_bitstrings(self.AB_dc, 2, [len(self.A_dc), len(self.B_dc)], [self.int_type, self.str_type], [self.num_bytes_int, self.num_bytes_str]), self.AB_ds) 


    
if __name__ == '__main__':
    unittest.main()
