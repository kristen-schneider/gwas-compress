# imports
import basics
import serialize
import compress
import decompress
import deserialize
import unittest

# Testing serialization --> compression --> decompression --> deserialization
class TestSerializationToDeserialization(unittest.TestCase):
    
    #num_columns = 5
    block_size = 5
    mtime = 0   # for reproducibility we choose mtime = 0 for unittests
    int_type = 0
    str_type = 1
    float_type = 2
    type_dict = {int: 5, float: 5, str: 5}
    
    # integer data
    I = [['1','1','1','1','1']]
    I_s = b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01'
    I_c = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xffc````d\xc0B\x00\x00s \xa8\xa5\x19\x00\x00\x00'
    I_dc = b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01'
    I_ds = [[1,1,1,1,1]]
    
    # float data
    F = [['1.2', '3.45', '-6.78e+00', '9.000e-05', '0.1234e+05']]

    # bool data
    B = [['true', 'false', 'false', 'true', 'false']]
 
    # string data
    S = [['A', 'C', 'T', 'G', 'A']]
    S_s = b'ACTGA'
    S_c = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xffst\x0eqw\x04\x00\x9f_F\xff\x05\x00\x00\x00'
    S_dc = b'ACTGA'
    S_ds = [['A', 'C', 'T', 'G', 'A']]
    
    # integer and string data
    IS = [['1','1','1','1','1'], ['A', 'C', 'T', 'G', 'A']]
    IS_s = b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01ACTGA'
    IS_c = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xffc````d\xc0B8:\x87\xb8;\x02\x00\xca.\x1d\xe5\x1e\x00\x00\x00' 
    IS_dc =  b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01ACTGA'
    IS_ds = [[1,1,1,1,1], ['A', 'C', 'T', 'G', 'A']]
   

    def test_basics(self):
        self.assertEqual(basics.get_data_type('1'), int)
        self.assertEqual(basics.get_data_type('1.'), float)
        self.assertEqual(basics.get_data_type('1.2e+05'), float)
        self.assertEqual(basics.get_data_type('one'), str)
        self.assertEqual(basics.get_data_type('true'), bool)
        self.assertEqual(basics.get_data_type('false'), bool)
        self.assertEqual(basics.get_data_type(self.I[0][0]), int)
        self.assertEqual(basics.get_data_type(self.F[0][0]), float)
        self.assertEqual(basics.get_data_type(self.S[0][0]), str)
        self.assertEqual(basics.make_data_types_list(['1', 'A']), [int, str])
        self.assertEqual(basics.make_data_types_list(['1', '11063', 'T', 'G', '4.213e-05', '4.799e-05', '-1.334e+00', '9.999e+00', '8.938e-01', 'true']),\
                                                     [int, int, str, str, float, float, float, float, float, bool])
        self.assertEqual(basics.convert_to_type(self.I[0], int), [1,1,1,1,1])
        self.assertEqual(basics.convert_to_type(self.F[0], float), [1.2, 3.45, -6.78e+00, 9.000e-05, 0.1234e+05])
        self.assertEqual(basics.convert_to_type(self.S[0], str), self.S[0])
        self.assertEqual(basics.get_bitstring_length_by_data_type(5, int, self.type_dict[int]), 25)
        self.assertEqual(basics.get_bitstring_length_by_data_type(5, str, self.type_dict[str]), 5)
          
 
    def test_serialize(self):
        self.assertEqual(serialize.serialize_data([1,1,1,1,1], self.type_dict[int]), self.I_s)
        self.assertEqual(serialize.serialize_data(['A','C','T','G','A'], self.type_dict[str]), self.S_s) 
        self.assertEqual(serialize.serialize_list_columns(self.I, self.type_dict), self.I_s)
        self.assertEqual(serialize.serialize_list_columns(self.S, self.type_dict), self.S_s)
        self.assertEqual(serialize.serialize_list_columns(self.IS, self.type_dict), self.IS_s)
 
    def test_compress(self):        
        self.assertEqual(compress.compress_data(self.I_s, self.mtime), self.I_c)
        self.assertEqual(compress.compress_data(self.S_s, self.mtime), self.S_c)
        self.assertEqual(compress.compress_data(self.IS_s, self.mtime), self.IS_c)

    def test_decompress(self):
        self.assertEqual(decompress.decompress_data(self.I_c), self.I_dc)
        self.assertEqual(decompress.decompress_data(self.S_c), self.S_dc)
        self.assertEqual(decompress.decompress_data(self.IS_c), self.IS_dc)
         
    def test_deserialize(self):
        self.assertEqual(deserialize.deserialize_data(self.I_dc, int, self.type_dict[int]), self.I_ds[0])
        self.assertEqual(deserialize.deserialize_data(self.S_dc, str, self.type_dict[str]), self.S_ds[0])
        self.assertEqual(deserialize.deserialize_block_bitstring(self.I_dc, self.block_size, [int], self.type_dict), self.I_ds)
        self.assertEqual(deserialize.deserialize_block_bitstring(self.S_dc, self.block_size, [str], self.type_dict), self.S_ds)
        self.assertEqual(deserialize.deserialize_block_bitstring(self.IS_dc, self.block_size, [int, str], self.type_dict), self.IS_ds)

    def test_basics_combination(self):    
        self.assertEqual(basics.get_bitstring_length_by_data_type(len(self.I[0]), basics.get_data_type(self.I[0][0]), self.type_dict[int]), len(self.I_s))
        self.assertEqual(basics.get_bitstring_length_by_data_type(len(self.S[0]), basics.get_data_type(self.S[0][0]), self.type_dict[str]), len(self.S_s))
    
    def test_compress_combination(self):
        self.assertEqual(compress.compress_data(serialize.serialize_list_columns(self.I, self.type_dict), self.mtime), self.I_c)
        self.assertEqual(compress.compress_data(serialize.serialize_list_columns(self.S, self.type_dict), self.mtime), self.S_c)
        self.assertEqual(compress.compress_data(serialize.serialize_list_columns(self.IS, self.type_dict), self.mtime), self.IS_c) 
    
    def test_decompress_combinatoin(self):
        self.assertEqual(decompress.decompress_data(compress.compress_data(serialize.serialize_list_columns(self.I, self.type_dict), self.mtime)), self.I_dc)
        self.assertEqual(decompress.decompress_data(compress.compress_data(serialize.serialize_list_columns(self.S, self.type_dict), self.mtime)), self.S_dc)
        self.assertEqual(decompress.decompress_data(compress.compress_data(serialize.serialize_list_columns(self.IS, self.type_dict), self.mtime)), self.IS_dc)
        
    def test_deserialize_combination(self):
        self.assertEqual(deserialize.deserialize_block_bitstring(\
                            decompress.decompress_data(\
                                compress.compress_data(\
                                    serialize.serialize_list_columns(self.I, self.type_dict), \
                                self.mtime)), \
                            self.block_size, [int], self.type_dict), \
                        self.I_ds)
        self.assertEqual(deserialize.deserialize_block_bitstring(\
                            decompress.decompress_data(\
                                compress.compress_data(\
                                    serialize.serialize_list_columns(self.S, self.type_dict), \
                                self.mtime)), \
                            self.block_size, [str], self.type_dict), \
                        self.S_ds)
        self.assertEqual(deserialize.deserialize_block_bitstring(\
                            decompress.decompress_data(\
                                compress.compress_data(\
                                    serialize.serialize_list_columns(self.IS, self.type_dict), \
                                self.mtime)), \
                            self.block_size, [int, str], self.type_dict), \
                        self.IS_ds)

    
if __name__ == '__main__':
    unittest.main()
