%% SPDX-FileCopyrightText: 2022 International Photoacoustics Standardisation Consortium (IPASC)
%% SPDX-FileCopyrightText: 2022 Janek Gröhl
%% SPDX-License-Identifier: BSD 3-Clause License

classdef kwave_adapter
    properties
        sensor_definition = 0;
        time_series_data = 0;
        medium = 0;
        kgrid = 0;
        fov = 0;
    end
    
    methods
                
        %% Constructor for the api
        function obj = kwave_adapter(varargin)
            if (nargin<=4)
                error("Need at least sensor definition, time series, medium, and kgrid as input.")
            end
            obj.sensor_definition = varargin{1};
            obj.time_series_data = permute(varargin{2}, [2, 1]);
            obj.medium = varargin{3};
            obj.kgrid = varargin{4};
            if (nargin>=5)
                obj.fov = varargin{5};
            end
        end
        
        function device_struct = generate_device_dict(obj, varargin)
            %% For now, this function supports a 2D kartesian definition
            %% and the kWaveArray class definition, only!
            
            if isa(obj.sensor_definition, "kWaveArray")
                disp("kWaveArray detected!");
                num_detectors = obj.sensor_definition.number_elements;
                device_struct.general.num_detectors = num_detectors;
                device_struct.general.num_illuminators = 0;
                
                for det = 1:num_detectors
                    index = strcat("deleteme", sprintf( '%010d', (det-1) ));
                    elem = obj.sensor_definition.elements{1, det};
                    device_struct.detectors.(index).detector_position = [elem.position(1) elem.position(3) elem.position(2)];
                    device_struct.detectors.(index).detector_geometry_type = "CUBOID";
                    device_struct.detectors.(index).detector_geometry = [elem.width elem.length elem.width];
                    device_struct.detectors.(index).detector_orientation = [elem.orientation(1) elem.orientation(3) elem.orientation(2)];
                end
                
                %% FIXME: we need a FOV definition.
                if any(obj.fov)
                    device_struct.general.field_of_view = obj.fov;
                else
                    device_struct.general.field_of_view = [];
                end

            else
                disp("Assuming 2D Kartesian definition.");
                num_detectors = size(obj.sensor_definition.mask, 2);
                device_struct.general.num_detectors = num_detectors;
                device_struct.general.num_illuminators = 0;
                if any(obj.fov)
                    device_struct.general.field_of_view = obj.fov;
                else
                    device_struct.general.field_of_view = [min(obj.sensor_definition.mask(1, :))+0.001 max(obj.sensor_definition.mask(1, :))-0.001 0 0 min(obj.sensor_definition.mask(2, :))+0.001 max(obj.sensor_definition.mask(2, :))-0.001];
                end
                for det = 1:num_detectors
                    index = strcat("deleteme", sprintf( '%010d', (det-1) ));
                    device_struct.detectors.(index).detector_position = [obj.sensor_definition.mask(1, det) 0 obj.sensor_definition.mask(2, det)];
                    device_struct.detectors.(index).detector_geometry_type = "CUBOID";
                    device_struct.detectors.(index).detector_geometry = [obj.kgrid.dx obj.kgrid.dz obj.kgrid.dy];
                    device_struct.detectors.(index).frequency_response = obj.sensor_definition.frequency_response;
                end
            end
        end
        
        function acquisition_struct = generate_acquisition_dict(obj, varargin)
            acquisition_struct.ad_sampling_rate = 1.0 / obj.kgrid.dt;
            acquisition_struct.sizes = size(obj.time_series_data);
            acquisition_struct.speed_of_sound = [obj.medium.sound_speed];
        end
        
        function return_data = get_pa_data(obj, varargin)
            device_dict = obj.generate_device_dict();
            acquisition_dict = obj.generate_acquisition_dict();
            return_data = pa_data(obj.time_series_data, acquisition_dict, device_dict);
        end
    end
end