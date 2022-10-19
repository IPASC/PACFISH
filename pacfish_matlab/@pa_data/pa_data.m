%% SPDX-FileCopyrightText: 2022 International Photoacoustics Standardisation Consortium (IPASC)
%% SPDX-FileCopyrightText: 2022 François Varray
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
        
        %% List of getters (extracted from https://github.com/IPASC/PACFISH/blob/main/pacfish/core/PAData.py)
        function out = get_illuminator_ids(obj)
            % Returns a list of all IDs of the illumination elements that are added in this PAData instance.
            % Return list
            %   a list of all ids of the illumination elements
            out = [];
            if(isfield(obj.meta_data_device, 'illuminators'))
                out = fieldnames(obj.meta_data_device.illuminators);
            end
        end
        
        function out = get_detector_ids(obj)
            % Returns a list of all IDs of the detection elements that are added in this PAData instance.
            % Return list
            %   a list of all ids of the detection elements
            out = [];
            if(isfield(obj.meta_data_device, 'detectors'))
                out = fieldnames(obj.meta_data_device.detectors);
            end
        end
        
        function out = get_acquisition_meta_datum(obj, meta_data_tag)
            % This method returns data from the acquisition meta data dictionary.
            % Parameters meta_data_tag: a string instance for which to get the information.
            % Return object
            %   return value might be None, if the specified meta data tag was not found in the dictionary.
            out = get_field(obj.meta_data, meta_data_tag);
        end
        
        function out = get_custom_meta_datum(obj, meta_data_tag)
            % This method returns data from the acquisition meta data dictionary.
            % Parameters meta_data_tag: a string instance for which to get the information.
            % Return object
            %   return value might be None, if the specified meta data tag was not found in the dictionary.
            out = get_field(obj.meta_data, meta_data_tag);
        end
        
        function out = get_device_uuid(obj)
            % The UUID is a universally unique identifier to the device description that can be referenced.
            % Return str
            %   return value can be None, of no UUID was found in the meta data.
            out = get_field(obj.meta_data_device.general, 'unique_identifier');
        end
        
        function out = get_field_of_view(obj)
            % An array defining an approximate cuboid (3D) area that should be reconstructed in 3D Cartesian coordinates [x1_start, x1_end, x2_start, x2_end, x3_start, x3_end]. A 2D Field of View can be defined by setting the start and end coordinate of the respective dimension to the same value.
            % Return ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_field(obj.meta_data_device.general, 'field_of_view');
        end
        
        %
        function out = get_number_of_illuminators(obj)
            % The number of illuminators quantifies the number of illuminators that are used in the respective PA imaging device. Each of these illuminators is described by a set of illumination geometry parameters.
            % Return int
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_field(obj.meta_data_device.general, 'num_illuminators');
        end
        
        
        function out = get_number_of_detectors(obj)
            % The number of detectors quantifies the number of transducer elements that are used in the respective PA imaging device. Each of these transducer elements is described by a set of detection geometry parameters.
            % Return int
            %    return value can be None, of the key was not found in the meta data dictionary.
            out = get_field(obj.meta_data_device.general, 'num_detectors');
        end
        
        
        function out = get_illuminator_position(obj, identifier)
            % The illuminator position defines the position of the illuminator centroid in 3D cartesian coordinates [x1, x2, x3] .
            % Parameters : identifier str: The ID of a specific illumination element. If `None` then all illumination elements are queried.
            % Return ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_from_struct(obj.meta_data_device.illuminators, identifier, 'illuminator_position');
        end
        
        function out = get_illuminator_orientation(obj, identifier)
            % The illuminator orientation defines the rotation of the illuminator in 3D cartesian coordinates [r1, r2, r3]. It is the normal of the planar illuminator surface.
            % Parameters : identifier str: The ID of a specific illumination element. If `None` then all illumination elements are queried.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_from_struct(obj.meta_data_device.illuminators, identifier, 'illuminator_orientation');
        end
        
        
        function out = get_illuminator_geometry(obj, identifier)
            % The illuminator shape defines the shape of the optical fibres, so it describes  whether the illuminator is a point illuminator, or has a more continuous form. Illuminators can only have planar emitting surfaces.
            % Parameters: identifier str: The ID of a specific illumination element. If `None` then all illumination elements are queried.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_from_struct(obj.meta_data_device.illuminators, identifier, 'illuminator_geometry');
        end
        
        function out = get_illuminator_geometry_type(obj, identifier)
            % The illuminator geometry type defines the shape of the optical fibre (bundle) output. It determines the interpretation of the data in the illuminator geometry field.
            % The following geometry types are currently supported:
            % - "CIRCULAR" - defined by a single value that determines the radius of the circle
            % - "SPHERE" - defined by a single value that determines the radius of the sphere
            % - "CUBOID" - defined by three values that determine the extent of the cuboid in x, y,nand z dimensions before the position and orientation transforms.
            % - "MESH" - defined by a STL-formatted string that determines the positions of points and faces before the position and orientation transforms.
            % Parameters: identifier str: The ID of a specific illumination element. If `None` then all illumination elements are queried.
            % Return str
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = [];
            if (isempty(identifier))
                identifier = fieldnames(obj.meta_data_device.illuminators);
            end
            if (isempty(identifier))
                disp('No orientation illuminator found in the padata');
            else
                if (length(identifier)==1)
                    out = obj.meta_data_device.illuminators.(identifier{1}).illuminator_geometry_type;
                else
                    for i=1:length(identifier)
                        out{i} = obj.meta_data_device.illuminators.(identifier{1}).illuminator_geometry_type;
                    end
                end
            end
        end
        
        function out = get_wavelength_range(obj, identifier)
            % The wavelength range quantifies the wavelength  range that the illuminator is capable of generating by reporting three values: the minimum wavelength max, the maximum wavelength  max and a metric for the
            % accuracy accuracy: (min, max, accuracy). This parameter could for instance be (700, 900, 1.2), meaning that this illuminator can be tuned from 700 nm to 900 nm with an accuracy of 1.2 nm.
            % Parameters: identifier str: The ID of a specific illumination element. If `None` then all illumination elements are queried.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_from_struct(obj.meta_data_device.illuminators, identifier, 'wavelength_range');
        end
        
        
        
        function out = get_beam_energy_profile(obj, identifier)
            % The beam energy profile field is a discretized functional of wavelength (nm) that represents the light energy of the illuminator with regard to the wavelength. Thereby, systematic differences in multispectral image acquisitions can be accounted for.
            % Parameters: identifier str: The ID of a specific illumination element. If `None` then all illumination elements are queried.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_from_struct(obj.meta_data_device.illuminators, identifier, 'beam_energy_profile');
        end
        
        function out = get_beam_stability_profile(obj, identifier)
            % The beam noise profile field is a functional of wavelength (nm) that represents the standard deviation of the pulse-to-pulse energy of the illuminator with regard to the wavelength.
            % Parameters: identifier str: The ID of a specific illumination element. If `None` then all illumination elements are queried.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_from_struct(obj.meta_data_device.illuminators, identifier, 'beam_stability_profile');
        end
        
        function out = get_pulse_width(obj, identifier)
            % The pulse duration or pulse width describes the total length of a light pulse, measured as the time interval between the half-power points on the leading and trailing edges of the pulse.
            % Parameters: identifier str: The ID of a specific illumination element. If `None` then all illumination elements are queried.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_from_struct(obj.meta_data_device.illuminators, identifier, 'pulse_width');
        end
        
        
        function out = get_beam_profile(obj, identifier)
            % The beam intensity profile is a function of a spatial position that specifies the relative beam intensity according to the planar emitting surface of the illuminator shape.
            % Parameters: identifier str: The ID of a specific illumination element. If `None` then all illumination elements are queried.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_from_struct(obj.meta_data_device.illuminators, identifier, 'beam_intensity_profile');
        end
        
        
        function out = get_beam_profile_distance(obj, identifier)
            % The distance from the light source for measuring its beam intensity profile.
            % Parameters: identifier str: The ID of a specific illumination element. If `None` then all illumination elements are queried.
            % Return float
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_from_struct(obj.meta_data_device.illuminators, identifier, 'intensity_profile_distance');
        end
        
        
        function out = get_beam_divergence(obj, identifier)
            % The beam divergence angles represent the opening angles of the beam from the illuminator shape with respect to the orientation vector. This angle represented by the standard deviation of the beam divergence.
            % Parameters: identifier str: The ID of a specific illumination element. If `None` then all illumination elements are queried.
            % Return float
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_from_struct(obj.meta_data_device.illuminators, identifier, 'beam_divergence_angles');
        end
        
        function out = get_detector_position(obj, identifier)
            % The positions of each detection element in 3D Cartesian coordinates [x1, x2, x3].
            % Parameters : identifier: str The ID of a specific detection element. If `None` then all detection elements are queried.
            % Return ndarray
            % return value can be None, of the key was not found in the meta data dictionary.
            out = get_from_struct(obj.meta_data_device.detectors, identifier, 'detector_position');
            
        end
        
        
        function out = get_detector_orientation(obj, identifier)
            % The element orientation defines the rotation of the detection element in 3D cartesian coordinates [r1, r2, r3] in radians.
            % Parameters: identifier str: The ID of a specific detection element. If `None` then all detection elements are queried.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_from_struct(obj.meta_data_device.detectors, identifier, 'detector_orientation');
        end
        
        function out = get_detector_geometry(obj, identifier)
            % The element size defines the size of the detection element in 3D cartesian coordinates [x1, x2, x3] relative to its position and orientation.
            % Parameters: identifier str: The ID of a specific detection element. If `None` then all detection elements are queried.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_from_struct(obj.meta_data_device.detectors, identifier, 'detector_geometry');
        end
        
        function out = get_detector_geometry_type(obj, identifier)
            % The detector geometry type defines how to interpret the data in the detector geometry field.
            % The following geometry types are currently supported:
            % - "CIRCULAR" - defined by a single value that determines the radius of the circle
            % - "SPHERE" - defined by a single value that determines the radius of the sphere
            % - "CUBOID" - defined by three values that determine the extent of the cuboid in x, y, and z dimensions before the position and orientation transforms.
            % - "MESH" - defined by a STL-formatted string that determines the positions of points and faces before the position and orientation transforms.
            % Parameters: identifier str: The ID of a specific detection element. If `None` then all detection elements are queried.
            % Return str
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = [];
            if (isempty(identifier))
                identifier = fieldnames(obj.meta_data_device.detectors);
            end
            if (isempty(identifier))
                disp('No orientation illuminator found in the padata');
            else
                if (length(identifier)==1)
                    out = obj.meta_data_device.detectors.(identifier{1}).detector_geometry_type;
                else
                    for i=1:length(identifier)
                        out{i} = obj.meta_data_device.detectors.(identifier{1}).detector_geometry_type;
                    end
                end
            end
        end
        
        function out = get_frequency_response(obj, identifier)
            % The frequency response is a functional that characterizes the response of the detection element to the frequency of the incident pressure waves.
            % Parameters: identifier str: The ID of a specific detection element. If `None` then all detection elements are queried.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_from_struct(obj.meta_data_device.detectors, identifier, 'frequency_response');
        end
        
        function out = get_angular_response(obj, identifier)
            % The angular response field characterizes the angular sensitivity of the detection element to the incident angle (relative to the elements orientation) of the incoming pressure wave.
            % Parameters: identifier str: The ID of a specific detection element. If `None` then all detection elements are queried.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_from_struct(obj.meta_data_device.detectors, identifier, 'angular_response');
        end
        
        function out = get_regions_of_interest(obj)
            % A list of named regions within the underlying 3D Cartesian coordinate system (cf. Device Metadata). Strings containing the region names are mapped to arrays that define either an approximate cuboid area (cf. Field of View) or a list of coordinates describing a set of 3D Cartesian coordinates surrounding the named region.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = [];
            if (isfield(obj.meta_data, 'regions_of_interest'))
                f = fieldnames(obj.meta_data.regions_of_interest);
                for i=1:length(f)
                    out{i} = obj.meta_data.regions_of_interest.(f{i});
                end
            end
        end
        
        
        function out = get_encoding(obj)
            % The encoding field is representative of the character set that was used to encode the binary data and the metadata. E.g. one of ‘UTF-8’, ‘ASCII’, ‘CP-1252’, …
            % Return str
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'encoding');
        end
        
        function out = get_compression(obj)
            % The compression field is representative of the compression method that was used to compress the binary data. E.g. one of ‘raw’, ‘gzip’, …
            % Return str
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'compression');
        end
        
        function out = get_data_UUID(obj)
            % 128-bit Integer displayed as a hexadecimal string in 5 groups separated by hyphens, in the form 8-4-4-4-12 for a total of 36 characters. The UUID is randomly generated using the UUID Version 4 standard.
            % Return str
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'uuid');
        end
        
        function out = get_data_type(obj)
            % The data type field represents the datatype of the binary data. This field is given in the C++ data type naming convention. E.g. ‘short’, ‘unsigned short’, ‘int’, ‘unsigned int’, ‘long’, ‘unsigned long’, ‘long long’, ‘float’, ‘double’, ‘long double’.
            % Return str
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'data_type');
        end
        
        function out = get_dimensionality(obj)
            % The dimensionality field represents the acquisition format of the binary data and specifies the number of spatiotemporal dimensions of the data that is comprised of one or more frames. E.g. ‘1D’, ‘2D’, ‘3D’, ‘1D+t’, 2D+t’, ‘3D+t’. In this notion, the time series sampling of one transducer would count as a “spatial” dimension. These are defined as 1D = [𝝉], 2D = [x1, 𝝉], 3D = [x1, 𝝉, x2]. The “+t” will then add a time dimension for multiple of these frames.
            % Return str
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'dimensionality');
        end
        
        function out = get_sizes(obj)
            % The sizes field quantifies the number of data points in each of the dimensions specified in the dimensionality field. e.g. [128, 2560, 26] with a “2D+t” dimensionality.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'sizes');
        end
        
        function out = get_photoacoustic_imaging_device_reference(obj)
            % A string referencing the UUID of the PA imaging device description as defined in the Device Metadata.
            % Return str
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'photoacoustic_imaging_device_reference');
        end
        
        function out = get_pulse_energy(obj)
            % A value specifying the pulse energy used to generate the photoacoustic signal. If the pulse energies are averaged over many pulses, the average value must be specified.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'pulse_energy');
        end
        
        function out = get_measurement_time_stamps(obj)
            % An array specifying the time at which a measurement was recorded.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'measurement_time_stamps');
        end
        
        function out = get_acquisition_wavelengths(obj)
            % A 1D array that contains all wavelengths used for the image acquisition.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'acquisition_wavelengths');
        end
        
        function out = get_time_gain_compensation(obj)
            % An array containing relative factors that have been used to correct the time series data for the effect of acoustic attenuation.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'time_gain_compensation');
        end
        
        function out = get_overall_gain(obj)
            % A single value describing a factor used to modify the amplitude of the raw time series data.
            % Return float
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'overall_gain');
        end
        
        function out = get_element_dependent_gain(obj)
            % An array that contains the relative factors used for apodisation or detection element-wise sensitivity corrections.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'element_dependent_gain');
        end
        
        function out = get_temperature(obj)
            % An array describing the temperature of the imaged space (covering both the imaged medium and the coupling agent) for each measurement.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'temperature_control');
        end
        
        function out = get_acoustic_coupling_agent(obj)
            % A string representing the acoustic coupling agent that is used.
            % Return str
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'acoustic_coupling_agent');
        end
        
        function out = get_speed_of_sound(obj)
            % Either a single value representing the mean global speed of sound in the entire imaged medium or a 3D array representing a heterogeneous speed of sound map in
            % the device coordinate system. This definition covers both the imaged medium and the coupling agent.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'speed_of_sound');
        end
        
        function out = get_scanning_method(obj)
            % A string representing the scanning method that is used. The following descriptions can be used: (“composite_scan”, “full_scan”). This flag determines the
            % way the metadatum “measurement” is defined.
            % Return str
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'scanning_method');
        end
        
        function out = get_sampling_rate(obj)
            % A single value referring to the rate at which samples of the analogue signal are taken to be converted into digital form.
            % Return float
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'ad_sampling_rate');
        end
        
        function out = get_frequency_domain_filter(obj)
            % The frequency threshold levels that have been applied to filter the raw time series data.
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'frequency_domain_filter');
        end
        
        function out = get_measurement_spatial_poses(obj)
            % Coordinates describing the position and orientation changes of the acquisition system relative to the measurement of reference (first measurement).
            % Return np.ndarray
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'measurement_spatial_poses');
        end
        
        function out = get_measurements_per_image(obj)
            % A single value describing the number of measurements that constitute the dataset corresponding to one image.
            % Return int
            %   return value can be None, of the key was not found in the meta data dictionary.
            out = get_acquisition_meta_datum(obj, 'measurements_per_image');
        end
        
    end
    
end


function out = get_from_struct(obj_struct, identifier, tag)
out = [];
if (isempty(identifier))
    identifier = fieldnames(obj_struct);
end
if (isempty(identifier))
    disp(['No ' obj_struct 'found in the padata']);
else
    if (size(obj_struct.(identifier{1}).(tag),2)==1)
        for i=1:length(identifier)
            out(:,i) = obj_struct.(identifier{i}).(tag);
        end
    else
        for i=1:length(identifier)
            out(:,:,i) = obj_struct.(identifier{i}).(tag);
        end
    end
end
end


function out = get_field(obj_struct, tag)
out = [];
if(isfield(obj_struct, tag))
    out = obj_struct.(tag);
end
end