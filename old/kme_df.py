import numpy as np
import pandas as pd
import os
from baseconv import base64


def read_keys_from_file():
    """
    Reads keys from the provided final key file with format as specified by qcrypto/remotecrypto/filespec.txt
    point 5.

    :return: Pandas dataframe containing a single column 'keys', indexed from 0.
    """

    key_array = []

    for filename in os.listdir('../key_files'):
        file_path = os.path.join('key_files', filename)
        with open(file_path, 'rb') as f:
            data = np.fromfile(file=f, dtype='<u4')
            for index, val in enumerate(data):
                if index > 3:
                    # key_array.append('{0:032b}'.format(val))
                    key_array.append(base64.encode(val))

    df = pd.DataFrame(key_array, columns=['keys'])
    return df


class kme:
    """
    Class for the KME on each node. The keys are stored in a  a Pandas dataframe. This class also defines the related
    methods for manipulating the keys.
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
        self.df = read_keys_from_file()
        self.stored_key_count = len(self.df)
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

        # Number of entries in dataframe to grab
        num_of_entries = num_of_keys_to_concat*number

        try:
            # random_state takes in a RandomState object as seed. this gives it a seed according to current time.
            index_of_keys_arr = self.df['keys'].sample(n=num_of_entries, random_state=np.random.RandomState()).index
        except ValueError:
            raise

        keys_array = []
        for index in index_of_keys_arr:
            key = self.df['keys'][index]
            temp_dict = {"key_ID": index, "key": key}
            keys_array.append(temp_dict)

        key_container = {"keys": keys_array}

        # delete the keys that were retrieved in master SAE
        self.df.drop(index_of_keys_arr, inplace=True)

        # #dict_of_keys has key_ID in tuple form (for multiple keys), and corresponding keys in tuple form
        # dict_of_keys = {}
        #
        # for i in range(len(index_of_entries)):
        #     if i % num_of_keys_to_concat == 0:
        #         temp_arr_to_make_id_tuple = []
        #         temp_arr_to_make_key_tuple = []
        #         for j in range(num_of_keys_to_concat):
        #             ind = i+j
        #             temp_arr_to_make_id_tuple.append(index_of_entries[ind])
        #             temp_arr_to_make_key_tuple.append(self.df['keys'][ind])
        #     dict_of_keys[list(temp_arr_to_make_id_tuple)] = temp_arr_to_make_key_tuple
        #
        # #---------IMPLEMENT DELETE KEYS FROM DATAFRAME BEFORE RETURNING-----------

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
