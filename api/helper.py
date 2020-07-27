"""Collection of helper functions to handle the logic for the KME.
"""
import base64
import os
import numpy as np


def concat_keys(key_array, size_of_key):
    """ Helper function to concatenate keys.

    Parameters
    ----------
    key_array: array-like
        Array of keys, where each key is in decimal (integer) form.

    size_of_key: int
        How many keys to concatenate together to one key at a time (eg. if 64bit and each key
        is 32bit, then size_of_key=2)

    Returns
    -------
    array
        Array of concatenated keys in integer type. The number of keys will be ``len(key_array)/size_of_key``.

    Notes
    -----
    This function takes in array of keys in their integer representation, and concatenates *consecutive* keys based on
    ``size_of_key``. For example,

    .. highlight:: python
    .. code-block:: python

        >>> arr = [1122334455, 2233445566, 3344556677, 4455667788]
        >>> concat_keys(arr, 2)
        [4820389781632429246, 28729523099122538572]

    Notice that the output array has length ``len(key_array)/size_of_key``. As ``size_of_key`` is 2, keys are grouped
    consecutively into groups of 2 and concatenated. For example, 4820389781632429246 is the integer result of
    concatenating 1122334455 and 2233445566 with the function ``concat_two_int``.
    """

    concatenated_keys = []
    for i, _ in enumerate(key_array):
        if i % size_of_key == 0:
            key1 = key_array[i]
            for j in range(1, size_of_key):
                key2 = key_array[i+j]
                key1 = concat_two_int(key1, key2)
            concatenated_keys.append(key1)

    return concatenated_keys


def retrieve_keys_from_file(num_of_keys_to_retrieve: int, key_file_path: str):
    """ Helper function to retrieve keys from the actual qcrypto binary key files.

    This function will parse the qcrypto binary files appropriately and return the keys in integer representation.
    It will also update the header files appropriately after consuming the keys.
    See: `qcrypto github filespec.txt <https://github.com/kurtsiefer/qcrypto/blob/master/remotecrypto/filespec.txt>`_.

    Parameters
    ----------
    key_file_path: str
        Path to directory containing qcrypto key files.

    num_of_keys_to_retrieve: int
        Total number of keys to retrieve.

    Returns
    -------
    array
        Array of keys in decimal (integer) form.

    """
    keys_retrieved = np.array([])

    while num_of_keys_to_retrieve > 0:

        sorted_key_files = sorted(os.listdir(key_file_path))
        key_file_name = sorted_key_files[0]  # Retrieve first key file in sorted list
        key_file_path = os.path.join(key_file_path, key_file_name)

        with open(key_file_path, 'rb') as f:
            key_file = np.fromfile(file=f, dtype='<u4')
        os.remove(key_file_path)  # Delete the file. Rewrite back modified file later

        header = key_file[:4]  # Header has 4 elements. The rest are key material.
        keys_available = key_file[4:]
        len_of_key_file = len(keys_available)

        if len_of_key_file >= num_of_keys_to_retrieve:  # Sufficient keys in this file alone
            keys_retrieved = np.concatenate([keys_retrieved, keys_available[:num_of_keys_to_retrieve]])
            keys_available = keys_available[num_of_keys_to_retrieve:]  # Remaining keys
            num_of_keys_to_retrieve = 0
            header[3] -= num_of_keys_to_retrieve  # Update header about number of keys in this file left

            # Write updated file back with the same name
            key_file = np.concatenate([header, keys_available])
            key_file.tofile(key_file_path)

        else:
            keys_retrieved = np.concatenate([keys_retrieved, keys_available[:]])
            num_of_keys_to_retrieve -= len_of_key_file

    keys_retrieved = np.array(keys_retrieved, dtype=int)  # Cast type to integer as they tend to become floats
    return keys_retrieved


def int_to_bitstring(x: int) -> str:
    """ Function to convert an integer to AT LEAST a 32-bit binary string.

    For integer less than 32 bits, it will pad the integer with extra bits of 0s until it is of size 32bit.
    If the integer is greater than 32-bits, then return the binary representation with the minimum number of bits to
    represent the integer.

    Parameters
    ----------
    x: int
        Integer to convert to bitstring

    Returns
    -------
    str
        Bitstring of AT LEAST size 32-bits.

    Notes
    -----
    Here are some example cases.

    .. highlight:: python
    .. code-block:: python

        >>> int1 = 2
        >>> int_to_bitstring(int1)
        00000000000000000000000000000010
        >>> int2 = 9999999999999
        >>> int_to_bitstring(int2)
        10010001100001001110011100101001111111111111

    In the first example, the binary representation of 2 is simply 10. Hence, the function pads the bitstring with
    30 0s on the left to return a 32-bit bitstring. In the second example, 9999999999999 in binary consist of > 32-bits,
    hence the function returns the full binary representation.
    """
    return '{:032b}'.format(x)


def bin_to_int(x: str) -> int:
    """ Convert from a binary string to a integer.

    Parameters
    ----------
    x: str
        Binary string to convert.

    Returns
    -------
    int
        Corresponding integer.
    """
    return int(x, 2)


def concat_two_int(int1, int2):
    """ Concatenate two integers `in their 32-bit binary form`.

    Parameters
    ----------
    int1, int2: int
        Two integers to concatenate.

    Returns
    -------
    int
        Concatenated integer.

    Notes
    -----
    For example:
    123 in 32-bit binary is 00000000000000000000000001111011.
    456 in 32-bit binary is 00000000000000000000000111001000.
    The binary concatenated form is
    0000000000000000000000000111101100000000000000000000000111001000,
    which in base 10 is 528280977864.
    """
    int1_bin = int_to_bitstring(int1)
    int2_bin = int_to_bitstring(int2)
    concat = int1_bin + int2_bin
    return bin_to_int(concat)


def int_to_base64(x: int) -> str:
    """ Converts an integer to a base64 string.

    This is helpful in converting the encryption key, often expressed as a large base 10 integer, into base64 as it
    is the format required by the ETSI QKD API.

    Parameters
    ----------
    x: int
        Integer to convert to base 64

    Returns
    -------
    str
        Corresponding string in base64
    """

    base64_byte = base64.b64encode(bitstring_to_bytes(int_to_bitstring(x)))  # returns a byte object encoded in base64
    base64_str = base64_byte.decode()  # convert from byte object to string
    return base64_str


def bitstring_to_bytes(s: str) -> bytes:
    """ Converts a string to a byte object.

    This function is necessary as certain libraries (specifically the base64 library) accepts byte objects, not strings
    which are often expressed in UTF-8 or ASCII formats.

    Parameters
    ----------
    s: str
        String to be converted to bytes object.

    Returns
    -------
    bytes
        Corresponding string in bytes format.
    """
    return int(s, 2).to_bytes((len(s)+7) // 8, byteorder='big')