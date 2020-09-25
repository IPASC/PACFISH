classdef ipasc_tool
    properties 
        binary_time_series_data ;
        meta_data = struct()
        meta_data_device = struct()
        SamplingFrequency ;
    end
    
    methods
        %% Constructor for the api
        function obj = ipasc_tool(varargin)
            if (nargin==0)
                [filename, pathname] = uigetfile({'*.hdf5','*.h5'}, 'Pick a HDF5 file to open');
                if (isequal(filename,0) || isequal(pathname,0))
                    error('No file selected'); 
                end
                file = [pathname, filename]; 
            else
                file = varargin{1};
            end
            % test the file
            [~, ~, ext] = fileparts(file);
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
                    obj.binary_time_series_data = S.(names{i});
                elseif (strcmp(names{i}, 'meta_data'))
                    obj.meta_data = S.(names{i});
                elseif (strcmp(names{i}, 'meta_data_device'))
                    obj.meta_data_device = S.(names{i});
                else
                    warning(['The field ', names{i}, ' is not saved']);
                end
            end

            fprintf('\tReading completed\n\n**********************\n');
          
        end
            
     
        %% Other methods
        function show_data(obj,varargin)
            if (nargin==1)
                dB = 40;
            else
                dB = varargin{1};
            end
            N = size(obj.binary_time_series_data,1);
            M = ceil(N/3);
            for i=1:N
                 subplot(3,M,i); imagesc(rf2log(squeeze(obj.binary_time_series_data(i,:,:)), dB)); 
            end
        end
        
        %% compute the sampling frequency
        function update_parameter(obj)
            obj.SamplingFrequency = 1/obj.meta_data.ad_sampling_rate;
        end
    end
                
end

%% Temporary function used in the constructor  
function S = extract_field(S, file, location, struc)
    for i=1:length(struc.Groups)
        name = struc.Groups(i).Name;
        k=find(name=='/');
        name = name(k(end)+1:end);
        if (isempty(struc.Groups(i).Groups))
            % I create the current structure level
            S.(name) = struct();
            for j=1:length(struc.Groups(i).Datasets)
                % I read the dataset inside
                S.(name).(struc.Groups(i).Datasets(j).Name) = h5read(file, [location name '/' struc.Groups(i).Datasets(j).Name]);
            end
        else
            % new item to crate in the structure
            S.(name) = struct();
            S.(name) = extract_field(S.(name), file, [location name '/' ], struc.Groups(i));
        end
    end
end

function O=rf2bmode(I)
    O = abs(hilbert(I));
end

function O=bmode2log(I, varargin)
    dB = 40;
    if nargin>1
        dB = varargin{1};
    end
    O = 20*log10(I/max(I(:)))+dB;
    O(O<0) = 0;
end

function O = rf2log(I, varargin)
    O = bmode2log(rf2bmode(I), varargin{1});
end

