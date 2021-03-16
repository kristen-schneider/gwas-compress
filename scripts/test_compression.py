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

# Testing funnel format generation (where all incoming files can be split into the same format)
class TestFileHeader(unittest.TestCase):
    HEADER = ['chr','pos','ref','alt','af_cases_EUR','af_controls_EUR','beta_EUR','se_EUR','pval_EUR','low_confidence_EUR']
    TAB_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-tab.tsv'
    DATA = ['1','11063','T','G','4.213e-05','4.799e-05','-1.334e+00','9.999e+00','8.938e-01','true']
    BLOCK_SIZE = 5   
    CRRCT_FILE_HEADER = [10, 5, [], []]
    

    def test_make_file_header(self):
        self.assertEqual(file_header.make_file_header(self.TAB_FILE, self.BLOCK_SIZE), self.CRRCT_FILE_HEADER)
    

class TestFunnelFormat(unittest.TestCase):
    HEADER = ['chr','pos','ref','alt','af_cases_EUR','af_controls_EUR','beta_EUR','se_EUR','pval_EUR','low_confidence_EUR']
    TAB_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-tab.tsv'
    TAB_FILE_75 = '/Users/kristen/Desktop/compression_sandbox/toy_data/75-lines-tab.tsv'
    COMMA_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-comma.csv'
    SPACE_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-space.ssv'
    BLOCK_SIZE = 5
    NUM_LINES_IN_FILE = 9 # not including header
    BLOCK_STRING = '1\t11063\tT\tG\t4.213e-05\t4.799e-05\t-1.334e+00\t9.999e+00\t8.938e-01\ttrue\n1\t13259\tG\tA\t2.984e-05\t2.786e-04\t-1.047e+00\t1.448e+00\t4.699e-01\ttruei\n'
    
    def test_determine_delimeter(self):
        self.assertEqual(funnel_format.determine_delimeter(self.TAB_FILE), '\t')
        self.assertEqual(funnel_format.determine_delimeter(self.COMMA_FILE), ',')
        self.assertEqual(funnel_format.determine_delimeter(self.SPACE_FILE), ' ')

    def test_get_header(self):
        self.assertEqual(type(funnel_format.get_header(self.TAB_FILE, '\t')), list)
        self.assertEqual(funnel_format.get_header(self.TAB_FILE, '\t'), self.HEADER)

    def test_get_chr_format(self):
        self.assertEqual(funnel_format.get_chr_format(self.TAB_FILE, self.HEADER, '\t'), 0) 

    def test_split_into_blocks(self):
        self.assertEqual(len(funnel_format.split_into_blocks(self.TAB_FILE, self.BLOCK_SIZE)), math.ceil(self.NUM_LINES_IN_FILE/self.BLOCK_SIZE))  
    def test_make_one_block(self):
        self.assertEqual(len(funnel_format.make_one_block(self.BLOCK_STRING, len(self.HEADER), self.BLOCK_SIZE, '\t')), len(self.HEADER)) 
    def test_make_all_blocks(self):
        self.assertEqual(len(funnel_format.make_all_blocks(self.TAB_FILE, self.BLOCK_SIZE, len(self.HEADER))), 2)
    
    
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


# Testing driver file which does all the workflow woohoo
#class TestDriver(unittest.TestCase):
#    HEADER = ['chr','pos','ref','alt','af_cases_EUR','af_controls_EUR','beta_EUR','se_EUR','pval_EUR','low_confidence_EUR']
#    TAB_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-tab.tsv'
#    TAB_FILE_75 = '/Users/kristen/Desktop/compression_sandbox/toy_data/75-lines-tab.tsv'
#    COMMA_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-comma.csv'
#    SPACE_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-space.ssv'
#    BLOCK_SIZE = 10

#    def test_write_new_file(self):
#        self.assertEqual(driver.write_new_file(self.TAB_FILE, self.BLOCK_SIZE), 2)
    

    
if __name__ == '__main__':
    unittest.main()
