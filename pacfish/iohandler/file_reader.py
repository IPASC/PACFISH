# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-FileCopyrightText: 2021 Computer Assisted Medical Interventions Group, DKFZ
# SPDX-FileCopyrightText: 2021 Janek Gröhl
# SPDX-License-Identifier: BSD 3-Clause License

import h5py
from pacfish import PAData
import numpy as np


def load_data(file_path, file_dictionary_path="/"):
    """

    Loads a dictionary from an hdf5 file.

    The MIT License (MIT)

    Copyright (c) 2021 Computer Assisted Medical Interventions Group, DKFZ
    Copyright (c) 2021 VISION Lab, Cancer Research UK Cambridge Institute (CRUK CI)

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.


    :param file_path: Path of the file to load the dictionary from.
    :param file_dictionary_path: Path in dictionary structure of hdf5 file to lo the dictionary in.
    :returns: Dictionary
    """

    def recursively_load_dictionaries(file, path):
        """
        Helper function which recursively loads data from the hdf5 group structure to a dictionary.

        :param file: hdf5 file instance to load the data from.
        :param path: Current group path in hdf5 file group structure.
        :returns: Dictionary
        """
        dictionary = {}
        for key, item in h5file[path].items():
            if isinstance(item, h5py._hl.dataset.Dataset):
                if item[()] is not None:
                    dictionary[key] = item[()]
                    if isinstance(dictionary[key], bytes):
                        dictionary[key] = dictionary[key].decode("utf-8")
                    elif isinstance(dictionary[key], np.bool_):
                        dictionary[key] = bool(dictionary[key])
                else:
                    dictionary[key] = None
            elif isinstance(item, h5py._hl.group.Group):
                if key == "list":
                    dictionary_list = [None for x in item.keys()]
                    for listkey in sorted(item.keys()):
                        print(listkey)
                        if isinstance(item[listkey], h5py._hl.dataset.Dataset):
                            dictionary_list[int(listkey)] = item[listkey][()]
                        elif isinstance(item[listkey], h5py._hl.group.Group):
                            dictionary_list[int(listkey)] = recursively_load_dictionaries(file, path + key + "/" + listkey + "/")
                    dictionary = dictionary_list
                else:
                    dictionary[key] = recursively_load_dictionaries(file, path + key + "/")
        return dictionary

    with h5py.File(file_path, "r") as h5file:
        binary_data = h5file["/binary_time_series_data"][()]
        pa_data = PAData(binary_data)
        pa_data.meta_data_acquisition = recursively_load_dictionaries(h5file, "/meta_data/")
        pa_data.meta_data_device = recursively_load_dictionaries(h5file, "/meta_data_device/")
        return pa_data
