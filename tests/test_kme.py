import unittest
import sys
sys.path.append("..")
from project import KME


class BasicKmeTest(unittest.TestCase):

    def setUp(self):
        self.kme = KME('../key_files')

    def test_get_status(self):
        status = self.kme.get_status()
        self.assertEqual(len(status), 11)

    def test_get_one_key(self):
        size = self.kme.key_size
        number = 1
        key_container = self.kme.get_key(number, size)
        self.assertEqual(len(key_container["keys"]), 1)
        self.assertTrue("key" in key_container["keys"][0])
        self.assertTrue("key_ID" in key_container["keys"][0])

    def test_get_multiple_keys(self):
        size = self.kme.key_size
        number = 5
        key_container = self.kme.get_key(number, size)
        self.assertEqual(len(key_container["keys"]), 5)

    def test_get_concat_key(self):
        size = self.kme.key_size * 3
        number = 1
        key_container = self.kme.get_key(number, size)
        self.assertEqual(len(key_container["keys"]), 1)

        # key_ID are concatenated with a "+" delimiter between the indiviudal key UUIDs
        key_ID = key_container["keys"][0]["key_ID"]
        key_ID_split = key_ID.split("+")
        self.assertEqual(len(key_ID_split), 3)


if __name__ == "__main__":
    unittest.main()