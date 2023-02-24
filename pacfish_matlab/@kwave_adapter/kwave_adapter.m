%% SPDX-FileCopyrightText: 2022 International Photoacoustics Standardisation Consortium (IPASC)
%% SPDX-FileCopyrightText: 2022 Janek Gröhl
%% SPDX-FileCopyrightText: 2023 Jeffrey Sackey
%% SPDX-FileCopyrightText: 2023 François Varray
%% SPDX-License-Identifier: BSD 3-Clause License

classdef kwave_adapter
    properties
        sensor_definition = 0;
        time_series_data = 0;
        medium = 0;
        kgrid = 0;
        fov = 0;
        % Assume 3D defintion of rectangular elements for transducer elements by default.
        model = 1;
        % Position variables made in place of getting the positions (As
        % that cannot be done with line elements)
        position1 = 0; 
        position2 = 0;
        position3 = 0;
        % This variable is later used to determine height for the line
        % elements
        lineheight = 0;
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
            % Changed order of model and fov so it is easier to not define
            % fov when calling the function
            if (nargin==5) % Checks whether the number of inputs from function call is 5 or not
                obj.model = varargin{5}; % Used to determine what type of simulation is being done  
            end
            if (nargin>=6) % Checks whether the number of inputs from function call is 6 or above
               obj.fov = varargin{6}; % Takes the fov definition
            end
            obj.lineheight = 0.1e-3; % We assume the height of line elements is this  
        end
        
        function device_struct = generate_device_dict(obj, varargin)
            %% For now, this function supports a 2D kartesian definition
            %% and the kWaveArray class definition, only!
            
            if isa(obj.sensor_definition, "kWaveArray")
                disp("kWaveArray detected!");
                num_detectors = obj.sensor_definition.number_elements;
                device_struct.general.num_detectors = num_detectors;
                device_struct.general.num_illuminators = 0;
                min_1 = 100000;
                min_2 = 100000;
                min_3 = 100000;
                switch obj.model
                    case 1 % 3D with position elements used as detector - all this would be the original code function
                        for det = 1:num_detectors
                            if (min_1 > obj.sensor_definition.elements{1, det}.position(1))
                                min_1 = obj.sensor_definition.elements{1, det}.position(1);
                            end
                            if (min_2 > obj.sensor_definition.elements{1, det}.position(2))
                                min_2 = obj.sensor_definition.elements{1, det}.position(2);
                            end
                            if (min_3 > obj.sensor_definition.elements{1, det}.position(3))
                                min_3 = obj.sensor_definition.elements{1, det}.position(3);
                            end
                        end
                        for det = 1:num_detectors
                            index = strcat("deleteme", sprintf( '%010d', (det-1) ));
                            elem = obj.sensor_definition.elements{1, det};
                            disp(elem)
                            device_struct.detectors.(index).detector_position = [elem.position(1)-min_1 elem.position(3)-min_3 elem.position(2)-min_2];
                            device_struct.detectors.(index).detector_geometry_type = "CUBOID";
                            device_struct.detectors.(index).detector_geometry = [elem.length elem.width elem.length]; 
                            device_struct.detectors.(index).detector_orientation = [elem.orientation(1) elem.orientation(3) elem.orientation(2)];
                        end
                    case 2 % 3D with line elements used as detector
                        for det = 1:num_detectors
                            % This part of the code checks whether a line
                            % exists in each
                            % dimension and if so creates a position value
                            % using the line's midpoint 
                            % If one does not exist then the start point is
                            % used as this would mean in that specific
                            % dimension start point = end point
                            if dist(obj.sensor_definition.elements{1, det}.start_point(1),obj.sensor_definition.elements{1, det}.end_point(1)) ~= 0 % Checks whether the distance between the start point/end point in the x direction is not 0
                                % This finds the distance between the start
                                % point and end point in the x dimension, halves it and adds
                                % it to the smaller distance to get
                                % midpoint
                                obj.position1 = (dist(obj.sensor_definition.elements{1, det}.start_point(1),obj.sensor_definition.elements{1, det}.end_point(1))/2) + min(obj.sensor_definition.elements{1, det}.start_point(1),obj.sensor_definition.elements{1, det}.end_point(1));
                            else
                                % This sets the position1 variable to the
                                % lines
                                % start point in the x dimension
                                obj.position1 = obj.sensor_definition.elements{1, det}.start_point(1);
                            end
                            if (min_1 > obj.position1)
                                % Performs the same thing as 
                                %if (min_1 > obj.sensor_definition.elements{1, det}.position(1))
                                    %min_1 = obj.sensor_definition.elements{1, det}.position(1);
                                % in original code just uses the new
                                % positions made
                                min_1 = obj.position1;
                            end
                            if dist(obj.sensor_definition.elements{1, det}.start_point(2),obj.sensor_definition.elements{1, det}.end_point(2)) ~= 0 % Checks whether the distance between the start point/end point in the y direction is not 0
                                % This finds the distance between the start
                                % point and end point in the y dimension, halves it and adds
                                % it to the smaller distance to get
                                % midpoint
                                obj.position2 = (dist(obj.sensor_definition.elements{1, det}.start_point(2),obj.sensor_definition.elements{1, det}.end_point(2))/2) + min(obj.sensor_definition.elements{1, det}.start_point(2),obj.sensor_definition.elements{1, det}.end_point(2));
                            else
                                 % This sets the position2 variable to the
                                % lines
                                % start point in the y dimension
                                obj.position2 = obj.sensor_definition.elements{1, det}.start_point(2);
                            end
                            if (min_2 > obj.position2)
                                % Performs the same thing as 
                                %if (min_2 > obj.sensor_definition.elements{1, det}.position(2))
                                    %min_2 = obj.sensor_definition.elements{1, det}.position(2);
                                % in original code just uses the new
                                % positions made
                                min_2 = obj.position2;
                            end            
                            if dist(obj.sensor_definition.elements{1, det}.start_point(3),obj.sensor_definition.elements{1, det}.end_point(3)) ~= 0 % Checks whether the distance between the start point/end point in the z direction is not 0
                                % This finds the distance between the start
                                % point and end point in the z dimension, halves it and adds
                                % it to the smaller distance to get
                                % midpoint
                                obj.position3 = (dist(obj.sensor_definition.elements{1, det}.start_point(3),obj.sensor_definition.elements{1, det}.end_point(3))/2) + min(obj.sensor_definition.elements{1, det}.start_point(3),obj.sensor_definition.elements{1, det}.end_point(3));
                            else
                                 % This sets the position3 variable to the
                                % lines
                                % start point in the z dimension
                                obj.position3 = obj.sensor_definition.elements{1, det}.start_point(3);
                            end
                            if (min_3 > obj.position3)
                                % Performs the same thing as 
                                %if (min_3 > obj.sensor_definition.elements{1, det}.position(3))
                                    %min_3 = obj.sensor_definition.elements{1, det}.position(3);
                                % in original code just uses the new
                                % positions made
                                min_3 = obj.position3;
                            end
                        end
                        for det = 1:num_detectors
                            index = strcat("deleteme", sprintf( '%010d', (det-1) ));
                            elem = obj.sensor_definition.elements{1, det};
                            if dist(elem.start_point(1),elem.end_point(1)) ~= 0 % Checks whether the distance between the start point/end point in the x direction is not 0
                                % This finds the distance between the start
                                % point and end point in the x dimension, halves it and adds
                                % it to the smaller distance to get
                                % midpoint
                                obj.position1 = (dist(elem.start_point(1),elem.end_point(1))/2) + min(elem.start_point(1),elem.end_point(1));
                            else
                                 % This sets the position1 variable to the
                                % lines
                                % start point in the x dimension
                                obj.position1 = elem.start_point(1);
                            end
                            if dist(elem.start_point(2),elem.end_point(2)) ~= 0 % Checks whether the distance between the start point/end point in the y direction is not 0
                                % This finds the distance between the start
                                % point and end point in the y dimension, halves it and adds
                                % it to the smaller distance to get
                                % midpoint
                                obj.position2 = (dist(elem.start_point(2),elem.end_point(2))/2) + min(elem.start_point(2),elem.end_point(2));
                            else
                                 % This sets the position2 variable to the
                                % lines
                                % start point in the y dimension
                                obj.position2 = elem.start_point(2);
                            end
                            if dist(elem.start_point(3),elem.end_point(3)) ~= 0 % Checks whether the distance between the start point/end point in the z direction is not 0
                                % This finds the distance between the start
                                % point and end point in the z dimension, halves it and adds
                                % it to the smaller distance to get
                                % midpoint
                                obj.position3 = (dist(elem.start_point(3),elem.end_point(3))/2) + min(elem.start_point(3),elem.end_point(3));
                            else
                                 % This sets the position3 variable to the
                                % lines
                                % start point in the z dimension
                                obj.position3 = elem.start_point(3);
                            end
                            device_struct.detectors.(index).detector_position = [obj.position1-min_1 obj.position3-min_3 obj.position2-min_2]; % Same thing as old code but elem.position(1) is replaced with obj.position1 for example
                            device_struct.detectors.(index).detector_geometry_type = "LINE"; % They are line elements
                            % Length is determined by checking the
                            % distance between the start point and end
                            % point of the line in the x, y and z
                            % directions, squaring each and summing
                            % them and lastly square rooting the sum
                            % which is using pythagoras to determine
                            % line length 
                            % If change is in only 1 dimension other
                            % distances
                            % would be 0 and therefore the distance of the
                            % non-0 direction would be not be considered
                            % This length is stored as elem.width as that's
                            % how rectangle elements would store their length
                            elem.width = sqrt((dist(elem.start_point(1),elem.end_point(1)))^2+(dist(elem.start_point(2),elem.end_point(2)))^2+(dist(elem.start_point(3),elem.end_point(3)))^2);
                            % Width is the line height determined
                            % earlier
                            % Stored as elem.length as that's where
                            % rectangle elements store their width
                            elem.length = obj.lineheight;
                            % The project uses sohcahtoa
                            % to determine the angle used for
                            % orientation 
                            % Specifically uses cos theta =
                            % adjacent/hypotenuse
                            % adjacent = y direction distance
                            % hypotenuse = magnitude of element length in
                            % the y and z direction
                            costheta1 = dist(elem.start_point(2),elem.end_point(2))/(sqrt((dist(elem.start_point(2),elem.end_point(2)))^2+(dist(elem.start_point(3),elem.end_point(3)))^2));
                            % If the denominator of the fraction is = 0
                            % then the result would be not a number
                            % This checks whether the result is not a
                            % number
                            % and sets cos theta to 0 if so as this should
                            % be the default value
                            if isnan(costheta1)
                                costheta1 = 0;
                            end
                            % Sets the orientation to 180 - the cos inverse
                            % of cos theta to fix any directional issues
                            % the normal inverse would cause
                            orientation1 = 180 - acosd(costheta1);	
                            % The project uses sohcahtoa
                            % to determine the angle used for
                            % orientation 
                            % Specifically uses cos theta =
                            % adjacent/hypotenuse
                            % adjacent = z direction distance
                            % hypotenuse = magnitude of element length in
                            % the x and z direction
                            costheta2 = dist(elem.start_point(3),elem.end_point(3))/(sqrt((dist(elem.start_point(3),elem.end_point(3)))^2+(dist(elem.start_point(1),elem.end_point(1)))^2));
                            % If the denominator of the fraction is = 0
                            % then the result would be not a number
                            % This checks whether the result is not a
                            % number
                            % and sets cos theta to 0 if so as this should
                            % be the default value
                            if isnan(costheta2)
                                costheta2 = 0;
                            end
                            orientation2 = 180 - acosd(costheta2);
                        	% The project uses sohcahtoa
                            % to determine the angle used for
                            % orientation 
                            % Specifically uses cos theta =
                            % adjacent/hypotenuse
                            % adjacent = x direction distance
                            % hypotenuse = magnitude of element length in
                            % the x and y direction
                            costheta3 = dist(elem.start_point(1),elem.end_point(1))/(sqrt((dist(elem.start_point(2),elem.end_point(2)))^2+(dist(elem.start_point(1),elem.end_point(1)))^2));
                            % If the denominator of the fraction is = 0
                            % then the result would be not a number
                            % This checks whether the result is not a
                            % number
                            % and sets cos theta to 0 if so as this should
                            % be the default value
                            if isnan(costheta3)
                                costheta3 = 0;
                            end
                            % Sets the orientation to 180 - the cos inverse
                            % of cos theta to fix any directional issues
                            % the normal inverse would cause
                            orientation3 = 180 - acosd(costheta3);	
                            % Stores the 3 orientations made as the
                            % detector orientation

                            device_struct.detectors.(index).detector_orientation = [orientation1 orientation3 orientation2];
                            device_struct.detectors.(index).detector_geometry = [elem.length elem.width elem.length];
                        end
                    case 3 % 2D with position elements used as detector
                        for det = 1:num_detectors
                            if (min_1 > obj.sensor_definition.elements{1, det}.position(1))
                                min_1 = obj.sensor_definition.elements{1, det}.position(1);
                            end
                            if (min_2 > obj.sensor_definition.elements{1, det}.position(2))
                                min_2 = obj.sensor_definition.elements{1, det}.position(2);
                            end
                            % Original Code but the min_3 section removed
                            % as the input is not 3D
                        end
                        for det = 1:num_detectors
                            index = strcat("deleteme", sprintf( '%010d', (det-1) ));
                            elem = obj.sensor_definition.elements{1, det};
                            disp(elem)
                            % Original code with the min_3-elem.position(3)
                            % removed as the input is 2D
                            device_struct.detectors.(index).detector_position = [elem.position(1)-min_1 0 elem.position(2)-min_2]; 
                            device_struct.detectors.(index).detector_geometry_type = "RECTANGLE";
                            % Geometry only requires 2 dimensions here x
                            % and y as input is 2D
                            device_struct.detectors.(index).detector_geometry = [elem.length 0 elem.width];
                            % Orientation in 2D only has 1 value rather
                            % than an array of 3 so this change adjusts for
                            % that
                            device_struct.detectors.(index).detector_orientation = [elem.orientation];
                            disp(device_struct.detectors.(index).detector_orientation)
                        end
                    case 4 % 2D with line elements used as detector
                         % This part of the code checks whether a line
                            % exists in each
                            % dimension and if so creates a position value
                            % using the line's midpoint 
                            % If one does not exist then the start point is
                            % used as this would mean in that specific
                            % dimension start point = end point
                        for det = 1:num_detectors
                            if dist(obj.sensor_definition.elements{1, det}.start_point(1),obj.sensor_definition.elements{1, det}.end_point(1)) ~= 0 % Checks whether the distance between the start point/end point in the x direction is not 0
                                % This finds the distance between the start
                                % point and end point in the x dimension, halves it and adds
                                % it to the smaller distance to get
                                % midpoint
                                obj.position1 = (dist(obj.sensor_definition.elements{1, det}.start_point(1),obj.sensor_definition.elements{1, det}.end_point(1))/2) + min(obj.sensor_definition.elements{1, det}.start_point(1),obj.sensor_definition.elements{1, det}.end_point(1));
                            else
                                 % This sets the position1 variable to the
                                 % lines
                                 % start point in the x dimension
                                obj.position1 = obj.sensor_definition.elements{1, det}.start_point(1);
                            end
                            if (min_1 > obj.position1)
                                % Performs the same thing as 
                                %if (min_1 > obj.sensor_definition.elements{1, det}.position(1))
                                    %min_1 = obj.sensor_definition.elements{1, det}.position(1);
                                % in original code just uses the new
                                % positions made
                                min_1 = obj.position1;
                            end
                            if dist(obj.sensor_definition.elements{1, det}.start_point(2),obj.sensor_definition.elements{1, det}.end_point(2)) ~= 0 % Checks whether the distance between the start point/end point in the y direction is not 0
                                % This finds the distance between the start
                                % point and end point in the y dimension, halves it and adds
                                % it to the smaller distance to get
                                % midpoint
                                obj.position2 = (dist(obj.sensor_definition.elements{1, det}.start_point(2),obj.sensor_definition.elements{1, det}.end_point(2))/2) + min(obj.sensor_definition.elements{1, det}.start_point(2),obj.sensor_definition.elements{1, det}.end_point(2));
                            else
                                % This sets the position2 variable to the
                                % lines
                                % start point in the y dimension
                                obj.position2 = obj.sensor_definition.elements{1, det}.start_point(2);
                            end
                            if (min_2 > obj.position2)
                                % Performs the same thing as 
                                %if (min_2 > obj.sensor_definition.elements{1, det}.position(2))
                                    %min_2 = obj.sensor_definition.elements{1, det}.position(2);
                                % in original code just uses the new
                                % positions made
                                min_2 = obj.position2;
                            end
                        end
                        for det = 1:num_detectors
                            index = strcat("deleteme", sprintf( '%010d', (det-1) ));
                            elem = obj.sensor_definition.elements{1, det};
                            if dist(elem.start_point(1),elem.end_point(1)) ~= 0 % Checks whether the distance between the start point/end point in the x direction is not 0
                                obj.position1 = (dist(elem.start_point(1),elem.end_point(1))/2) + min(elem.start_point(1),elem.end_point(1));
                                % This finds the distance between the start
                                % point and end point in the x dimension, halves it and adds
                                % it to the smaller distance to get
                                % midpoint
                            else
                                % This sets the position1 variable to the
                                % lines
                                % start point in the x dimension
                                obj.position1 = elem.start_point(1);
                            end
                            if dist(elem.start_point(2),elem.end_point(2)) ~= 0 % Checks whether the distance between the start point/end point in the y direction is not 0
                                obj.position2 = (dist(elem.start_point(2),elem.end_point(2))/2) + min(elem.start_point(2),elem.end_point(2));
                                 % This finds the distance between the start
                                % point and end point in the y dimension, halves it and adds
                                % it to the smaller distance to get
                                % midpoint
                            else
                                 % This sets the position2 variable to the
                                % lines
                                % start point in the y dimension
                                obj.position2 = elem.start_point(2);
                            end
                            device_struct.detectors.(index).detector_position = [obj.position1-min_1 0 obj.position2-min_2];
                            device_struct.detectors.(index).detector_geometry_type = "LINE"; % They are line elements
                            % Length is determined by checking the
                            % distance between the start point and end
                            % point of the line in the x and y
                            % directions, squaring each and summing
                            % them and lastly square rooting the sum
                            % which is using pythagoras to determine
                            % line length assuming there is a change in
                            % both x and y
                            % If change is in 1 dimension only the other distance
                            % would be 0 and therefore the distance of the
                            % non-0 direction would not be considered
                            % This length is stored as elem.width as that's
                            % how rectangle elements would store their length
                            elem.width = sqrt((dist(elem.start_point(1),elem.end_point(1)))^2+(dist(elem.start_point(2),elem.end_point(2)))^2);
                            
                            % The project uses sohcahtoa
                            % to determine the angle used for
                            % orientation 
                            % Specifically uses cos theta =
                            % adjacent/hypotenuse
                            % adjacent = y direction distance
                            % hypotenuse = element length (elem.width)
                            costheta = dist(elem.start_point(2),elem.end_point(2))/elem.width;
                            % Sets the orientation to 180 - the cos inverse
                            % of cos theta to fix any directional issues
                            % the normal inverse would cause
                            elem.orientation = acosd(costheta);
                            
                            % Width is the line height determined
                            % earlier
                            % Stored as elem.length as that's where
                            % rectangle elements store their width
                            elem.length = obj.lineheight;
                            % Orientation doesn't exist for lines
                             % Geometry only requires 2 dimensions here x
                            % and y as input is 2D
                            
                            device_struct.detectors.(index).detector_orientation = elem.orientation; % Sets element orientation
                            
                            device_struct.detectors.(index).detector_geometry = [elem.length 0 elem.width]; 

                        end
                end
                

                if any(obj.fov) % Checks whether FOV was given as an input (was previously checked above)
                    device_struct.general.field_of_view = obj.fov; 
                else
                    device_struct.general.field_of_view = [0 (obj.kgrid.Nx*obj.kgrid.dx) 0 (obj.kgrid.Nz*obj.kgrid.dz) 0 (obj.kgrid.Ny*obj.kgrid.dy)]; % If not then the program defines the FOV as full view taken from kgrid - dz/Nz are already 0 for 2D simulations 
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