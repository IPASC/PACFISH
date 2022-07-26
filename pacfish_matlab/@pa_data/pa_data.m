%% SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
%% SPDX-FileCopyrightText: 2021 François Varray
%% SPDX-FileCopyrightText: 2022 Janek Gröhl
%% SPDX-License-Identifier: BSD 3-Clause License

classdef pa_data
    properties 
        binary_time_series_data ;
        meta_data = struct();
        meta_data_device = struct();
    end
    
    methods
                
        %% Constructor for the api
        function obj = pa_data(varargin)
            file = "0";
            if (nargin==0)
                [filename, pathname] = uigetfile({'*.hdf5','*.h5'}, 'Pick a HDF5 file to open');
                if (isequal(filename,0) || isequal(pathname,0))
                    error('No file selected'); 
                end
                file = [pathname, filename]; 
            elseif (nargin==1)
                file = varargin{1};
            elseif (nargin==3)
                obj.binary_time_series_data = varargin{1};
                obj.meta_data = varargin{2};
                obj.meta_data_device = varargin{3};
            end
            
            if file ~= "0"
                [binary_data, meta_acquisition, meta_device] = pacfish.load_data(file);
                obj.binary_time_series_data = binary_data;
                obj.meta_data = meta_acquisition;
                obj.meta_data_device = meta_device;
            end
           
        end
        
        
        function obj = save_data(obj, file, varargin)
            pacfish.write_data(file, obj, varargin{1});
        end
        
        
    end
                
end


