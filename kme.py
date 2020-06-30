import os
import numpy as np
import helper


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
        Master function that returns the key container of keys from master KME.
        :param: number: type STRING. number of keys requested
        :param: size: type STRING. size of key in bits requested
        :return: key container containing the specified keys and key_IDs stored in a dictionary
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


        #
        # keys_array = []
        # index_of_keys_arr = []
        # for dict_iter in key_ids:
        #     key_index = dict_iter["key_ID"]
        #     index_of_keys_arr.append(key_index)
        #     key = self.df['keys'][key_index]
        #     temp_dict = {"key_ID": key_index, "key": key}
        #     keys_array.append(temp_dict)
        #
        # key_container = {"keys": keys_array}
        #
        # # delete keys that were retrieved in slave SAE
        # self.df.drop(index_of_keys_arr, inplace=True)

        return key_container

    def get_multiple_keys(self, number, size):
        """
        Helper function that calculates the logic of how many keys is needed.

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

        # Pass to helper function to retrieve key from the qcrypto binary key files
        keys_retrieved = helper.retrieve_keys_from_file(num_of_entries)
        self.stored_key_count -= num_of_entries

        # Each key in keys_retrieved in 32bits, so if you want longer keys then pass to helper function to
        # concatenate the keys
        key_container = helper.concat_keys(keys_retrieved, num_of_keys_to_concat)

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
