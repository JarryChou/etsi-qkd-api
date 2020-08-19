import unittest
import sys
sys.path.append("..")
from api import KME
from unittest.mock import patch


class BasicKmeTest(unittest.TestCase):

    def setUp(self):

        # since we use mocks no actual keying material will be consumed, but still provide a valid path
        # to config.ini for the constructor to not return an error of invalid path
        self.kme = KME('../api/config.ini')

    def test_get_status(self):

        status = self.kme.get_status()
        self.assertEqual(len(status), 11)

    @patch('api.helper.retrieve_keys_from_file')
    def test_get_one_32_bit_key(self, mock_retrieve_key_function):

        size = self.kme.key_size
        number = 1

        # mock the retrieve key function to return one key of type int == 123456
        # prevents the use of actual keying material for tests
        mock_retrieve_key_function.return_value = [[123456]]

        key_container = self.kme.get_key(number, size)
        self.assertEqual(len(key_container["keys"]), 1)
        self.assertTrue("key" in key_container["keys"][0])
        self.assertTrue("key_ID" in key_container["keys"][0])

    @patch('api.helper.retrieve_keys_from_file')
    def test_get_multiple_32_bit_keys(self, mock_retrieve_key_function):
        size = self.kme.key_size
        number = 4

        # assume each of the 6-digit integers are 32-bit keys
        mock_retrieve_key_function.return_value = [[123456], [234567], [345678], [456789]]

        key_container = self.kme.get_key(number, size)
        self.assertEqual(len(key_container["keys"]), 4)

    @patch('api.helper.retrieve_keys_from_file')
    def test_get_one_128_bit_keys(self, mock_retrieve_key_function):
        size = self.kme.key_size*4  # 128-bit key
        number = 3

        # one row of 4*32=128-bit key
        mock_retrieve_key_function.return_value = [[123456, 234567, 345678, 456789]]

        key_container = self.kme.get_key(number, size)
        self.assertEqual(len(key_container["keys"]), 1)

        # key_ID are concatenated with a "+" delimiter between the individual key UUIDs
        key_ID = key_container["keys"][0]["key_ID"]
        key_ID_split = key_ID.split("+")
        self.assertEqual(len(key_ID_split), 4)  # check that UUID indeed consists of 4 separate UUIDs

    @patch('api.helper.retrieve_keys_from_file')
    def test_get_multiple_128_bit_keys(self, mock_retrieve_key_function):
        size = self.kme.key_size*4  # 128-bit key
        number = 3

        # assume each row contains 4*32=128-bit keys, and there are 3 rows, therefore 3*128-bit keys
        mock_retrieve_key_function.return_value = [[123456, 234567, 345678, 456789],
                                                   [112233, 223344, 334455, 445566],
                                                   [778899, 889900, 990011, 123456]]

        key_container = self.kme.get_key(number, size)
        self.assertEqual(len(key_container["keys"]), 3)

        keys = key_container["keys"]
        for i, _ in enumerate(keys):  # loop over each key and check that each is made of 4 separate UUIDs
            key_ID = keys[i]["key_ID"]
            key_ID_split = key_ID.split("+")
            self.assertEqual(len(key_ID_split), 4)


if __name__ == "__main__":
    unittest.main()