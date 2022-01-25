%% SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
%% SPDX-FileCopyrightText: 2022 Janek Gröhl
%% SPDX-License-Identifier: BSD 3-Clause License

function write_data(filepath, padata)
    %% Central PACFISH saving function.
    %% Saves a pa_data class into an HDF5 container.
    
    % test the file
    [~, ~, ext] = fileparts(filepath);
    % If file does not have an extension, assume it is "hdf5".
    if (isempty(ext))
        filepath = [filepath '.hdf5'];
    end
    
    save_field(filepath, "/binary_time_series_data", padata.binary_time_series_data)
    save_field(filepath, "/meta_data", padata.meta_data)
    save_field(filepath, "/meta_data_device", padata.meta_data_device)

    
function save_field(filepath, dataset, data)
    if isstruct(data)
        fields = fieldnames(data);
        for k=1:length(fields)
            ds_name = strcat(dataset, "/", erase(fields{k}, "deleteme"));
            ds_data = data.(fields{k});
            if ischar(ds_data)
                ds_data = string(ds_data);
            end
            save_field(filepath, ds_name, ds_data)
        end       
    else
        h5create(filepath, dataset, size(data), 'Datatype', class(data))
        h5write(filepath, dataset, data)
    end
