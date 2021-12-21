# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-License-Identifier: BSD 3-Clause License

from unittest.case import TestCase
from pacfish import PAData
from testing.unit_tests.utils import create_complete_device_metadata_dictionary, create_complete_acquisition_meta_data_dictionary
import numpy as np


class MetaDataTest(TestCase):

    def setUp(self):
        self.acquisition_metadata = create_complete_acquisition_meta_data_dictionary()
        self.device_metadata = create_complete_device_metadata_dictionary()
        self.pa_data = PAData(binary_time_series_data=np.random.random((4, 200)),
                              meta_data_acquisition=self.acquisition_metadata,
                              meta_data_device=self.device_metadata)
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_get_general_information(self):
        assert self.pa_data.get_device_uuid() is not None
        assert self.pa_data.get_field_of_view() is not None
        assert self.pa_data.get_number_of_detectors() is not None
        assert self.pa_data.get_number_of_illuminators() is not None

    def test_get_illuminator_position(self):
        assert self.pa_data.get_illuminator_position() is not None
        assert self.pa_data.get_illuminator_position(list(self.pa_data.get_illuminator_ids())[0]) is not None
        assert self.pa_data.get_illuminator_position(0) is not None

    def test_get_illuminator_orientation(self):
        assert self.pa_data.get_illuminator_orientation() is not None
        assert self.pa_data.get_illuminator_orientation(list(self.pa_data.get_illuminator_ids())[0]) is not None
        assert self.pa_data.get_illuminator_orientation(0) is not None

    def test_get_illuminator_size(self):
        assert self.pa_data.get_illuminator_geometry() is not None
        assert self.pa_data.get_illuminator_geometry(list(self.pa_data.get_illuminator_ids())[0]) is not None
        assert self.pa_data.get_illuminator_geometry(0) is not None

    def test_get_wavelength_range(self):
        assert self.pa_data.get_wavelength_range() is not None
        assert self.pa_data.get_wavelength_range(list(self.pa_data.get_illuminator_ids())[0]) is not None
        assert self.pa_data.get_wavelength_range(0) is not None

    def test_get_energy_profile(self):
        assert self.pa_data.get_beam_energy_profile() is not None
        assert self.pa_data.get_beam_energy_profile(list(self.pa_data.get_illuminator_ids())[0]) is not None
        assert self.pa_data.get_beam_energy_profile(0) is not None

    def test_get_stability_profile(self):
        assert self.pa_data.get_beam_stability_profile() is not None
        assert self.pa_data.get_beam_stability_profile(list(self.pa_data.get_illuminator_ids())[0]) is not None
        assert self.pa_data.get_beam_stability_profile(0) is not None

    def test_get_pulse_duration(self):
        assert self.pa_data.get_pulse_width() is not None
        assert self.pa_data.get_pulse_width(list(self.pa_data.get_illuminator_ids())[0]) is not None
        assert self.pa_data.get_pulse_width(0) is not None

    def test_get_beam_intensity_profile(self):
        assert self.pa_data.get_beam_profile() is not None
        assert self.pa_data.get_beam_profile(list(self.pa_data.get_illuminator_ids())[0]) is not None
        assert self.pa_data.get_beam_profile(0) is not None

    def test_get_beam_divergence_angles(self):
        assert self.pa_data.get_beam_divergence() is not None
        assert self.pa_data.get_beam_divergence(list(self.pa_data.get_illuminator_ids())[0]) is not None
        assert self.pa_data.get_beam_divergence(0) is not None

    def test_get_detector_position(self):
        assert self.pa_data.get_detector_position() is not None
        assert self.pa_data.get_detector_position(list(self.pa_data.get_detector_ids())[0]) is not None
        assert self.pa_data.get_detector_position(0) is not None

    def test_get_detector_orientation(self):
        assert self.pa_data.get_detector_orientation() is not None
        assert self.pa_data.get_detector_orientation(list(self.pa_data.get_detector_ids())[0]) is not None
        assert self.pa_data.get_detector_orientation(0) is not None

    def test_get_detector_geomtery(self):
        assert self.pa_data.get_detector_geometry() is not None
        assert self.pa_data.get_detector_geometry(list(self.pa_data.get_detector_ids())[0]) is not None
        assert self.pa_data.get_detector_geometry(0) is not None

    def test_get_frequency_response(self):
        assert self.pa_data.get_frequency_response() is not None
        assert self.pa_data.get_frequency_response(list(self.pa_data.get_detector_ids())[0]) is not None
        assert self.pa_data.get_frequency_response(0) is not None

    def test_get_angular_response(self):
        assert self.pa_data.get_angular_response() is not None
        assert self.pa_data.get_angular_response(list(self.pa_data.get_detector_ids())[0]) is not None
        assert self.pa_data.get_angular_response(0) is not None

    def test_aquisition_metadata(self):
        assert self.pa_data.get_encoding() is not None
        assert self.pa_data.get_compression() is not None
        assert self.pa_data.get_data_UUID() is not None
        assert self.pa_data.get_data_type() is not None
        assert self.pa_data.get_dimensionality() is not None
        assert self.pa_data.get_sizes() is not None
        assert self.pa_data.get_photoacoustic_imaging_device_reference() is not None
        assert self.pa_data.get_pulse_energy() is not None
        assert self.pa_data.get_measurement_time_stamps() is not None
        assert self.pa_data.get_acquisition_wavelengths() is not None
        assert self.pa_data.get_time_gain_compensation() is not None
        assert self.pa_data.get_overall_gain() is not None
        assert self.pa_data.get_element_dependent_gain() is not None
        assert self.pa_data.get_temperature() is not None
        assert self.pa_data.get_acoustic_coupling_agent() is not None
        assert self.pa_data.get_scanning_method() is not None
        assert self.pa_data.get_sampling_rate() is not None
        assert self.pa_data.get_frequency_domain_filter() is not None
        assert self.pa_data.get_measurement_spatial_poses() is not None
        assert self.pa_data.get_measurements_per_image() is not None
