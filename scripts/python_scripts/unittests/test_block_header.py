import unittest
import block_header

class TestBlockHeader(unittest.TestCase):
    s_block = b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00+7' \
              b'\x00\x00\x003\xcb\x00\x00\x00D\xe9TGGGAA?\x06\x16\x97\xc7\x06\x8f;>\xffJ\x1d/' \
              b'\x90\xbcP?GZ\x8f\x98\x8e\xd7\x9f?\t)\x1b\xd8"\xc1K?2B!\xe3\x7f\x96\xb9?K=s(' \
              b'\x15\xc8\xbf\xbf\xf5X\x10bM\xd2\xf2\xbf\xf0\xc0\x83\x12n\x97\x8d\xbf\xb9\x1edo' \
              b'\x15a\x91@#\xff|\xed\x91hs?\xf7+\x02\x0cI\xba^?\xean\x97\x8dO\xdf;?\xec\x9a\x02' \
              b'u%F\x0b?\xde\x12\xd7s\x18\xfcP?\xec\xf9\tk\xb9\x8c~truetruetrue'

    block_header_data = [15, 30, 33, 36, 60, 84, 108, 132, 156, 159]
    col0 = [1,1,1]
    col1 = [11063, 13259, 17641]
    col2 = ['T', 'G', 'G']
    col3 = ['G', 'A', 'A']
    col4 = [4.213e-05, 2.984e-05, 0.0007127]
    col5 = [4.799e-05, 0.0002786, 0.0008313]
    col6 = [-1.334, -1.047, -0.09812]
    col7 = [9.999, 1.448, 0.826]
    col8 = [0.8938, 0.4699, 0.9054]
    col9 = ['t', 'r', 'u']



    def test_get_block_header(self):
        self.assertEqual(block_header.get_block_header(
            self.s_block, 3, [1, 1, 3, 3, 2, 2, 2, 2, 2, 3], {1: 5, 2: 8, 3: 5}),
            self.block_header_data)

    def test_deserialize_one_column(self):
        # deserialize_one_column(s_block, block_header, column_i, block_size, data_type, num_bytes)
        self.assertEqual(block_header.deserialize_one_column(self.s_block, self.block_header_data, 0, 3, 1, 5),
                         self.col0)
        self.assertEqual(block_header.deserialize_one_column(self.s_block, self.block_header_data, 1, 3, 1, 5),
                         self.col1)
        self.assertEqual(block_header.deserialize_one_column(self.s_block, self.block_header_data, 2, 3, 3, 5),
                         self.col2)
        self.assertEqual(block_header.deserialize_one_column(self.s_block, self.block_header_data, 3, 3, 3, 5),
                         self.col3)
        self.assertEqual(block_header.deserialize_one_column(self.s_block, self.block_header_data, 4, 3, 2, 8),
                         self.col4)
        self.assertEqual(block_header.deserialize_one_column(self.s_block, self.block_header_data, 5, 3, 2, 8),
                         self.col5)
        self.assertEqual(block_header.deserialize_one_column(self.s_block, self.block_header_data, 6, 3, 2, 8),
                         self.col6)
        self.assertEqual(block_header.deserialize_one_column(self.s_block, self.block_header_data, 7, 3, 2, 8),
                         self.col7)
        self.assertEqual(block_header.deserialize_one_column(self.s_block, self.block_header_data, 8, 3, 2, 8),
                         self.col8)
        self.assertEqual(block_header.deserialize_one_column(self.s_block, self.block_header_data, 9, 3, 3, 5),
                         self.col9)

if __name__ == '__main__':
    unittest.main()