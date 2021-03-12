# imports
import kristen_format
import unittest
import gzip



# Testing gzip functionality
class TestGZ(unittest.TestCase):
    
    TAB_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-tab.tsv'
    TAB_FILE_75 = '/Users/kristen/Desktop/compression_sandbox/toy_data/75-lines-tab.tsv'
    COMMA_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-comma.csv'
    SPACE_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-space.ssv'
    BLOCK_SIZE = 5
    
    
    def test_data_structures(self):
        blocks = kristen_format.make_blocks(self.TAB_FILE, self.BLOCK_SIZE)
        delimeter = kristen_format.determine_delimeter(self.TAB_FILE)
        header = kristen_format.get_header(self.TAB_FILE, delimeter)
        num_cols = len(header)

        # DS1: list of lists
        self.assertEqual(len(kristen_format.ks_ds_list_of_cols(num_cols, blocks, '\t')), 2)
        self.assertEqual(len(kristen_format.ks_ds_list_of_cols(num_cols, blocks, delimeter)), 2)
        # DS2: dictionary key = col, values = blocks
        self.assertEqual(len(kristen_format.ks_ds_dict_cols_blocks(header, blocks, delimeter)), len(header))
        # DS3: dictionary key = block, values = cols
        self.assertEqual(len(kristen_format.ks_ds_dict_blocks_cols(num_cols, blocks, delimeter)), len(blocks))    
    
if __name__ == '__main__':
    unittest.main()
