# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-FileCopyrightText: 2021 Computer Assisted Medical Interventions Group, DKFZ
# SPDX-FileCopyrightText: 2021 Janek Gröhl
# SPDX-License-Identifier: MIT

import h5py
from pacfish import PAData
import numpy as np


def load_data(file_path:str):
    """
    Loads a PAData instance from an IPASC-formatted HDF5 file.

    Parameters
    ----------
    file_path: str
        Path of the HDF5 file to load the PAData from.

    Return
    ------
    PAData
        PAData instance containing all data and metadata read from the HDF5 file.
    """

    def recursively_load_dictionaries(file, path):
        dictionary = {}
        for key, item in h5file[path].items():
            if isinstance(item, h5py._hl.dataset.Dataset):
                dictionary[key] = None
                if item[()] is not None:
                    dictionary[key] = item[()]
                    if isinstance(dictionary[key], bytes):
                        dictionary[key] = dictionary[key].decode("utf-8")
                        if dictionary[key] == "None":
                            dictionary[key] = None

            elif isinstance(item, h5py._hl.group.Group):
                    dictionary[key] = recursively_load_dictionaries(file, path + key + "/")
        return dictionary

    with h5py.File(file_path, "r") as h5file:
        binary_data = h5file["/binary_time_series_data"][()]
        pa_data = PAData(binary_data)
        pa_data.meta_data_acquisition = recursively_load_dictionaries(h5file, "/meta_data/")
        pa_data.meta_data_device = recursively_load_dictionaries(h5file, "/meta_data_device/")
        return pa_data
