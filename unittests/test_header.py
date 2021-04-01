# imports
import header_compress
import unittest

# Testing funnel format generation (where all incoming files can be split into the same format)
class TestFileHeader(unittest.TestCase):
    TAB_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-tab.tsv'
    TAB_FILE_75 = '/Users/kristen/Desktop/compression_sandbox/toy_data/75-lines-tab.tsv'
    COMMA_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-comma.csv'
    SPACE_FILE = '/Users/kristen/Desktop/compression_sandbox/toy_data/10-lines-space.ssv'
        
    TAB_ROW1 = 'chr\tpos\tref\talt\taf_cases_EUR\taf_controls_EUR\tbeta_EUR\tse_EUR\tpval_EUR\tlow_confidence_EUR' 
    COMMA_ROW1 = 'chr,pos,ref,alt,af_cases_EUR,af_controls_EUR,beta_EUR,se_EUR,pval_EUR,low_confidence_EUR' 
    SPACE_ROW1 = 'chr pos ref alt af_cases_EUR af_controls_EUR beta_EUR se_EUR pval_EUR low_confidence_EUR' 
    TAB_ROW2 = '1\t13259\tG\tA\t2.984e-05\t2.786e-04\t-1.047e+00\t1.448e+00\t4.699e-01\ttrue'
    COMMA_ROW2 = '1,13259,G,A,2.984e-05,2.786e-04,-1.047e+00,1.448e+00,4.699e-01,true'
    SPACE_ROW2 = '1 13259 G A 2.984e-05 2.786e-04 -1.047e+00 1.448e+00 4.699e-01 true'
    
    MAGIC_NUMBER = 1
    VERSION = 1    

    TAB_DELIMETER = '\t'
    COMMA_DELIMETER = ','
    SPACE_DELIMETER = ' '
    DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3}    

    COL_NAMES = ['chr','pos','ref','alt','af_cases_EUR','af_controls_EUR','beta_EUR','se_EUR','pval_EUR','low_confidence_EUR']
    COL_TYPES = [1, 1, 3, 3, 2, 2, 2, 2, 2, 3]
    NUM_COLS = 10
    
    TAB_HEADER = [[MAGIC_NUMBER, VERSION], [TAB_DELIMETER], COL_NAMES, COL_TYPES, [len(COL_NAMES)]] 
    COMMA_HEADER = [[MAGIC_NUMBER, VERSION], [COMMA_DELIMETER], COL_NAMES, COL_TYPES, [len(COL_NAMES)]] 
    SPACE_HEADER = [[MAGIC_NUMBER, VERSION], [SPACE_DELIMETER], COL_NAMES, COL_TYPES, [len(COL_NAMES)]] 
   
    def test_get_delimeter(self):
        self.assertEqual(header_compress.get_delimeter(self.TAB_ROW1), self.TAB_DELIMETER)
        self.assertEqual(header_compress.get_delimeter(self.COMMA_ROW1), self.COMMA_DELIMETER)
        self.assertEqual(header_compress.get_delimeter(self.SPACE_ROW1), self.SPACE_DELIMETER)

    def test_get_column_names(self):
        self.assertEqual(header_compress.get_column_names(self.TAB_ROW1, self.TAB_DELIMETER), self.COL_NAMES)
        self.assertEqual(header_compress.get_column_names(self.COMMA_ROW1, self.COMMA_DELIMETER), self.COL_NAMES)
        self.assertEqual(header_compress.get_column_names(self.SPACE_ROW1, self.SPACE_DELIMETER), self.COL_NAMES)
    
    def test_get_num_columns(self):
        self.assertEqual(header_compress.get_num_columns(self.COL_NAMES, self.COL_TYPES), len(self.COL_NAMES))
        self.assertEqual(header_compress.get_num_columns(self.COL_NAMES, self.COL_TYPES), self.NUM_COLS)
        
    def test_get_file_data(self):
        self.assertEqual(header_compress.get_file_data(self.TAB_FILE, self.DATA_TYPE_CODE_BOOK), self.TAB_HEADER)
        self.assertEqual(header_compress.get_file_data(self.COMMA_FILE, self.DATA_TYPE_CODE_BOOK), self.COMMA_HEADER)
        self.assertEqual(header_compress.get_file_data(self.SPACE_FILE, self.DATA_TYPE_CODE_BOOK), self.SPACE_HEADER)
            


if __name__ == '__main__':
    unittest.main()
