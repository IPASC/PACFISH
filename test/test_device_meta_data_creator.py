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



import os
from unittest.case import TestCase
from ipasc_tool.core import MetadataTags
from ipasc_tool.core import MetadataDeviceTags
from ipasc_tool.api.DeviceMetaDataCreator import DeviceMetaDataCreator, IlluminationElementCreator
import numpy as np


def create_random_testing_parameters():
    test_float = np.random.random()
    test_list = [np.random.random(), np.random.random(), -np.random.random()]
    test_string = str(np.random.random())
    test_dict = dict()
    test_array = np.random.random((1000,2))
    return {'test_float': test_float, 'test_list': test_list, 'test_string': test_string, 'test_dict': test_dict, 'test_array': test_array}


class DeviceMetaDataCreatorTest(TestCase):

    def setUp(self):
        self.device_dict_creator = DeviceMetaDataCreator()
        
        print("setUp")

    def tearDown(self):
        print("tearDown")
        
    def test_set_general_information(self):
        test_list = create_random_testing_parameters()['test_list']
        test_string = create_random_testing_parameters()['test_string']

        self.device_dict_creator.set_general_information(test_string, test_list)
        device_dict = self.device_dict_creator.finalize_device_meta_data()

        assert device_dict[self.device_dict_creator.GENERAL][MetadataDeviceTags.UUID.info.tag] == test_string
        assert device_dict[self.device_dict_creator.GENERAL][MetadataDeviceTags.FIELD_OF_VIEW.info.tag] == test_list
        
    def test_add_detection_element(self):
        
        test_dict = create_random_testing_parameters()['test_dict']
        self.device_dict_creator.add_detection_element(test_string, test_dict)
        device_dict = self.device_dict_creator.finalize_device_meta_data()
        
        assert device_dict[self.device_dict_creator.GENERAL][MetadataDeviceTags.DETECTORS.info.tag][test_string] == test_dict

    def test_add_illumination_element(self):
        test_dict = create_random_testing_parameters()['test_dict']
        self.device_dict_creator.add_illumination_element(test_string, test_dict)
        device_dict = self.device_dict_creator.finalize_device_meta_data()
        assert device_dict[self.device_dict_creator.GENERAL][MetadataDeviceTags.ILLUMINATORS.info.tag][test_string] == test_dict

        os.remove(self.device_dict_creator.save_file_name)


class IlluminationElementCreatorTest(TestCase):

    def setUp(self):
        self.illuminator_creator = IlluminationElementCreator()
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_set_illuminator_position(self):
        test_list = create_random_testing_parameters()['test_list']
        self.illuminator_creator.set_illuminator_position(test_list)
        illumination_dict = self.illuminator_creator.get_dictionary()
        assert illumination_dict[MetadataDeviceTags.ILLUMINATOR_POSITION.info.tag] == test_list

    def test_set_illuminator_shape(self):
        test_array = create_random_testing_parameters()['test_array']
        self.illuminator_creator.set_illuminator_shape(test_array)
        illumination_dict = self.illuminator_creator.get_dictionary()
        assert illumination_dict[MetadataDeviceTags.ILLUMINATOR_SHAPE.info.tag] == test_array

    def test_set_wavelength_range(self):
        test_list = create_random_testing_parameters()['test_list']
        self.illuminator_creator.set_wavelength_range(test_list)
        illumination_dict = self.illuminator_creator.get_dictionary()
        assert illumination_dict[MetadataDeviceTags.WAVELENGTH_RANGE.info.tag] == test_list
    
    def test_set_laser_energy_profile(self):
        test_array = create_random_testing_parameters()['test_array']
        self.illuminator_creator.set_laser_energy(test_array)
        illumination_dict = self.illuminator_creator.get_dictionary()
        assert illumination_dict[MetadataDeviceTags.LASER_ENERGY_PROFILE.info.tag] == test_array
    
    def test_set_laser_stability_profile(self):
        test_array = create_random_testing_parameters()['test_array']
        self.illuminator_creator.set_illuminator_shape(test_array)
        illumination_dict = self.laser_stability.get_dictionary()
        assert illumination_dict[MetadataDeviceTags.LASER_STABILTY_PROFILE.info.tag] == test_array
    
    def test_set_pulse_width(self):    
        test_list = create_random_testing_parameters()['test_list']
        self.illuminator_creator.set_pulse_width(test_list)
        illumination_dict = self.illuminator_creator.get_dictionary()
        assert illumination_dict[MetadataDeviceTags.PULSE_WIDTH.info.tag] == test_list 

    def test_set_beam_intensity_profile(self):
        test_array = create_random_testing_parameters()['test_array']
        self.illuminator_creator.set_beam_intensity_profile(test_array)
        illumination_dict = self.illuminator_creator.get_dictionary()
        assert illumination_dict[MetadataDeviceTags.BEAM_INTENSITY_PROFILE.info.tag] == test_array
    
    def test_set_beam_divergence_angles(self):
        test_float = create_random_testing_parameters()['test_float']
        self.illuminator_creator.set_beam_divergence_angle(test_float)
        illumination_dict = self.illuminator_creator.get_dictionary()
        assert illumination_dict[MetadataDeviceTags.BEAM_DIVERGENCE_ANGLES.info.tag] == test_float
        os.remove(self.illuminator_creator.save_file_name)



class DetectionElementCreatorTest(TestCase):

    def setUp(self):
        self.detection_creator = DetectionElementCreator()
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_set_detector_position(self):
        test_list = create_random_testing_parameters()['test_list']
        self.detection_creator.set_detector_position(test_list)
        detection_dict = self.detection_creator.get_dictionary()
        assert detection_dict[MetadataDeviceTags.DETECTOR_POSITION.info.tag]  == test_list


    def test_set_detector_orientation(self):
        test_list = create_random_testing_parameters()['test_list']
        self.detection_creator.set_detector_orientation(test_list)
        detection_dict = self.detection_creator.get_dictionary()
        assert detection_dict[MetadataDeviceTags.DETECTOR_ORIENTATION.info.tag]  == test_list


    def test_set_detector_size(self):
        test_list = create_random_testing_parameters()['test_list']
        self.detection_creator.set_detector_size(test_list)
        detection_dict = self.detection_creator.get_dictionary()
        assert detection_dict[MetadataDeviceTags.DETECTOR_SIZE.info.tag]  == test_list
            

    def test_frequency_response(self):
        test_array = create_random_testing_parameters()['test_array']
        self.detection_creator.set_frequency_reponse(test_array)
        detection_dict = self.detection_creator.get_dictionary()
        assert detection_dict[MetadataDeviceTags.FREQUENCY_RESPONSE.info.tag]  == test_array


    def test_set_angular_response(self):
        test_array = create_random_testing_parameters()['test_array']
        self.detection_creator.set_angular_response(test_array)
        detection_dict = self.detection_creator.get_dictionary()
        assert detection_dict[MetadataDeviceTags.ANGULAR_RESPONSE.info.tag]  == test_array


        os.remove(self.detection_creator.save_file_name)

