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
    
    def test_determine_delimeter(self):
        self.assertEqual(kristen_format.determine_delimeter(self.TAB_FILE), '\t')
        self.assertEqual(kristen_format.determine_delimeter(self.COMMA_FILE), ',')
        self.assertEqual(kristen_format.determine_delimeter(self.SPACE_FILE), ' ')
        
    def test_make_blocks(self):
        # testing that the make_blocks function returns proper number of blocks
        self.assertEqual(len(kristen_format.make_blocks(self.TAB_FILE, self.BLOCK_SIZE)), 2)
        self.assertEqual(len(kristen_format.make_blocks(self.TAB_FILE_75, self.BLOCK_SIZE)), 15)
        # testing that the make_blocks function makes blocks with proper number of lines
        self.assertEqual(len(kristen_format.make_blocks(self.TAB_FILE, self.BLOCK_SIZE)[0].split('\n')), self.BLOCK_SIZE)
        self.assertEqual(len(kristen_format.make_blocks(self.TAB_FILE_75, self.BLOCK_SIZE)[0].split('\n')), self.BLOCK_SIZE)
    
    
if __name__ == '__main__':
    unittest.main()
