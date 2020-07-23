import unittest
import sys
sys.path.append("..")
from api import KME
from unittest.mock import patch


class BasicKmeTest(unittest.TestCase):

    def setUp(self):
        # since we use mocks no actual keying material will be consumed, but still provide a valid path
        # for the constructor to not return an error of invalid path
        self.kme = KME('../key_files')

    def test_get_status(self):
        status = self.kme.get_status()
        self.assertEqual(len(status), 11)

    @patch('api.helper.retrieve_keys_from_file')
    def test_get_one_key(self, mock_retrieve_key_function):
        size = self.kme.key_size
        number = 1

        # mock the retrieve key function to return one key of type int == 123456
        # prevents the use of actual keying material for tests
        mock_retrieve_key_function.return_value = [123456]

        key_container = self.kme.get_key(number, size)
        self.assertEqual(len(key_container["keys"]), 1)
        self.assertTrue("key" in key_container["keys"][0])
        self.assertTrue("key_ID" in key_container["keys"][0])

    @patch('api.helper.retrieve_keys_from_file')
    def test_get_multiple_keys(self, mock_retrieve_key_function):
        size = self.kme.key_size
        number = 3

        mock_retrieve_key_function.return_value = [123456, 234567, 345678]

        key_container = self.kme.get_key(number, size)
        self.assertEqual(len(key_container["keys"]), 3)

    @patch('api.helper.retrieve_keys_from_file')
    def test_get_concat_key(self, mock_retrieve_key_function):
        size = self.kme.key_size*3
        number = 1

        # need to return 3 keys to concatenate
        mock_retrieve_key_function.return_value = [123456, 234567, 345678]

        key_container = self.kme.get_key(number, size)
        self.assertEqual(len(key_container["keys"]), 1)

        # key_ID are concatenated with a "+" delimiter between the indiviudal key UUIDs
        key_ID = key_container["keys"][0]["key_ID"]
        key_ID_split = key_ID.split("+")
        self.assertEqual(len(key_ID_split), 3)


if __name__ == "__main__":
    unittest.main()