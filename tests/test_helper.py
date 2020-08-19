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
        self.assertEqual(helper.concat_two_int(123, 456), 528280977864)

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
        assume our test keys are = [[123, 456], [789, 987], [654, 321]], and we want to concat the rows,
        i.e.. 123 with 456, 789 with 987 etc.
        concat_two_int(123,456) == 528280977864
        concat_two_int(789, 987) == 3388729197531
        concat_two_int(654, 321) == 2808908611905
        So we expect concat_keys to return [528280977864, 3388729197531, 2808908611905]
        """
        keys_to_concat = [[123, 456], [789, 987], [654, 321]]
        correct_answer = [528280977864, 3388729197531, 2808908611905]
        self.assertEqual(helper.concat_keys(keys_to_concat), correct_answer)

    def test_int_to_bitstring(self):
        """
        9999999999999 as a bitstring is 10010001100001001110011100101001111111111111
        """
        int_to_convert = 9999999999999
        bitstring = '10010001100001001110011100101001111111111111'
        self.assertEqual(helper.int_to_bitstring(int_to_convert), bitstring)

    def test_bitstring_to_bytes(self):
        """
        '1100100001001' in UTF-8 big-endian encoding is \x19\t.
        """
        bitstring = '1100100001001'
        byte_ans = b'\x19\t'
        self.assertEqual(helper.bitstring_to_bytes(bitstring), byte_ans)

    def test_int_to_bytes(self):
        """
        123456 in UTF-8 big-endian encoding is \x00\x01\xe2@
        """
        int_to_convert = 123456
        byte_ans = b'\x00\x01\xe2@'
        self.assertEqual(helper.int_to_bytes(int_to_convert), byte_ans)

    def test_convert_int_to_uuid(self):
        """
        123456 when used as seed for convert_int_to_uuid returns the uuid 36ad8d7d-040e-9ed2-4eba-167ef2e8cb7e
        """
        int_seed = 123456
        uuid = '36ad8d7d-040e-9ed2-4eba-167ef2e8cb7e'
        self.assertEqual(helper.convert_int_to_uuid(int_seed), uuid)

    def test_flatten_2d_list(self):
        """
        Straightforwardly, [[111, 222], [333, 444], [555, 666, 777]] when flattened is
        [111, 222, 333, 444, 555, 666, 777]
        """
        list_to_flatten = [[111, 222], [333, 444], [555, 666, 777]]
        flattened_list = [111, 222, 333, 444, 555, 666, 777]
        self.assertEqual(helper.flatten_2d_list(list_to_flatten), flattened_list)


if __name__ == "__main__":
    unittest.main()
