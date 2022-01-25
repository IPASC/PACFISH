"""
SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
SPDX-License-Identifier: CC0
"""
import pacfish as pf
import numpy as np

from testing.unit_tests.utils import assert_equal_dicts

FILE_PATH_MATLAB_WRITTEN_FILE = "C:/PACFISH/pacfish_matlab/+pacfish/test.hdf5"
FILE_PATH_PYTHON_WRITTEN_FILE = "C:/standardised-image-reconstruction/1BdSLl4BSxpxXDwWcBKKVV4nHULPe7IS8_ipasc.hdf5"

pa_data = pf.load_data(FILE_PATH_MATLAB_WRITTEN_FILE)
pa_data_2 = pf.load_data(FILE_PATH_PYTHON_WRITTEN_FILE)

pf.visualize_device(pa_data.meta_data_device)
pf.visualize_device(pa_data_2.meta_data_device)

# Testing if the two read files are actually the same
assert np.equal(pa_data.binary_time_series_data, pa_data_2.binary_time_series_data).all()
assert_equal_dicts(pa_data.meta_data_acquisition, pa_data_2.meta_data_acquisition)
assert_equal_dicts(pa_data.meta_data_device, pa_data_2.meta_data_device)
