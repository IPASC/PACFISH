# BSD 3-Clause License
#
# Copyright (c) 2020, IPASC
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import h5py
from ipasc_tool import PAData
import numpy as np


def write_data(file_path: str, pa_data:PAData, file_compression: str = None):
    """
    Saves a dictionary with arbitrary content or an item of any kind to an hdf5-file with given filepath.

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

    :param file_path: Path of the file to save the dictionary in.
    :param pa_data: PAData instance
    :param file_compression: possible file compression for the hdf5 output file. Values are: gzip, lzf and szip.
    :returns: :mod:`Null`
    """

    def recursively_save_dictionaries(file, path, data_dictionary, compression: str = None):
        """
        Helper function which recursively grabs data from dictionaries in order to store them into hdf5 groups.

        :param file: hdf5 file instance to store the data in.
        :param path: Current group path in hdf5 file group structure.
        :param data_dictionary: Dictionary to save.
        :param compression: possible file compression for the corresponding dataset. Values are: gzip, lzf and szip.
        """

        for key, item in data_dictionary.items():
            key = str(key)
            if not isinstance(item, (list, dict, type(None))):

                if isinstance(item, (bytes, int, np.int64, float, str, bool, np.bool_)):
                    try:
                        h5file[path + key] = item
                    except (OSError, RuntimeError, ValueError):
                        del h5file[path + key]
                        h5file[path + key] = item
                else:
                    c = None
                    if isinstance(item, np.ndarray):
                        c = compression

                    try:
                        h5file.create_dataset(path + key, data=item, compression=c)
                    except (OSError, RuntimeError, ValueError):
                        del h5file[path + key]
                        h5file.create_dataset(path + key, data=item, compression=c)
            elif item is None:
                try:
                    h5file[path + key] = "None"
                except (OSError, RuntimeError, ValueError):
                    del h5file[path + key]
                    h5file[path + key] = "None"
            elif isinstance(item, list):
                list_dict = dict()
                for i, list_item in enumerate(item):
                    list_dict[str(i).zfill(10)] = list_item
                    recursively_save_dictionaries(file, path + key + "/list/", list_dict, file_compression)
            else:
                recursively_save_dictionaries(file, path + key + "/", item, file_compression)

    with h5py.File(file_path, "w") as h5file:
        h5file.create_dataset("binary_time_series_data", data=pa_data.binary_time_series_data)
        recursively_save_dictionaries(h5file, "/meta_data/", pa_data.meta_data_acquisition)
        recursively_save_dictionaries(h5file, "/meta_data_device/", pa_data.meta_data_device)



