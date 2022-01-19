% read with a given file in Matlab
path = 'C:\standardised-image-reconstruction\';
filename = '1BdSLl4BSxpxXDwWcBKKVV4nHULPe7IS8_ipasc.hdf5';
file = [path filename];

% Create an instance of the class
% Option A: use the pa_data constructor
padata = pacfish.pa_data(file);


% As a simple test, write the same data back into a different file
pacfish.write_data("test.hdf5", padata)

% And load it again
padata_rewritten = pacfish.pa_data("test.hdf5");
