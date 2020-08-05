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
from ipasc_tool.core.PAData import PAData


def load_data(path: str):
    """
    TODO
    :param path: Path to an hdf5 file containing PAData.
    :return: PAData instance
    """
    pa_data = PAData()

    def recursively_load_dictionaries(file, in_file_path):
        """
        TODO
        :param file: instance of an hdf5 File object
        :param in_file_path: Path inside the file object group structure
        :return: Dictionary instance
        """
        data = {}
        for key, item in h5file[in_file_path].items():
            if isinstance(item, h5py._hl.dataset.Dataset):
                if item[()] is not None:
                    data[key] = item[()]
                else:
                    data[key] = None
            elif isinstance(item, h5py._hl.group.Group):
                if key == "list":
                    data = list()
                    for listkey in sorted(item.keys()):
                        if isinstance(item[listkey], h5py._hl.dataset.Dataset):
                            data.append(item[listkey][()])
                        elif isinstance(item[listkey], h5py._hl.group.Group):
                            data.append(
                                recursively_load_dictionaries(file, path + key + "/" + listkey + "/"))
                else:
                    data[key] = recursively_load_dictionaries(file, path + key + "/")
        return data

    with h5py.File(path, "r") as h5file:
        pa_data.binary_time_series_data = h5file["/binary_time_series_data"][()]
        pa_data.meta_data = recursively_load_dictionaries(h5file, "/meta_data/")
        pa_data.meta_data_device = recursively_load_dictionaries(h5file, "/meta_data_device/")

    return pa_data


def write_data(path: str, pa_data: PAData):
    """
    TODO
    :param path: Path to save an hdf5 file containing PAData.
    :param pa_data: PAData instance
    :return:
    """

    def recursively_save_dictionaries(file, in_file_path, dictionary):
        """
        TODO
        :param file: instance of an hdf5 File object
        :param in_file_path: Path inside the file object group structure
        :param dictionary: Dictionary instance to save
        :return:
        """

        for key, item in dictionary.items():
            if not isinstance(item, (list, dict, type(None))):

                try:
                    h5file[in_file_path + key] = item
                except RuntimeError:
                    del h5file[in_file_path + key]
                    try:
                        h5file[in_file_path + key] = item
                    except RuntimeError as err:
                        try:
                            h5file[in_file_path + key] = item.__dict__
                        except AttributeError:
                            print(item, "of type", type(item), "could not be serialized!")
                            raise err
            elif item is None:
                h5file[path + key] = "None"
            elif isinstance(item, list):
                list_dict = dict()
                for i, list_item in enumerate(item):
                    list_dict[str(i)] = list_item
                recursively_save_dictionaries(file, path + key + "/list/", list_dict)
            else:
                recursively_save_dictionaries(file, path + key + "/", item)

    with h5py.File(path, "w") as h5file:
        h5file.create_dataset("binary_time_series_data", data=pa_data.binary_time_series_data)
        recursively_save_dictionaries(h5file, "/meta_data/", pa_data.meta_data)
        recursively_save_dictionaries(h5file, "/meta_data_device/", pa_data.meta_data_device)
