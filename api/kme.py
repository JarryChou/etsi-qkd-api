"""Class implementing the Key Management Entity (KME).
"""
import random
import os
import numpy as np
from api import helper
import configparser
from typing import List


class KME:
    """
    Class for the KME on each node. This class also defines the related methods for manipulating
    the keys. Most of the configurations for the KME, such as the IP address of the web server hosting the API,
    IP address of the SAE etc. is stored in a ``config.ini`` file.

    Parameters
    ----------
    config_path : str
        ABSOLUTE file path to config.ini that is contained in the etsi-qkd-api/api folder.

    Attributes
    ----------
    source_KME_ID: str
        IP address of the source (master) KME.

    target_KME_ID: str
        IP address of the target (slave) KME

    master_SAE_ID: str
        IP address of the master SAE (user application that requests keys)

    slave_SAE_ID: str
        IP address of the slave SAE.

    key_size: int
        Size of each key in bits in the KME.

    max_key_per_request: int
        Maximum number of keys per request

    max_key_size: int
        Maximum size of each key in bits that can be requested.

    min_key_size: int
        Minimum size of each key in bits that can be requested.

    max_SAE_ID_count: int
        Maximum number of additional SAEs allowed (0 at the moment).

    status_extension: str
        Optional field for future use (unclear what it should be used for at the moment)

    rd: random (object, from random Python library)
        Object to initialize random seed and pass to UUID generator to generate UUIDs as the key IDs.
    """

    def __init__(self, config_path: str):

        # read attributes from config file
        config = configparser.ConfigParser()
        config.read(config_path)
        default_section = config['DEFAULT']

        self.key_file_path = default_section.get('key_file_path')

        # read and count keys from qcrypto files available at key_file_path
        self.stored_key_count = 0
        for filename in os.listdir(self.key_file_path):
            file_path = os.path.join(self.key_file_path, filename)
            with open(file_path, 'rb') as f:
                data = np.fromfile(file=f, dtype='<u4')
                self.stored_key_count += len(data) - 4  # minus 4 due to header information

        # class attributes
        self.max_key_count = self.stored_key_count
        self.source_KME_ID = default_section.get('source_KME_ID')
        self.target_KME_ID = default_section.get('target_KME_ID')
        self.master_SAE_ID = default_section.get('master_SAE_ID')
        self.slave_SAE_ID = default_section.get('source_SAE_ID')
        self.key_size = default_section.getint('key_size')
        self.max_key_per_request = default_section.getint('max_key_per_request')
        self.max_key_size = default_section.getint('max_key_size')
        self.min_key_size = default_section.getint('min_key_size')
        self.max_SAE_ID_count = default_section.getint('max_SAE_ID_count')
        self.status_extension = default_section.get('status_extension')

        # set a random seed for generating UUIDs
        self.rd = random.Random()
        self.rd.seed(0)  # fix initial seed to be 0 for both master and slave

    def get_key(self, number: int, size: int) -> dict:
        """Master function that returns the key container of keys from KME.

         Function that handles the logic for retrieving the keys from qcrypto files. If the size of each key
         is a multiple of 32, then the keys need to be concatenated. The file retrieving is done by a helper
         function, :func:`~api.helper.retrieve_keys_from_file`, that actually opens the qcrypto file and retrieves the
         keys.

         Parameters
         ----------
         number : int
             The number of keys requested.
         size : int
             The size of each key in bits.

         Returns
         -------
         dict
             Key container containing the keys requested.

         Raises
         ------
         ValueError
            Error if there are insufficient keys.

         """
        if number is None:
            number = 1

        if size is None:
            size = self.key_size

        num_key_in_each = int(size/self.key_size)

        # If insufficient keys raise ValueError
        if num_key_in_each*number > self.stored_key_count:
            raise ValueError

        # Pass to helper function to retrieve key from the qcrypto binary key files
        keys_retrieved = helper.retrieve_keys_from_file(number, num_key_in_each, self.key_file_path)

        # Each key in keys_retrieved is 32bits, so if you want longer keys then pass to
        # helper function to concatenate the keys
        # concatenated_keys will be an array of integers
        concatenated_keys = helper.concat_keys(keys_retrieved)

        # convert each key to base64
        concatenated_keys = [helper.int_to_base64(x) for x in concatenated_keys]

        # create the keys object as per key container specification in API
        keys_array = []
        for ind, val in enumerate(zip(concatenated_keys, keys_retrieved)):
            concat_key = val[0]
            constituent_keys = val[1]
            list_of_uuids = [helper.convert_int_to_uuid(x) for x in constituent_keys]
            separator = '+'
            key_ID = separator.join(list_of_uuids)  # delimit each key with '+'
            temp_dict = {"key_ID": key_ID, "key": concat_key}
            keys_array.append(temp_dict)

        key_container = {'keys': keys_array}

        self.stored_key_count -= number*num_key_in_each  # update how many keys retrieved from kme

        return key_container

    def get_key_with_id(self, key_ids: List[dict]) -> dict:
        """ Returns the key container of keys from KME given the key IDs.

        Function will be called by the 'slave' application requesting for keys. The actual retrieving of keys
        is passed to the helper function :func:`~api.helper.retrieve_keys_given_uuid`.

        Parameters
        ---------
        key_ids: List[dict]
            Array of dictionaries containing the key ids. Each dictionary contains one key id, in the format:
            { "key_id": <key_id> }

        Returns
        -------
        dict
            Key container containing the keys requested.

        Raises
        ------
        KeyError
            Error if the keys requested cannot be found. Thrown by :func:`~api.helper.retrieve_keys_given_uuid`.
        """

        num_keys_retrieved = 0
        uuid_array = []

        # uuid_array is a 2D list, where each row contains the constituent key IDs (UUIDs) that make up each key
        for val in key_ids:
            concat_key_id = val["key_ID"]
            key_ids_arr = concat_key_id.split("+")  # remember key IDs are concatenated with '+'
            # key_ids_arr = textwrap.wrap(concat_key_id, 36)
            num_keys_retrieved += len(key_ids_arr)
            uuid_array.append(key_ids_arr)

        # pass to helper
        keys_retrieved = helper.retrieve_keys_given_uuid(uuid_array, self.key_file_path)

        # rest of code is similar to retrieve_key_from_file
        concatenated_keys = helper.concat_keys(keys_retrieved)
        concatenated_keys = [helper.int_to_base64(x) for x in concatenated_keys]
        keys_array = []
        for ind, val in enumerate(zip(concatenated_keys, keys_retrieved)):
            concat_key = val[0]
            constituent_keys = val[1]
            list_of_uuids = [helper.convert_int_to_uuid(x) for x in constituent_keys]
            separator = '+'
            key_ID = separator.join(list_of_uuids)  # delimit each key with '+'
            temp_dict = {"key_ID": key_ID, "key": concat_key}
            keys_array.append(temp_dict)

        key_container = {'keys': keys_array}
        self.stored_key_count -= num_keys_retrieved # update how many keys retrieved from kme

        return key_container

    def get_status(self) -> dict:
        """Returns status of KME according to the ETSI specification.

        Returns
        -------
        dict
            Dictionary containing status properties of KME.
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
