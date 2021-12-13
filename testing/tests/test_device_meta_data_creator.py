# BSD 3-Clause License
#
# Copyright (c) 2020, IPASC
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


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

        assert device_dict[self.device_dict_creator.GENERAL][MetadataDeviceTags.UUID.tag] == test_string
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
        assert (illumination_dict[MetadataDeviceTags.LASER_ENERGY_PROFILE.tag] == test_array).all()
    
    def test_set_laser_stability_profile(self):
        test_array = create_random_testing_parameters()['test_array']
        self.illuminator_creator.set_laser_stability_profile(test_array)
        illumination_dict = self.illuminator_creator.get_dictionary()
        assert (illumination_dict[MetadataDeviceTags.LASER_STABILITY_PROFILE.tag] == test_array).all()
    
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
