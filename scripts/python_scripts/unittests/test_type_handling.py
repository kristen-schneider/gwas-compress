# imports
import unittest
import type_handling
import numpy as np


# DEFINED (should be same for all files)
type_to_bytes_code_book = {1: 5, 2: 8, 3: 5}
data_type_code_book = {int: 1, float: 2, str: 3}


class TestTypeHandling(unittest.TestCase):    
    # INPUTS FOR TESTING
    I = ['1', '1', '1', '1', '1']
    F = ['4.213e-05', '4.799e-05', '-1.334e+00', '9.999e+00', '8.938e-01']
    S = ['A', 'C', 'T', 'G', 'A']
    F_NA = ['4.213e-05', '4.799e-05', 'NA', 'NA', '8.938e-01']
    first_row = ['1', '11063', 'T', 'G', '4.213e-05', '4.799e-05', '-1.334e+00', '9.999e+00', '8.938e-01', 'true']
    num_rows_in_block = 5 # also, block size
    
    def test_get_data_type(self):
        self.assertEqual(type_handling.get_data_type('1', data_type_code_book), 1)
        self.assertEqual(type_handling.get_data_type('1.', data_type_code_book), 2)
        self.assertEqual(type_handling.get_data_type('1.2e+05', data_type_code_book), 2)
        self.assertEqual(type_handling.get_data_type('true', data_type_code_book), 3)
        self.assertEqual(type_handling.get_data_type('true', data_type_code_book), 3)
        self.assertEqual(type_handling.get_data_type('false', data_type_code_book), 3)
        self.assertEqual(type_handling.get_data_type('false', data_type_code_book), 3)
        self.assertEqual(type_handling.get_data_type('one', data_type_code_book), 3)
        
    def test_get_column_types(self):
        self.assertEqual(type_handling.get_column_types(['1', 'A'], data_type_code_book), \
                                                        [1, 3])
        self.assertEqual(type_handling.get_column_types(self.first_row, data_type_code_book),\
                                                        [1, 1, 3, 3, 2, 2, 2, 2, 2, 3])
        
    def test_convert_to_type(self):
        self.assertEqual(type_handling.convert_to_type(self.I, 1), \
                                                    [1, 1, 1, 1, 1])
        self.assertEqual(type_handling.convert_to_type(self.F, 2), \
                                                    [4.213e-05, 4.799e-05, -1.334e+00, 9.999e+00, 8.938e-01])
        self.assertEqual(type_handling.convert_to_type(self.F_NA, 2), \
                                                    [4.213e-05, 4.799e-05, np.nan, np.nan, 8.938e-01])
        self.assertEqual(type_handling.convert_to_type(self.S, 3), \
                                                    ['A', 'C', 'T', 'G', 'A'])
        
    def test_get_bitstring_length_by_data_type(self):
        self.assertEqual(type_handling.get_bitstring_length_by_data_type(self.num_rows_in_block, 1, type_to_bytes_code_book[1]), 25)
        self.assertEqual(type_handling.get_bitstring_length_by_data_type(self.num_rows_in_block, 2, type_to_bytes_code_book[2]), 40)
        self.assertEqual(type_handling.get_bitstring_length_by_data_type(self.num_rows_in_block, 3, type_to_bytes_code_book[3]), 5)



if __name__ == '__main__':
    unittest.main()
