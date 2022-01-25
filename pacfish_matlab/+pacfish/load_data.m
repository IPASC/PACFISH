%% SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
%% SPDX-FileCopyrightText: 2021 François Varray
%% SPDX-FileCopyrightText: 2022 Janek Gröhl
%% SPDX-License-Identifier: BSD 3-Clause License

function [binary_data, meta_acquisition, meta_device] = load_data(file)
    %% Central PACFISH loading function.
    %% Loads an HDF5 file into the given pa_data instance.

    % test the file
    [~, ~, ext] = fileparts(file);
    % If file does not have an extension, assume it is "hdf5".
    if (isempty(ext))
        file = [file '.hdf5'];
    end
    if (exist(file,'file')==0)
        error(['The file ',file,' does not exist.']);
    end


    fprintf('\n\n\n**********************\n\n\tTry to read %s file\n\n', file);
    h5_info = h5info(file);

    % read one or several dataset
    for i=1:length(h5_info.Datasets)
        S.(h5_info.Datasets(i).Name) = h5read(file, ['/' h5_info.Datasets(i).Name]);
    end

    % Extract the others dataset in the h5 file
    S = extract_field(S, file, '/', h5_info);

    % sparse the various structure...
    names = fieldnames(S);
    for i=1:length(names)
        if (strcmp(names{i}, 'binary_time_series_data'))
            binary_data = S.(names{i});
        elseif (strcmp(names{i}, 'meta_data'))
            meta_acquisition = S.(names{i});
        elseif (strcmp(names{i}, 'meta_data_device'))
            meta_device = S.(names{i});
        else
            warning(['The field ', names{i}, ' is not saved']);
        end
    end

    fprintf('\tReading completed\n\n**********************\n');
end


%% Temporary function used in the constructor  
function S = extract_field(S, file, location, struc)
    for i=1:length(struc.Groups)
        name = struc.Groups(i).Name;
        k=find(name=='/');
        name = name(k(end)+1:end);
        struct_name = [name];
        try
            S.(struct_name) = struct();
        catch ME
            struct_name = ['deleteme' name];
            S.(struct_name) = struct();
        end
        if (isempty(struc.Groups(i).Groups))
            % I create the current structure level
            for j=1:length(struc.Groups(i).Datasets)
                % I read the dataset inside
                S.(struct_name).(struc.Groups(i).Datasets(j).Name) = h5read(file, [location name '/' struc.Groups(i).Datasets(j).Name]);
            end
        else
            % new item to crate in the structure
            S.(struct_name) = extract_field(S.(struct_name), file, [location name '/' ], struc.Groups(i));
        end
    end
end


