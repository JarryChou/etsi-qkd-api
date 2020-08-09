"""Collection of helper functions to handle the logic for the KME.
"""
import base64
import os
import numpy as np
from typing import List
from hashlib import shake_128
import uuid


def concat_keys(key_array: List[List[int]]) -> List[int]:
    """ Helper function to concatenate keys.

    The function will concatenate integers in the same row of the 2D list ``key_array`` using :func:`~api.helper.concat_two_int`.

    Parameters
    ----------
    key_array: 2D list
        2D list of keys. Each row are the integers to be concatenated.

    Returns
    -------
    list
        List of concatenated keys in integer type. The number of keys will be ``len(key_array)`` (number of rows).

    Notes
    -----
    This function takes in a 2D array of keys in their integer form, and concatenates keys in the same row.

    .. highlight:: python
    .. code-block:: python

        >>> arr = [[1122334455, 2233445566], [3344556677, 4455667788]]
        >>> concat_keys(arr)
        [4820389781632429246, 28729523099122538572]

    Here, 4820389781632429246 is the integer result of concatenating 1122334455 and 2233445566 with the function
    :func:`~api.helper.concat_two_int`. Similarly 28729523099122538572 is the result of concatenating 3344556677 and 4455667788.
    """

    concatenated_keys = []
    for row in key_array:
        key1 = row[0]
        for _, key2 in enumerate(row[1:]):
            key1 = concat_two_int(key1, key2)
        concatenated_keys.append(key1)

    return concatenated_keys


def retrieve_keys_from_file(number: int, num_key_in_each: int, key_file_path: str) -> List[List[int]]:
    """ Helper function to retrieve keys from the actual qcrypto binary key files.

    This function will parse the qcrypto binary files appropriately and return the keys in integer representation.
    It will also update the header files appropriately after consuming the keys.
    See: `qcrypto github filespec.txt <https://github.com/kurtsiefer/qcrypto/blob/master/remotecrypto/filespec.txt>`_.

    Parameters
    ----------
    key_file_path: str
        Path to directory containing qcrypto key files.

    number: int
        Number of keys requested

    num_key_in_each: int
        How many 32bit keys each key is made of.

    Returns
    -------
    2D list
        List of keys in decimal (integer) form. Each row represents one key and has ``num_key_in_each`` integers,
        and there are ``number`` rows.

    """
    keys_retrieved = np.array([], dtype=int)
    tot_keys_to_retrieve = number * num_key_in_each

    while tot_keys_to_retrieve > 0:

        sorted_key_files = sorted(os.listdir(key_file_path))
        key_file_name = sorted_key_files[0]  # Retrieve first key file in sorted list
        _key_file_path = os.path.join(key_file_path, key_file_name)

        with open(_key_file_path, 'rb') as f:
            key_file = np.fromfile(file=f, dtype='<u4')
        os.remove(_key_file_path)  # Delete the file. Rewrite back modified file later

        header = key_file[:4]  # Header has 4 elements. The rest are key material.
        keys_available = key_file[4:]
        len_of_key_file = len(keys_available)

        if len_of_key_file >= tot_keys_to_retrieve:  # Sufficient keys in this file alone
            keys_retrieved = np.concatenate([keys_retrieved, keys_available[:tot_keys_to_retrieve]])
            keys_available = keys_available[tot_keys_to_retrieve:]  # Remaining keys
            header[3] -= tot_keys_to_retrieve  # Update header about number of keys in this file left
            tot_keys_to_retrieve = 0

            # Write updated file back with the same name
            key_file = np.concatenate([header, keys_available])
            key_file.tofile(_key_file_path)

        else:
            keys_retrieved = np.concatenate([keys_retrieved, keys_available[:]])
            tot_keys_to_retrieve -= len_of_key_file

    keys_retrieved = keys_retrieved.reshape(number, num_key_in_each)  # reshape to 2D array  # return as list
    return keys_retrieved.tolist()  # return as list


def retrieve_keys_given_uuid(uuid_array: List[List[str]], key_file_path: str) -> List[List[int]]:
    """ Helper function to retrieve keys given the UUIDs of the keys.

    This function

    Parameters
    ----------
    uuid_array: 2D list
        2D list of strings. Each row represents a single key, and the elements in the row are UUIDs of the individual
        keys that concatenate to make the full key.

    key_file_path: str
        Path to directory containing qcrypto key files.

    Returns
    -------
    2D list
        List of keys in decimal (integer) form. Each row represents a single key, and each element in a row is the
        actual key that will be eventually concatenated to form the final key.

    """

    uuid_array = np.array(uuid_array, dtype=str)  # convert to numpy array for easier manipulation
    keys_retrieved = np.zeros_like(uuid_array, dtype=int)
    sorted_key_files = sorted(os.listdir(key_file_path))

    for key_file_name in sorted_key_files:

        _key_file_path = os.path.join(key_file_path, key_file_name)

        with open(_key_file_path, 'rb') as f:
            key_file = np.fromfile(file=f, dtype='<u4')
        os.remove(_key_file_path)

        header = key_file[:4]
        keys_available = key_file[4:]

        keys_to_remove = []  # store index of keys to remove if found to have matching UUIDS
        count = 0  # count how many keys are being removed this file
        for index, key in enumerate(keys_available):  # iterate over every key in the key file
            uuid_ = convert_int_to_uuid(key)  # convert each key to UUID
            if uuid_ in uuid_array:  # if the UUID matches

                item_index = np.where(uuid_array == uuid_)
                row, col = item_index[0][0], item_index[1][0]  # get the index of the first occurrence, incase of repeat

                count += 1
                keys_retrieved[row][col] = key
                keys_to_remove.append(index)
                uuid_array[row][col] = '0'  # 0 to signify it has been retrieved

            if np.all(uuid_array == '0'):  # if uuid_array is all 0, stop searching as you have found all keys
                break

        keys_available = np.delete(keys_available, keys_to_remove)
        header[3] -= count
        key_file = np.concatenate([header, keys_available])
        key_file.tofile(_key_file_path)

        if np.all(uuid_array == '0'):
            return keys_retrieved.tolist()

    raise KeyError  # if it hasn't returned after looping over all key files, then the key(s) cant be found


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


def concat_two_int(int1: int, int2: int) -> int:
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


def int_to_bytes(x: int) -> bytes:
    """ Converts an integer to a byte object

    Parameter
    ---------
    x: int
        Integer to be converted.

    Returns
    -------
    bytes
        Corresponding integer in bytes format.
    """
    binary = int_to_bitstring(x)
    bytes_ = bitstring_to_bytes(binary)
    return bytes_


def convert_int_to_uuid(x: int) -> str:
    """Uses an integer as a seed to generate a UUID.

    This function first hashes the integer using the  `hashlib.shake_128 <https://docs.python.org/3/library/hashlib.html#shake-variable-length-digests>`_
    hashing algorithm. This allows us to generate a 128bit hash that the `uuid <https://docs.python.org/3/library/uuid.html>`_
    library requires as seed to generate a unique UUID.

    Parameters
    ----------
    x: int
        Integer as seed.

    Returns
    -------
    str
        UUID in string format.
    """
    x_byte = int_to_bytes(x)
    m = shake_128()
    m.update(x_byte)
    digest = m.digest(16)
    u = str(uuid.UUID(bytes=digest))
    return u


def flatten_2d_list(l: List[List]) -> List:
    """ Flattens a 2D list into a 1D list.

    Parameters
    ----------
    l: 2D list
        2D list to flatten

    Returns
    -------
    1D list
        Flattened list.
    """
    return [item for sublist in l for item in sublist]

