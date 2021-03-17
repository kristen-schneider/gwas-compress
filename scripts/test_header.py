# imports
import file_header
import basics
import funnel_format
import serialize
import compress
import decompress
import deserialize
import driver
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
    

    TAB_DELIMETER = '\t'
    COMMA_DELIMETER = ','
    SPACE_DELIMETER = ' '
    
    COL_NAMES = ['chr','pos','ref','alt','af_cases_EUR','af_controls_EUR','beta_EUR','se_EUR','pval_EUR','low_confidence_EUR']
    COL_TYPES = [int, int, str, str, float, float, float, float, float, bool]
    NUM_COLS = 10
    
    TAB_INFO = [TAB_DELIMETER, COL_NAMES, COL_TYPES, len(COL_NAMES)] 
    COMMA_INFO = [COMMA_DELIMETER, COL_NAMES, COL_TYPES, len(COL_NAMES)] 
    SPACE_INFO = [SPACE_DELIMETER, COL_NAMES, COL_TYPES, len(COL_NAMES)] 
   
    def test_get_delimeter(self):
        self.assertEqual(file_header.get_delimeter(self.TAB_ROW1), self.TAB_DELIMETER)    
        self.assertEqual(file_header.get_delimeter(self.COMMA_ROW1), self.COMMA_DELIMETER)    
        self.assertEqual(file_header.get_delimeter(self.SPACE_ROW1), self.SPACE_DELIMETER)    

    def test_get_column_names(self):
        self.assertEqual(file_header.get_column_names(self.TAB_ROW1, self.TAB_DELIMETER), self.COL_NAMES)
        self.assertEqual(file_header.get_column_names(self.COMMA_ROW1, self.COMMA_DELIMETER), self.COL_NAMES)
        self.assertEqual(file_header.get_column_names(self.SPACE_ROW1, self.SPACE_DELIMETER), self.COL_NAMES)
    
    def test_get_column_types(self):
        self.assertEqual(file_header.get_column_types(self.TAB_ROW2, self.TAB_DELIMETER), self.COL_TYPES) 
        self.assertEqual(file_header.get_column_types(self.COMMA_ROW2, self.COMMA_DELIMETER), self.COL_TYPES) 
        self.assertEqual(file_header.get_column_types(self.SPACE_ROW2, self.SPACE_DELIMETER), self.COL_TYPES) 

    def test_get_num_columns(self):
        self.assertEqual(file_header.get_num_columns(self.COL_NAMES, self.COL_TYPES), len(self.COL_NAMES))
        self.assertEqual(file_header.get_num_columns(self.COL_NAMES, self.COL_TYPES), self.NUM_COLS)
        
    def test_get_file_data(self):
        self.assertEqual(file_header.get_file_data(self.TAB_FILE), self.TAB_INFO)
        self.assertEqual(file_header.get_file_data(self.COMMA_FILE), self.COMMA_INFO)
        self.assertEqual(file_header.get_file_data(self.SPACE_FILE), self.SPACE_INFO)
            


if __name__ == '__main__':
    unittest.main()
