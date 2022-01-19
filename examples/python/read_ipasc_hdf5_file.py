"""
SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
SPDX-License-Identifier: CC0
"""
import pacfish as pf

#FILE_PATH = "C:/PACFISH/pacfish_matlab/+pacfish/test.hdf5"
FILE_PATH = "C:/standardised-image-reconstruction/1BdSLl4BSxpxXDwWcBKKVV4nHULPe7IS8_ipasc.hdf5"

pa_data = pf.load_data(FILE_PATH)

pf.visualize_device(pa_data.meta_data_device)
