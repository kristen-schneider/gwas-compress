# imports
import sys
import serialize
import unittest

# Testing serialization
class TestSerialization(unittest.TestCase):

    A = [1,1,1,1,1]
    B = ['A', 'C', 'T', 'G', 'A']
    C = [100, 150, 200, 250, 300]
    #D = scientific notation...    

    def test_serialize(self):
        self.assertEqual(serialize.serialize_data(self.A, sys.getsizeof(int())), b'\x01\x01\x01\x01\x01')
        self.assertEqual(serialize.serialize_data(self.B, sys.getsizeof(str())), b'ACTGA')
        #self.assertEqual(serialization.serialize(C, sys.getsizeof(int)), b'')

if __name__ == '__main__':
    unittest.main()
