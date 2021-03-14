# imports
import sys
import serialize
import compress
import decompress
import deserialize
import unittest

# Testing serialization --> compression --> decompression --> deserialization
class TestSerializationToDeserialization(unittest.TestCase):
    
    # for reproducibility we choose mtime = 0 for unittests
    mtime = 0
    num_bytes = 5
    
    A = [1,1,1,1,1]
    A_s = b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01'
    A_c = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xffc````d\xc0B\x00\x00s \xa8\xa5\x19\x00\x00\x00'
    A_dc = b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01'
    A_ds = [1,1,1,1,1]
    
    B = ['A', 'C', 'T', 'G', 'A']
    B_s = b'ACTGA'
    B_c = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xffst\x0eqw\x04\x00\x9f_F\xff\x05\x00\x00\x00'
    B_dc = b'ACTGA'
    B_ds = ['A', 'C', 'T', 'G', 'A'] 
    
    #C = [100, 150, 200, 250, 300]
    #D = scientific notation...    

    def test_serialize(self):
        self.assertEqual(serialize.serialize_data(self.A, self.num_bytes), self.A_s)
        self.assertEqual(serialize.serialize_data(self.B, self.num_bytes), self.B_s)
    
    def test_compress(self):
        
        self.assertEqual(compress.compress_data(self.A_s, self.mtime), self.A_c)
        self.assertEqual(compress.compress_data(serialize.serialize_data(self.A, self.num_bytes), self.mtime), self.A_c)
        self.assertEqual(compress.compress_data(self.B_s, self.mtime), self.B_c)
        self.assertEqual(compress.compress_data(serialize.serialize_data(self.B, self.num_bytes), self.mtime), self.B_c)
    
    def test_decompress(self):
        self.assertEqual(decompress.decompress_data(self.A_c), self.A_dc)
        self.assertEqual(decompress.decompress_data(compress.compress_data(serialize.serialize_data(self.A, self.num_bytes), self.mtime)), self.A_dc)
        self.assertEqual(decompress.decompress_data(self.B_c), self.B_dc)
        self.assertEqual(decompress.decompress_data(compress.compress_data(serialize.serialize_data(self.B, self.num_bytes), self.mtime)), self.B_dc)
    
    def test_deserialize(self):
        self.assertEqual(deserialize.deserialize_data(self.A_dc, 0, len(self.A), self.num_bytes), self.A_ds)
        self.assertEqual(deserialize.deserialize_data(decompress.decompress_data(compress.compress_data(serialize.serialize_data(self.A, self.num_bytes), self.mtime)), 0, len(self.A), self.num_bytes), self.A_ds)
        self.assertEqual(deserialize.deserialize_data(self.B_dc, 1, len(self.B), self.num_bytes), self.B_ds)
        self.assertEqual(deserialize.deserialize_data(decompress.decompress_data(compress.compress_data(serialize.serialize_data(self.B, self.num_bytes), self.mtime)), 1, len(self.B), self.num_bytes), self.B_ds)


    
if __name__ == '__main__':
    unittest.main()
