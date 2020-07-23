import unittest
import sys
sys.path.append("..")
from api import helper


class BasicHelperTest(unittest.TestCase):

    def test_concat_two_int(self):
        """
        Test concatenation of keys 123 and 456.
        123 in 32-bit binary is 00000000000000000000000001111011.
        456 in 32-bit binary is 00000000000000000000000111001000.
        The binary concatenated form is 0000000000000000000000000111101100000000000000000000000111001000,
        which in base 10 is 528280977864.
        """
        self.assertEqual(helper.concat_two_int(123,456), 528280977864)

    def test_int_to_32_bin(self):
        """
        9999 as a 32 bit binary is 00000000000000000010011100001111
        """
        self.assertEqual(helper.int_to_bitstring(9999), '00000000000000000010011100001111')

    def test_bin_to_int(self):
        self.assertEqual(helper.bin_to_int('00000000000000000010011100001111'), 9999)

    def test_int_to_base64(self):
        """
        9999 when converted to 32-bit binary, then converted to base64 is AAAnDw==
        """
        self.assertEqual(helper.int_to_base64(9999), 'AAAnDw==')

    def test_concat_keys(self):
        """
        assume our test keys are = [123, 456, 789, 987, 654, 321], and we want to concat two keys at a time,
        i.e.. 123 with 456, 789 with 987 etc.
        concat_two_int(123,456) == 528280977864
        concat_two_int(789, 987) == 3388729197531
        concat_two_int(654, 321) == 2808908611905
        So we expect concat_keys to return [528280977864, 3388729197531, 2808908611905]
        """
        keys_to_concat = [123, 456, 789, 987, 654, 321]
        correct_answer = [528280977864, 3388729197531, 2808908611905]
        self.assertEqual(helper.concat_keys(keys_to_concat, 2), correct_answer)


if __name__ == "__main__":
    unittest.main()