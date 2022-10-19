"""
SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
SPDX-License-Identifier: CC0

This example can be used to download and visualise the example data that is provided via Zenodo.
https://doi.org/10.5281/zenodo.5938838
"""

from examples.python.example_utils.download_file import download_file
import pacfish as pf
import numpy as np
import matplotlib.pyplot as plt

# Uncomment only the line of the data set that you want to download and analyse

#data_url = "https://zenodo.org/record/5938838/files/sample_ipasc_kwave_2Dsim_circular_array.hdf5"
data_url = "https://zenodo.org/record/5938838/files/sample_ipasc_kwave_2Dsim_linear_array.hdf5"
#data_url = "https://zenodo.org/record/5938838/files/sample_ipasc_kwave_2Dsim_random_array.hdf5"
#data_url = "https://zenodo.org/record/5938838/files/sample_ipasc_kwave_2Dsim_semicircular_array.hdf5"

# Downloading file
filename = download_file(data_url)

# Loading file from disk as a pa_data instance
pa_data = pf.load_data(filename)

# perform completeness and consistency checking on the pa_data
pf.quality_check_pa_data(pa_data, verbose=True)

# Visualising the device metadata
pf.visualize_device(pa_data.meta_data_device, only_show_xz=False, title="2D device visualisation", show_legend=True,
                    save_path="figure.svg")

# Visualising the time series data
shape = np.shape(pa_data.binary_time_series_data)
plt.figure(figsize=(4.75, 4))
plt.title("Time Series Data")
plt.imshow(np.squeeze(pa_data.binary_time_series_data).T, aspect=shape[0]/shape[1])
plt.xlabel("Num detector elements")
plt.ylabel("Num time samples")
cb = plt.colorbar()
cb.set_label("Pressure amplitude [a.u.]")
plt.tight_layout()
plt.show()
