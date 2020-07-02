import base64
import os
import numpy as np


def concat_keys(key_array, size_of_key):
    """
    Helper function to concatenate keys.
    :param key_array: array of keys in decimal (int) form
    :param size_of_key: how many keys to concatenate together (eg. if 64bit, then size_of_key=2)
    :return: Array of concatenated keys in int type.
    """
    concatenated_keys = []
    for i in range(len(key_array)):
        if i % size_of_key == 0:
            key1 = key_array[i]
            for j in range(1, size_of_key):
                key2 = key_array[i+j]
                key_concat = concat_two_int(key1, key2)
            concatenated_keys.append(key_concat)

    return concatenated_keys


def retrieve_keys_from_file(num_of_keys_to_retrieve):
    """
    Helper function to retrieve keys from the actual qcrypto binary key files.
    :param num_of_keys_to_retrieve: total number of keys to retrieve
    :return: array of keys in decimal (int) form.
    """
    keys_retrieved = np.array([])

    while num_of_keys_to_retrieve > 0:

        sorted_key_files = sorted(os.listdir('key_files'))
        key_file_name = sorted_key_files[0]  # Retrieve first key file in sorted list
        key_file_path = os.path.join('key_files', key_file_name)

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


def int_to_32_bin(x: int) -> str:
    return '{:032b}'.format(x)


def bin_to_int(x: str) -> int:
    return int(x, 2)


def concat_two_int(x: int, y: int) -> int:
    x_bin = int_to_32_bin(x)
    y_bin = int_to_32_bin(y)
    concat = x_bin + y_bin
    return bin_to_int(concat)


def int_to_base64(x: int) -> str:
    base64_byte = base64.b64encode(str(x).encode('ascii'))  # byte object
    base64_str = base64_byte.decode('utf-8')  # convert from byte object to string
    return base64_str
