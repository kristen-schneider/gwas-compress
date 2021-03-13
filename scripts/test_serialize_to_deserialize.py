# imports
import sys
import serialize
import compress
import decompress
import deserialize
import unittest

# Testing serialization --> compression --> decompression --> deserialization
class TestSerializationToDeserialization(unittest.TestCase):

    A = [1,1,1,1,1]
    B = ['A', 'C', 'T', 'G', 'A']
    C = [100, 150, 200, 250, 300]
    #D = scientific notation...    

    def test_serialize(self):
        self.assertEqual(serialize.serialize_data(self.A, 5),
                        b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01')
        self.assertEqual(serialize.serialize_data(self.B, 5), b'ACTGA')
    


    
if __name__ == '__main__':
    unittest.main()
