import numpy as np
import os
import convert


def concat_keys(key_array, size_of_key):

    # if size_of_key == 1:
    #     concatenated_keys = [convert.int_to_base64(x) for x in key_array]
    # else:
    concatenated_keys = []
    for i in range(len(key_array)):
        if i%size_of_key == 0:
            key1 = key_array[i]
            for j in range(1, size_of_key):
                key2 = key_array[i+j]
                key1 = convert.concat_two_int(key1, key2)
            concatenated_keys.append(convert.int_to_base64(key1))

    keys_array = []
    for key_ID, key in enumerate(concatenated_keys):
        temp_dict = {"key_ID": key_ID, "key": key}
        keys_array.append(temp_dict)

    key_container = {'keys': keys_array}

    return key_container

class kme:
    """
    Class for the KME on each node. This class also defines the related methods for manipulating the keys.
    """

    source_KME_ID = 'a'
    target_KME_ID = 'b'
    master_SAE_ID = 'a'
    slave_SAE_ID = 'b'
    key_size = 32
    max_key_per_request = 128
    max_key_size = 1024
    min_key_size = 32
    max_SAE_ID_count = 0
    status_extension = ''

    def __init__(self):
        self.stored_key_count = 0

        for filename in os.listdir('key_files'):
            file_path = os.path.join('key_files', filename)
            with open(file_path, 'rb') as f:
                data = np.fromfile(file=f, dtype='<u4')
                self.stored_key_count += len(data) - 4 # minus 4 due to header information

        self.max_key_count = self.stored_key_count


    def get_key(self, number, size):
        """
        Returns a single 32-bit key along with the index
        :param: number: type STRING. number of keys requested
        :param: size: type STRING. size of key in bits requested
        :return: key container containing a single key
        """

        if number is None:
            number = 1
        else:
            number = int(number)

        if size is None:
            size = self.key_size
        else:
            size = int(size)

        try:
            key_container = self.get_multiple_keys(number, size)
        except ValueError:
            raise

        return key_container

    def get_key_with_id(self, key_ids):
        """

        :param key_ids: array of dictionaries with key_ids
        :return:
        """

        keys_array = []
        index_of_keys_arr = []
        for dict_iter in key_ids:
            key_index = dict_iter["key_ID"]
            index_of_keys_arr.append(key_index)
            key = self.df['keys'][key_index]
            temp_dict = {"key_ID": key_index, "key": key}
            keys_array.append(temp_dict)

        key_container = {"keys": keys_array}

        # delete keys that were retrieved in slave SAE
        self.df.drop(index_of_keys_arr, inplace=True)

        return key_container

    def get_multiple_keys(self, number, size):
        """
        Retrieves multiple keys of varying sizes

        :param number: number of keys requested
        :param size: size of each key in bits
        :return: dictionary, where key and values are tuples with the key IDs and keys
        """

        # Number of keys you must concatenate to get key of desired size
        num_of_keys_to_concat = int(size/self.key_size)

        # Number of keys to retrieve
        num_of_entries = num_of_keys_to_concat*number

        # If insufficient keys raise ValueError
        if num_of_entries > self.stored_key_count:
            raise ValueError

        self.stored_key_count -= num_of_entries
        keys_retrieved = np.array([])

        while num_of_entries > 0:

            sorted_key_files = sorted(os.listdir('key_files'))
            key_file_name = sorted_key_files[0] # Retrieve first key file in sorted list
            key_file_path = os.path.join('key_files', key_file_name)

            with open(key_file_path, 'rb') as f:
                key_file = np.fromfile(file=f, dtype='<u4')
            os.remove(key_file_path)  # Delete the file. Rewrite back modified file later

            header = key_file[:4]  # Header has 4 elements. The rest are key material.
            keys_available = key_file[4:]
            len_of_key_file = len(keys_available)

            if len_of_key_file >= num_of_entries:  # Sufficient keys in this file alone
                keys_retrieved = np.concatenate([keys_retrieved, keys_available[:num_of_entries]])
                keys_available = keys_available[num_of_entries:]  # Remaining keys
                num_of_entries = 0
                header[3] -= num_of_entries  # Update header about number of keys in this file left

                # Write updated file back with the same name
                key_file = np.concatenate([header, keys_available])
                key_file.tofile(key_file_path)

            else:
                keys_retrieved = np.concatenate([keys_retrieved, keys_available[:]])
                num_of_entries -= len_of_key_file

            keys_retrieved = np.array(keys_retrieved, dtype=int) # Cast type to integer
            key_container = concat_keys(keys_retrieved, num_of_keys_to_concat)
            return key_container

    def get_status(self):

        status = {
            "source_KME_ID": self.source_KME_ID,
            "target_KME_ID": self.target_KME_ID,
            "master_SAE_ID": self.master_SAE_ID,
            "slave_SAE_ID": self.slave_SAE_ID,
            "key_size": self.key_size,
            "stored_key_count": self.stored_key_count,
            "max_key_count": self.max_key_count,
            "max_key_per_request": self.max_key_per_request,
            "max_key_size": self.max_key_size,
            "min_key_size": self.min_key_size,
            "max_SAE_ID_count": self.max_SAE_ID_count
        }

        return status
