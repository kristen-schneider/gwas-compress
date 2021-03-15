# imports
import funnel_format
import serialize
import compress
import decompress
import deserialize
import unittest

# Testing funnel format generation (where all incoming files can be split into the same format)
class TestFunnelFormat(unittest.TestCase):
    HEADER = ['chr','pos','ref','alt','af_cases_EUR','af_controls_EUR','beta_EUR','se_EUR','pval_EUR','low_confidence_EUR']
    TAB_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-tab.tsv'
    TAB_FILE_75 = '/Users/kristen/Desktop/compression_sandbox/toy_data/75-lines-tab.tsv'
    COMMA_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-comma.csv'
    SPACE_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-space.ssv'
    BLOCK_SIZE = 5

    def test_determine_delimeter(self):
        self.assertEqual(funnel_format.determine_delimeter(self.TAB_FILE), '\t')
        self.assertEqual(funnel_format.determine_delimeter(self.COMMA_FILE), ',')
        self.assertEqual(funnel_format.determine_delimeter(self.SPACE_FILE), ' ')

    def test_get_header(self):
        self.assertEqual(type(funnel_format.get_header(self.TAB_FILE, '\t')), list)
        self.assertEqual(funnel_format.get_header(self.TAB_FILE, '\t'), self.HEADER)

    def test_get_chr_format(self):
        self.assertEqual(funnel_format.get_chr_format(self.TAB_FILE, self.HEADER, '\t'), 0) 

    def test_make_blocks(self):
        # testing that the make_blocks function returns proper number of blocks
        self.assertEqual(len(funnel_format.make_blocks(self.TAB_FILE, self.BLOCK_SIZE)), 2)
        self.assertEqual(len(funnel_format.make_blocks(self.TAB_FILE_75, self.BLOCK_SIZE)), 15)
        # testing that the make_blocks function makes blocks with proper number of lines
        self.assertEqual(len(funnel_format.make_blocks(self.TAB_FILE, self.BLOCK_SIZE)[0].split('\n')), self.BLOCK_SIZE)
        self.assertEqual(len(funnel_format.make_blocks(self.TAB_FILE_75, self.BLOCK_SIZE)[0].split('\n')), self.BLOCK_SIZE)



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
    
    AB_dc = A_dc+B_dc
    AB_ds = [A, B]
   
    C = [1.2, 3.45, 67.8, 9.000, 0.12345]
    #D = scientific notation...    

    def test_serialize(self):
        self.assertEqual(serialize.serialize_data(self.A, self.num_bytes_int), self.A_s)
        self.assertEqual(serialize.serialize_data(self.B, self.num_bytes_str), self.B_s)
    
    def test_compress(self):
        
        self.assertEqual(compress.compress_data(self.A_s, self.mtime), self.A_c)
        self.assertEqual(compress.compress_data(serialize.serialize_data(self.A, self.num_bytes_int), self.mtime), self.A_c)
        self.assertEqual(compress.compress_data(self.B_s, self.mtime), self.B_c)
        self.assertEqual(compress.compress_data(serialize.serialize_data(self.B, self.num_bytes_str), self.mtime), self.B_c)
    
    def test_decompress(self):
        self.assertEqual(decompress.decompress_data(self.A_c), self.A_dc)
        self.assertEqual(decompress.decompress_data(compress.compress_data(serialize.serialize_data(self.A, self.num_bytes_int), self.mtime)), self.A_dc)
        self.assertEqual(decompress.decompress_data(self.B_c), self.B_dc)
        self.assertEqual(decompress.decompress_data(compress.compress_data(serialize.serialize_data(self.B, self.num_bytes_str), self.mtime)), self.B_dc)
    
    def test_deserialize(self):
        # deserialize_data(dc_bitstring, val_type, num_bytes)
        self.assertEqual(deserialize.deserialize_data(self.A_dc, self.int_type, self.num_bytes_int), self.A_ds)
        self.assertEqual(deserialize.deserialize_data(decompress.decompress_data(compress.compress_data(serialize.serialize_data(self.A, self.num_bytes_int), self.mtime)), self.int_type, self.num_bytes_int), self.A_ds)
        self.assertEqual(deserialize.deserialize_data(self.B_dc, self.str_type, self.num_bytes_str), self.B_ds)
        self.assertEqual(deserialize.deserialize_data(decompress.decompress_data(compress.compress_data(serialize.serialize_data(self.B, self.num_bytes_str), self.mtime)), self.str_type, self.num_bytes_str), self.B_ds)
        # deserialize_list_bitstrings(dc_bitstring, num_columns, lengths_of_bitstrings, val_types_of_bitstrings, num_bytes_list)
        self.assertEqual(deserialize.deserialize_list_bitstrings(self.AB_dc, 2, [len(self.A_dc), len(self.B_dc)], [self.int_type, self.str_type], [self.num_bytes_int, self.num_bytes_str]), self.AB_ds) 

        

    
if __name__ == '__main__':
    unittest.main()
