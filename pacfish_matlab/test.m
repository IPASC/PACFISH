% % test perso
clear
% [a1, b1, c1] = load_data('test_input2.hdf5');
% pa = pa_data(a1, b1, c1);
% 
% % tenter de convertir tous les char en uint8 ?
% 
% write_data('test_output.hdf5', pa, 1);
% 
% [a2, b2, c2] = load_data('test_output.hdf5');
% 
% 
%% test egality
% out1 = check_egality(b1, b2);
% out2 = check_egality(c1, c2);
% fprintf("\n\n\nResultat de la comparaison : %d %d\n", out1, out2);
% 

% p1=c1.illuminators.deleteme0000000000.illuminator_geometry_type;
% p2=c2.illuminators.deleteme0000000000.illuminator_geometry_type;
% whos p1 p2
% p1-p2


%%
pa1 = pa_data('test_input.hdf5');
% pa1.save_data('test_output.hdf5', 1);
% pa2 = pa_data('test_output.hdf5');
% 
% %% check if the data contain the same values
% out1 = check_egality(pa1.meta_data,         pa2.meta_data);
% out2 = check_egality(pa1.meta_data_device,  pa2.meta_data_device);
% fprintf("\n\n\nResult of the conversion (with string converts to char): %d %d\n", out1, out2);


%% test des getters
disp('New try');

%%- general getters
ids_illu = pa1.get_illuminator_ids;
ids_dete = pa1.get_detector_ids;
% pa1.get_custom_meta_datum('speed_of_sound')
% pa1.get_acquisition_meta_datum('speed_of_sound')
% pa1.get_device_uuid
% pa1.get_field_of_view
% pa1.get_number_of_illuminators
% pa1.get_number_of_detectors
% pa1.get_regions_of_interest

%%- specific to illuminator
% pa1.get_illuminator_position(ids_illu)
% pa1.get_illuminator_orientation(ids_illu)
% pa1.get_illuminator_geometry(ids_illu)
% pa1.get_illuminator_geometry_type(ids_illu)
% pa1.get_wavelength_range(ids_illu)
% pa1.get_beam_energy_profile(ids_illu)
% pa1.get_beam_stability_profile(ids_illu)
% pa1.get_pulse_width(ids_illu)
% pa1.get_beam_profile(ids_illu)
% pa1.get_beam_profile_distance(ids_illu)
% pa1.get_beam_divergence(ids_illu)

%%- specific to detector
% pa1.get_detector_position(ids_dete)
% pa1.get_detector_orientation(ids_dete)
% pa1.get_detector_geometry(ids_dete)
% pa1.get_detector_geometry_type(ids_dete)
% pa1.get_frequency_response(ids_dete)
% pa1.get_angular_response(ids_dete)

%%- others
% pa1.get_encoding
% pa1.get_compression
% pa1.get_data_UUID
% pa1.get_data_type
% pa1.get_dimensionality
% pa1.get_sizes
% pa1.get_photoacoustic_imaging_device_reference
% pa1.get_pulse_energy
% pa1.get_measurement_time_stamps
% pa1.get_acquisition_wavelengths
% pa1.get_time_gain_compensation
% pa1.get_overall_gain
% pa1.get_element_dependent_gain
% pa1.get_temperature
% pa1.get_acoustic_coupling_agent
% pa1.get_speed_of_sound
% pa1.get_scanning_method
% pa1.get_sampling_rate
% pa1.get_frequency_domain_filter
% pa1.get_measurement_spatial_poses
% pa1.get_measurements_per_image

