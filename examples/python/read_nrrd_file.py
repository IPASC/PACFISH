"""
SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
SPDX-License-Identifier: CC0
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from testing.adapters.utils import create_nrrd_file
from pacfish.api.adapters.Nrrd_File_Converter import NrrdFileConverter
from pacfish import write_data
from pacfish import quality_check_pa_data
from pacfish.visualize_device import visualize_device

if not os.path.exists('demodata.nrrd'):
    create_nrrd_file('demodata.nrrd')

converter = NrrdFileConverter('demodata.nrrd')

pa_data = converter.generate_pa_data()

quality_check_pa_data(pa_data, verbose=True, log_file_path="")

write_data("demodata_ipasc.hdf5", pa_data)

binary = np.rot90(pa_data.binary_time_series_data[:, 500:-2500, 0, 0], -1)
binary = binary - np.min(binary) + 1
binary = np.log10(binary)
plt.imshow(binary, aspect=0.08, vmin=np.percentile(binary, 1), vmax=np.percentile(binary, 99))
plt.show()
plt.close()

visualize_device(pa_data.meta_data_device, title="Custom device visualisation based on IPASC data format specifications")

if os.path.exists("logfile.md"):
    os.remove("logfile.md")
if os.path.exists("demodata.nrrd"):
    os.remove("demodata.nrrd")
if os.path.exists("demodata_ipasc.hdf5"):
    os.remove("demodata_ipasc.hdf5")
