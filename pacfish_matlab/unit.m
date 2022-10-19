function unit(file)
%% load the data from python and reference matlab
pa_python = pa_data(file);
load(file); % load the pa_data structure

%% test of all the getters
%%- general getters of meta_data_device
assert(strcmp(pa_matlab.general.unique_identifier, pa_python.get_device_uuid), 'Error on device uuid getter')
assert(isempty(setdiff(pa_matlab.general.field_of_view, pa_python.get_field_of_view)), 'Error on field of view getter')
assert(pa_matlab.general.num_illuminators==pa_python.get_number_of_illuminators, 'Error on number of illuminators getter')
assert(pa_matlab.general.num_detectors==pa_python.get_number_of_detectors, 'Error on number of detectors getter')

%%- general getters of meta_data
assert(compare_struct(pa_matlab.regions_of_interest, pa_python.get_regions_of_interest), 'Error on region of interest getter')
assert(pa_matlab.speed_of_sound==pa_python.get_speed_of_sound, 'Error on speed of sound getter')
assert(strcmp(pa_matlab.encoding, pa_python.get_encoding), 'Error on encoding getter')
assert(strcmp(pa_matlab.compression, pa_python.get_compression), 'Error on compression getter')
assert(strcmp(pa_matlab.uuid, pa_python.get_data_UUID), 'Error on data UUID getter')
assert(strcmp(pa_matlab.data_type, pa_python.get_data_type), 'Error on dta type getter')
assert(strcmp(pa_matlab.dimensionality, pa_python.get_dimensionality), 'Error on dimensionality getter')
assert(strcmp(pa_matlab.photoacoustic_imaging_device_reference, pa_python.get_photoacoustic_imaging_device_reference), 'Error on photoacoustic device refrence getter')
assert(strcmp(pa_matlab.acoustic_coupling_agent, pa_python.get_acoustic_coupling_agent), 'Error on acoustic coupling agent getter')
assert(strcmp(pa_matlab.scanning_method, pa_python.get_scanning_method), 'Error on scanning getter')
assert(isempty(setdiff(pa_matlab.sizes, pa_python.get_sizes)), 'Error on size getter')
assert(isempty(setdiff(pa_matlab.pulse_energy, pa_python.get_pulse_energy)), 'Error on pulse energy getter')
assert(isempty(setdiff(pa_matlab.measurement_timestamps, pa_python.get_measurement_time_stamps)), 'Error on measurement time stamps getter')
assert(isempty(setdiff(pa_matlab.acquisition_wavelengths, pa_python.get_acquisition_wavelengths)), 'Error on acquisition wavelengths getter')
assert(isempty(setdiff(pa_matlab.time_gain_compensation, pa_python.get_time_gain_compensation)), 'Error on time gain compensation getter')
assert(isempty(setdiff(pa_matlab.overall_gain, pa_python.get_overall_gain)), 'Error on overall gain getter')
assert(isempty(setdiff(pa_matlab.element_dependent_gain, pa_python.get_element_dependent_gain)), 'Error on element dependent gain getter')
assert(isempty(setdiff(pa_matlab.temperature_control, pa_python.get_temperature)), 'Error on temperature getter')
assert(isempty(setdiff(pa_matlab.ad_sampling_rate, pa_python.get_sampling_rate)), 'Error on AD sampling rate getter')
assert(isempty(setdiff(pa_matlab.frequency_domain_filter, pa_python.get_frequency_domain_filter)), 'Error on frequency domain filter getter')
assert(isempty(setdiff(pa_matlab.measurement_spatial_poses, pa_python.get_measurement_spatial_poses)), 'Error on measurement spatial poses getter')
assert(isempty(setdiff(pa_matlab.measurements_per_image, pa_python.get_measurements_per_image)), 'Error on measurements per image getter')


%%- specific to illuminator
assert(isempty(setdiff(pa_matlab.illuminators.illuminator_position,pa_python.get_illuminator_position())), 'Error on illuminator position getter')
assert(isempty(setdiff(pa_matlab.illuminators.illuminator_geometry,pa_python.get_illuminator_geometry())), 'Error on illuminator orientation getter')
assert(isempty(setdiff(pa_matlab.illuminators.illuminator_orientation,pa_python.get_illuminator_orientation())), 'Error on illuminator orientation getter')
assert(isempty(setdiff(pa_matlab.illuminators.wavelength_range,pa_python.get_wavelength_range())), 'Error on wavelength range getter')
assert(isempty(setdiff(cell2mat(pa_matlab.illuminators.illuminator_geometry_type), cell2mat(pa_python.get_illuminator_geometry_type))), 'Error on illuminator geometry type getter')
assert(isempty(setdiff(pa_matlab.illuminators.pulse_width,pa_python.get_pulse_width())), 'Error on pulse width getter')
assert(isempty(setdiff(pa_matlab.illuminators.beam_energy_profile,pa_python.get_beam_energy_profile())), 'Error on beam energy profilegetter')
assert(isempty(setdiff(pa_matlab.illuminators.beam_stability_profile,pa_python.get_beam_stability_profile())), 'Error on beam stability profile getter')
assert(isempty(setdiff(pa_matlab.illuminators.beam_intensity_profile,pa_python.get_beam_profile())), 'Error on beam intensity profile getter')
assert(isempty(setdiff(pa_matlab.illuminators.beam_divergence_angles,pa_python.get_beam_divergence())), 'Error on beam divergence angles getter')
assert(isempty(setdiff(pa_matlab.illuminators.intensity_profile_distance,pa_python.get_beam_profile_distance())), 'Error on beam intensity profile distance getter')


%%- specific to detector
assert(isempty(setdiff(pa_matlab.detector.detector_position,pa_python.get_detector_position())), 'Error on detector position getter');
assert(isempty(setdiff(pa_matlab.detector.detector_orientation,pa_python.get_detector_orientation())), 'Error on detector orientation getter');
assert(isempty(setdiff(pa_matlab.detector.detector_geometry,pa_python.get_detector_geometry())), 'Error on detector geometry getter');
assert(isempty(setdiff(cell2mat(pa_python.get_detector_geometry_type()),cell2mat(pa_python.get_detector_geometry_type))), 'Error on detector geometry type getter');
assert(isempty(setdiff(pa_matlab.detector.frequency_response,pa_python.get_frequency_response())), 'Error on frequency response getter');
assert(isempty(setdiff(pa_matlab.detector.angular_response,pa_python.get_angular_response())), 'Error on angular response getter');


fprintf('\n\nUnit test passed on file %s\n\n', file);
end

function out = compare_struct(s1, s2)
out = 1;
f1 = fieldnames(s1);
f2 = fieldnames(s2);
if (length(f1)~=length(f2))
    out = 0;
else
    for i=1:length(f1)
        try
            out = out * isempty(setdiff(s1.(f1{i}), s2.(f1{i})));
        catch me
            out = 0;
        end
    end
end
out = (out==1);
end

