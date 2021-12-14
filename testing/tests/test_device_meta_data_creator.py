"""
SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
SPDX-License-Identifier: BSD 3-Clause License
"""

from unittest.case import TestCase
from pacfish import MetadataDeviceTags
from pacfish import DeviceMetaDataCreator, IlluminationElementCreator, DetectionElementCreator
from testing.tests.utils import create_random_testing_parameters


class DeviceMetaDataCreatorTest(TestCase):

    def setUp(self):
        self.device_dict_creator = DeviceMetaDataCreator()
        
        print("setUp")

    def tearDown(self):
        print("tearDown")
        
    def test_set_general_information(self):
        test_array = create_random_testing_parameters()['test_array']
        test_string = create_random_testing_parameters()['test_string']

        self.device_dict_creator.set_general_information(test_string, test_array)
        device_dict = self.device_dict_creator.finalize_device_meta_data()

        assert device_dict[self.device_dict_creator.GENERAL][MetadataDeviceTags.UNIQUE_IDENTIFIER.tag] == test_string
        assert (device_dict[self.device_dict_creator.GENERAL][MetadataDeviceTags.FIELD_OF_VIEW.tag] == test_array).all()
        
    def test_add_detection_element(self):
        
        test_dict = create_random_testing_parameters()['test_dict']

        self.device_dict_creator.add_detection_element(test_dict)
        device_dict = self.device_dict_creator.finalize_device_meta_data()

        for key in device_dict[self.device_dict_creator.DETECTORS]:
            assert device_dict[self.device_dict_creator.DETECTORS][key] == test_dict

    def test_add_illumination_element(self):
        test_dict = create_random_testing_parameters()['test_dict']

        self.device_dict_creator.add_illumination_element(test_dict)
        device_dict = self.device_dict_creator.finalize_device_meta_data()
        for key in device_dict[self.device_dict_creator.ILLUMINATORS]:
            assert device_dict[self.device_dict_creator.ILLUMINATORS][key] == test_dict


class IlluminationElementCreatorTest(TestCase):

    def setUp(self):
        self.illuminator_creator = IlluminationElementCreator()
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_set_illuminator_position(self):
        test_array = create_random_testing_parameters()['test_array']
        self.illuminator_creator.set_illuminator_position(test_array)
        illumination_dict = self.illuminator_creator.get_dictionary()
        assert (illumination_dict[MetadataDeviceTags.ILLUMINATOR_POSITION.tag] == test_array).all()

    def test_set_illuminator_shape(self):
        test_array = create_random_testing_parameters()['test_array']
        self.illuminator_creator.set_illuminator_geometry(test_array)
        illumination_dict = self.illuminator_creator.get_dictionary()
        assert (illumination_dict[MetadataDeviceTags.ILLUMINATOR_GEOMETRY.tag] == test_array).all()

    def test_set_wavelength_range(self):
        test_array = create_random_testing_parameters()['test_array']
        self.illuminator_creator.set_wavelength_range(test_array)
        illumination_dict = self.illuminator_creator.get_dictionary()
        assert (illumination_dict[MetadataDeviceTags.WAVELENGTH_RANGE.tag] == test_array).all()
    
    def test_set_laser_energy_profile(self):
        test_array = create_random_testing_parameters()['test_array']
        self.illuminator_creator.set_laser_energy_profile(test_array)
        illumination_dict = self.illuminator_creator.get_dictionary()
        assert (illumination_dict[MetadataDeviceTags.BEAM_ENERGY_PROFILE.tag] == test_array).all()
    
    def test_set_laser_stability_profile(self):
        test_array = create_random_testing_parameters()['test_array']
        self.illuminator_creator.set_laser_stability_profile(test_array)
        illumination_dict = self.illuminator_creator.get_dictionary()
        assert (illumination_dict[MetadataDeviceTags.BEAM_STABILITY_PROFILE.tag] == test_array).all()
    
    def test_set_pulse_width(self):    
        test_array = create_random_testing_parameters()['test_array']
        self.illuminator_creator.set_pulse_width(test_array)
        illumination_dict = self.illuminator_creator.get_dictionary()
        assert (illumination_dict[MetadataDeviceTags.PULSE_WIDTH.tag] == test_array).all()

    def test_set_beam_intensity_profile(self):
        test_array = create_random_testing_parameters()['test_array']
        self.illuminator_creator.set_beam_intensity_profile(test_array)
        illumination_dict = self.illuminator_creator.get_dictionary()
        assert (illumination_dict[MetadataDeviceTags.BEAM_INTENSITY_PROFILE.tag] == test_array).all()
    
    def test_set_beam_divergence_angles(self):
        test_float = create_random_testing_parameters()['test_float']
        self.illuminator_creator.set_beam_divergence_angles(test_float)
        illumination_dict = self.illuminator_creator.get_dictionary()
        assert illumination_dict[MetadataDeviceTags.BEAM_DIVERGENCE_ANGLES.tag] == test_float


class DetectionElementCreatorTest(TestCase):

    def setUp(self):
        self.detection_creator = DetectionElementCreator()
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_set_detector_position(self):
        test_array = create_random_testing_parameters()['test_array']
        self.detection_creator.set_detector_position(test_array)
        detection_dict = self.detection_creator.get_dictionary()
        assert (detection_dict[MetadataDeviceTags.DETECTOR_POSITION.tag] == test_array).all()

    def test_set_detector_orientation(self):
        test_array = create_random_testing_parameters()['test_array']
        self.detection_creator.set_detector_orientation(test_array)
        detection_dict = self.detection_creator.get_dictionary()
        assert (detection_dict[MetadataDeviceTags.DETECTOR_ORIENTATION.tag] == test_array).all()

    def test_set_detector_size(self):
        test_array = create_random_testing_parameters()['test_array']
        self.detection_creator.set_detector_geometry(test_array)
        detection_dict = self.detection_creator.get_dictionary()
        assert (detection_dict[MetadataDeviceTags.DETECTOR_GEOMETRY.tag] == test_array).all()

    def test_frequency_response(self):
        test_array = create_random_testing_parameters()['test_array']
        self.detection_creator.set_frequency_response(test_array)
        detection_dict = self.detection_creator.get_dictionary()
        assert (detection_dict[MetadataDeviceTags.FREQUENCY_RESPONSE.tag] == test_array).all()

    def test_set_angular_response(self):
        test_array = create_random_testing_parameters()['test_array']
        self.detection_creator.set_angular_response(test_array)
        detection_dict = self.detection_creator.get_dictionary()
        assert (detection_dict[MetadataDeviceTags.ANGULAR_RESPONSE.tag] == test_array).all()
