# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-FileCopyrightText: 2021 Computer Assisted Medical Interventions Group, DKFZ
# SPDX-FileCopyrightText: 2021 Janek Gröhl
# SPDX-License-Identifier: MIT

import h5py
from pacfish import PAData
from pacfish.core.Metadata import MetadataAcquisitionTags as Tags
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

                    # This is introduced to ensure compatibility with the MATLAB code...
                    if isinstance(dictionary[key], np.ndarray):
                        # remove any singleton dimensions
                        dictionary[key] = np.squeeze(dictionary[key])

                    if isinstance(dictionary[key], np.object_):
                        dictionary[key] = dictionary[key].astype(np.str_)
                        dictionary[key] = str(dictionary[key])

                    # H5PY loads datasets into numpy types by default. However, that is not how they were defined
                    # before writing, so the following two lines convert to the closest built-in type - if possible.
                    if isinstance(dictionary[key], np.generic):
                        dictionary[key] = dictionary[key].item()

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

        # Check for the file version to ensure backwards compatibility of the data format.
        if ((Tags.VERSION.tag not in pa_data.meta_data_acquisition) or
            (pa_data.meta_data_acquisition[Tags.VERSION.tag] == "V1")):
            print("INFO: Importing IPASC V1 data file.")

            if len(np.shape(pa_data.binary_time_series_data)) < 4:
                # Even though the data is labelled as being V1, it did only contain one (wavelength/measurement) field.
                # In this case, we can simply take the data as is and save it into V2.
                if len(np.shape(pa_data.binary_time_series_data)) == 3:
                    pa_data.binary_time_series_data = pa_data.binary_time_series_data[:, :, :, np.newaxis]
                elif len(np.shape(pa_data.binary_time_series_data)) == 2:
                    pa_data.binary_time_series_data = pa_data.binary_time_series_data[:, :, np.newaxis, np.newaxis]
                else:
                    raise AssertionError("The binary time series data was not compatible with the IPASC standard.")

            # we're in version 1, so we ned to reshape the wavelengths and measurements into the same dimension and
            # expand the wavelengths field to be as long as the number of measurements.
            (n_detectors, n_timesteps, n_wavelengths, n_measurements) = np.shape(pa_data.binary_time_series_data)
            pa_data.binary_time_series_data = pa_data.binary_time_series_data.reshape((n_detectors, n_timesteps,
                                                                                       n_wavelengths * n_measurements))

            if len(pa_data.get_acquisition_wavelengths().shape) == 0:
                wavelengths = [pa_data.get_acquisition_wavelengths().item()]
            else:
                wavelengths = list(pa_data.get_acquisition_wavelengths())

            wavelengths = wavelengths * n_measurements

            pa_data.meta_data_acquisition[Tags.ACQUISITION_WAVELENGTHS.tag] = np.asarray(wavelengths).reshape((-1, ))

        return pa_data
