import unittest
import numpy as np
import serialize
import deserialize


class TestNumpyArrays(unittest.TestCase):
    arr_size = 5
    np_arr = np.ones(arr_size, dtype=np.uint32, order='C')
    s_arr = b'\x00\x00\x00\x00\x01' \
            b'\x00\x00\x00\x00\x01' \
            b'\x00\x00\x00\x00\x01' \
            b'\x00\x00\x00\x00\x01' \
            b'\x00\x00\x00\x00\x01'
    reg_arr = [1,1,1,1,1]

    def test_numpy_serialize(self):
        # serialize_list(data, type, bytes)
        s_np_arr = serialize.serialize_list(self.np_arr, 1, 5)
        self.assertEqual(self.s_arr, s_np_arr)

    def test_numpy_deserialize(self):
        # deserialize_data(bitstring, block_size, data_type, num_bytes, chrm)
        ds_np_arr = deserialize.deserialize_list(self.s_arr, 5, 1, 5, 1)
        self.assertEqual(self.reg_arr, ds_np_arr)

    def test_to_numpy(self):
        # convert a list to a numpy array of proper types
        new_np_arr = np.array(self.reg_arr, dtype=np.uint32, order='C')
        np.testing.assert_array_equal(self.np_arr, new_np_arr)


if __name__ == '__main__':
    unittest.main()
