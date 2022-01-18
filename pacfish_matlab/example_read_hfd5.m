% read with a given file in Matlab
path = 'C:\standardised-image-reconstruction\';
filename = '1BdSLl4BSxpxXDwWcBKKVV4nHULPe7IS8_ipasc.hdf5';
file = [path filename];

% Create an instance of the class
% Option A: use the pa_data constructor
padata = pacfish.pa_data(file);

% Option B: load the HDF5 file manually and instantiate pa_data that way
[binary_data, meta_acquisition, meta_device] = pacfish.load_data(file);
padata_2 = pacfish.pa_data(binary_data, meta_acquisition, meta_device);
