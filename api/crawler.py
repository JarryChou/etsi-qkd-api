"""Class implementing a key file crawler.
"""
import os
import numpy as np


class KeyFileCrawler:
    """
    Class implements a key file crawler that counts the number of keys available stored in qcrypto files. This is a
    helper class for KME.

    Parameters
    ----------
    key_file_path: str
        Absolute file path to directory storing qcrypto key files.
    """

    def __init__(self, key_file_path):
        self.key_file_path = key_file_path

    def get_stored_key_count(self):
        """
        Method that counts the number of keys available from qcrypto files.

        Returns
        -------
        int
            Amount of keys available.

        """
        stored_key_count = 0
        for filename in os.listdir(self.key_file_path):
            file_path = os.path.join(self.key_file_path, filename)
            with open(file_path, 'rb') as f:
                data = np.fromfile(file=f, dtype='<u4')
                stored_key_count += len(data) - 4  # minus 4 due to header information

        return stored_key_count
