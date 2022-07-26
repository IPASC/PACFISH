%% SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
%% SPDX-FileCopyrightText: 2022 François Varray
%% SPDX-FileCopyrightText: 2022 Janek Gröhl
%% SPDX-License-Identifier: BSD 3-Clause License

classdef pacfish
       
    methods
                
        %% Constructor for the api
        function obj = pacfish(varargin)
%             obj.temp = 1;
        end
        
    end
    
    methods (Static)
        % loading function of the data
        function [binary_data, meta_acquisition, meta_device] = load_data(varargin)
            %% Central PACFISH loading function.
            file = varargin{1};
            
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

        
        
        function write_data(filepath, padata, varargin)
            %% Central PACFISH saving function.
            %% Saves a pa_data class into an HDF5 container.

            if isempty(varargin)
                overwrite = 0;
            else
                overwrite = varargin{1};
            end

            % delete existing file if exists and overwrite is true
            if (isfile(filepath) && overwrite)
                delete(filepath);
            end

            % test the file
            [~, ~, ext] = fileparts(filepath);
            % If file does not have an extension, assume it is "hdf5".
            if (isempty(ext))
                filepath = [filepath '.hdf5'];
            end

            save_field(filepath, "/binary_time_series_data", padata.binary_time_series_data)
            save_field(filepath, "/meta_data", padata.meta_data)
            save_field(filepath, "/meta_data_device", padata.meta_data_device)

        end

 
        end

 
        
        
        
end
                

%% Temporary function used in the constructor  
function S = extract_field(S, file, location, struc)

    for ds=1:length(struc.Datasets)
        name = struc.Datasets(ds).Name;
        struct_name = [name];
        S.(struct_name) = struct();
        S.(struct_name) = h5read(file, [location name]);
    end

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


    
function save_field(filepath, dataset, data)
    if isstruct(data)
        fields = fieldnames(data);
        for k=1:length(fields)
            ds_name = strcat(dataset, "/", erase(fields{k}, "deleteme"));
            ds_data = data.(fields{k});
            if ischar(ds_data)
%                 disp('cas du char...');
                ds_data = string(ds_data);
            end
            save_field(filepath, ds_name, ds_data)
        end       
    else
        h5create(filepath, dataset, size(data), 'Datatype', class(data))
        h5write(filepath, dataset, data)
    end
end