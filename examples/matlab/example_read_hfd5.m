% SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
% SPDX-License-Identifier: CC0

% read with a given file in Matlab
path = 'C:\kWave-PACFISH-export\';
filename = 'kwave_2Dsim_circular_array_new.hdf5';
file = [path filename];

% Create an instance of the class
% Option A: use the pa_data constructor
padata = pacfish.pa_data(file);

% Option B: load the HDF5 file manually and instantiate pa_data that way
[binary_data, meta_acquisition, meta_device] = pacfish.load_data(file);
padata_2 = pacfish.pa_data(binary_data, meta_acquisition, meta_device);
