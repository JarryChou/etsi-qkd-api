import random
import uuid
import os
import numpy as np
from api import helper


class KME:
    """
    Class for the KME on each node. This class also defines the related methods for manipulating
    the keys.
    """

    source_KME_ID = '10.0.1.30'
    target_KME_ID = '10.0.1.40'
    master_SAE_ID = '10.0.1.10'
    slave_SAE_ID = '10.0.1.20'
    key_size = 32
    max_key_per_request = 10
    max_key_size = 1024
    min_key_size = 32
    max_SAE_ID_count = 0
    status_extension = ''

    def __init__(self, key_file_path: str):
        self.stored_key_count = 0
        self.key_file_path = key_file_path

        for filename in os.listdir(key_file_path):
            file_path = os.path.join(key_file_path, filename)
            with open(file_path, 'rb') as f:
                data = np.fromfile(file=f, dtype='<u4')
                self.stored_key_count += len(data) - 4 # minus 4 due to header information

        self.max_key_count = self.stored_key_count

        self.rd = random.Random()
        self.rd.seed(0) # fix initial seed to be 0 for both master and slave

    def get_key(self, number, size):
        """
        Master function that returns the key container of keys from KME.
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
        :param size: size of each key in bits
        :return:
        """

        number = len(key_ids)

        first_key_ID = key_ids[0]["key_ID"]
        num_keys_concatenated = len(first_key_ID.split("+"))
        size = num_keys_concatenated*self.key_size

        key_container = self.get_key(number, size)

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
        # keys_retrieved will be an array of 32-bit integers
        keys_retrieved = helper.retrieve_keys_from_file(num_of_entries, self.key_file_path)
        self.stored_key_count -= num_of_entries

        # Each key in keys_retrieved is 32bits, so if you want longer keys then pass to
        # helper function to concatenate the keys
        # concatenated_keys will be an array of integers
        concatenated_keys = helper.concat_keys(keys_retrieved, num_of_keys_to_concat)

        # convert each key to base64
        concatenated_keys = [helper.int_to_base64(x) for x in concatenated_keys]

        # create the keys object as per key container specification in API
        keys_array = []
        for key in concatenated_keys:

            key_ID = ""
            for num_key in range(num_of_keys_to_concat):
                key_ID += str(uuid.UUID(int=self.rd.getrandbits(128))) # UUID requires 128 random bits to generate
                if num_key < num_of_keys_to_concat-1: # add a '+' delimiter to link UUIDs of concatenated keys
                    key_ID += "+"

            temp_dict = {"key_ID": key_ID, "key": key}
            keys_array.append(temp_dict)

        # add the size of each key as parameter under 'key_container_extension'
        key_container = {'keys': keys_array}

        return key_container

    def get_status(self):
        """
        Returns status of KME
        :return: dictionary of status properties of KME
        """
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
