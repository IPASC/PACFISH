# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-FileCopyrightText: 2021 Computer Assisted Medical Interventions Group, DKFZ
# SPDX-FileCopyrightText: 2021 Janek Gröhl
# SPDX-License-Identifier: MIT

import h5py
from pacfish import PAData
import numpy as np


def write_data(file_path: str, pa_data: PAData, file_compression: str = None):
    """
    Saves a PAData instance into an HDF5 file according to the IPASC consensus format.

    Parameters
    ----------

    file_path: str
        Path of the file to save the dictionary in.
    pa_data: PAData
        Instance of the PAData class containing all information
    file_compression: str
        possible file compression for the hdf5 output file. Possible values are: gzip, lzf and szip.

    Return
    ------
    None
        This method does not return anything
    """

    def recursively_save_dictionaries(file, path, data_dictionary, compression: str = None):
        for key, item in data_dictionary.items():
            key = str(key)
            if not isinstance(item, (list, dict, type(None))):

                if isinstance(item, (bytes, int, np.int64, float, str, bool, np.bool_)):
                        h5file[path + key] = item
                else:
                    if isinstance(item, np.ndarray):
                        h5file.create_dataset(path + key, data=item, compression=compression)
            elif item is None:
                    h5file[path + key] = "None"
            else:
                recursively_save_dictionaries(file, path + key + "/", item, file_compression)

    with h5py.File(file_path, "w") as h5file:
        h5file.create_dataset("binary_time_series_data", data=pa_data.binary_time_series_data)
        recursively_save_dictionaries(h5file, "/meta_data/", pa_data.meta_data_acquisition)
        recursively_save_dictionaries(h5file, "/meta_data_device/", pa_data.meta_data_device)
