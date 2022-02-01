"""
SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
SPDX-License-Identifier: CC0
"""
import pacfish as pf
import matplotlib.pyplot as plt
import numpy as np

name = "kwave_2Dsim_random_array_new"
FILE_PATH = f"C:/kWave-PACFISH-export/{name}.hdf5"
# FILE_PATH = "C:/standardised-image-reconstruction/15PPMPX__ZJQLvYSdWe5CxumvueVrizFy_ipasc.hdf5"

pa_data = pf.load_data(FILE_PATH)

pf.quality_check_pa_data(pa_data, verbose=True)

pf.visualize_device(pa_data.meta_data_device, only_show_xz=True, title="2D device visualisation",
                    save_path=f"C:/kWave-PACFISH-export/{name}_device.png")

shape = np.shape(pa_data.binary_time_series_data)
plt.figure(figsize=(4.75, 4))
plt.title("Time Series Data")
plt.imshow(np.squeeze(pa_data.binary_time_series_data).T, aspect=shape[0]/shape[1])
plt.xlabel("Num detector elements")
plt.ylabel("Num time samples")
cb = plt.colorbar()
cb.set_label("Pressure amplitude [a.u.]")
plt.tight_layout()
plt.savefig(f"C:/kWave-PACFISH-export/{name}_ts.png", dpi=300)
