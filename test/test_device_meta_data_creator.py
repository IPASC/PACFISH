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
from ipasc_tool.api import DeviceMetaDataCreator
import numpy as np


def create_random_testing_parameters():
    test_float = np.random.random()
    test_list = [(np.random.random(), np.random.random(); -np.random.random())]
    test_string = str(np.random())
    test_dict = dict()
    return {'test_float': test_float, 'test_list': test_list ,'test_string': test_string,'test_dict': test_dict}'


class DeviceMetaDataCreatorTest(TestCase):

    def setUp(self):
        self.device_dict_creator = DeviceMetaDataCreator()
        
        print("setUp")

    def tearDown(self):
        print("tearDown")
        
        
    def test_set_general_information(self): 
        test_list=create_random_testing_parameters()['test_list']
        test_string=create_random_testing_parameters()['test_string']
        
        
        self.device_dict_creator.set_general_information(test_string,test_list)
        device_dict=self.device_dict_creator
        assert device_dict[MetadataDeviceTags.GENERAL.info.tag]['UUID'] == test_string
        assert device_dict[MetadataDeviceTags.GENERAL.info.tag]['field_of_view'] == test_list

    def test_add_detection_element(self):
        test_dict=create_random_testing_parameters()['test_dict']
        
        add_detection_element(self.device_dict, test_string, test_dict)
        assert device_dict[MetadataDeviceTags.DETECTORS.info.tag][test_string] == test_dict
        
    def test_add_illumination_element(self):   
        test_dict=create_random_testing_parameters()['test_dict']
        
        add_illumination_element(self.device_dict, test_string, test_dict)
        assert device_dict[MetadataDeviceTags.ILLUMINATORS.info.tag][test_string] == test_dict
        
    def test_finalize_device_meta_data(self):
        
        assert self.detection_element_dict.finalize_device_meta_data(device_dict)
        
        os.remove(self.device_dict.save_file_name)
        

    
class IlluminationElementCreatorTest(TestCase):

    def setUp(self):
        self.illuminator_element_dict = IlluminationElementCreator()
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_set_illuminator_position(self):
        test_list=create_random_testing_parameters()['test_list']
        assert self.illuminator_element_dict.set_illuminator_position(self.illuminator_element_dict,test_list) == test_list
            
    def test_set_illuminator_shape(self):
        test_list=create_random_testing_parameters()['test_list']
        assert self.illuminator_element_dict.set_illuminator_shape(self.illuminator_element_dict,test_list) == test_list
        
            
    def test_set_wavelength_range(self):
        test_list=create_random_testing_parameters()['test_list']
        assert self.illuminator_element_dict.set_wavelength_range(self.illuminator_element_dict, test_list)== test_list
       
    def test_set_laser_energy_profile(self):
        test_list=create_random_testing_parameters()['test_list']
        assert self.illuminator_element_dict.set_laser_energy_profile(self.illuminator_element_dict,test_list)== test_list
        
    def test_set_laser_stability_profile(self):
        test_list=create_random_testing_parameters()['test_list']
        assert self.illuminator_element_dict.set_laser_stability_profile(self.illuminator_element_dict, test_list)== test_list
        
            
    def test_set_pulse_width(self):
        test_list=create_random_testing_parameters()['test_list']
        assert self.illuminator_element_dict.set_pulse_width(self.illuminator_element_dict,test_list)== test_list
        
            
    def test_set_beam_intensity_profile(self):
        test_float=create_random_testing_parameters()['test_float']
        assert self.illuminator_element_dict.set_beam_intensity_profile(self.illuminator_element_dict,test_float)== test_float
        
            
    def test_set_beam_divergence_angles(self):
        test_float=create_random_testing_parameters()['test_float']
        assert self.illuminator_element_dict.set_beam_divergence_angles(self.illuminator_element_dict,test_float)== test_float
        
            
    def test_get_dictionary(self):
        assert get_dictionary() ==
    
        os.remove(self.illuminator_element_dict.save_file_name)
          
        
        
class DetectionElementCreatorTest(TestCase):

    def setUp(self):
        self.detection_element_dict = DetectionElementCreator()
        print("setUp")

    def tearDown(self):
        print("tearDown")
            
    def test_set_detector_position(self):
        test_list=create_random_testing_parameters()['test_list']
        assert self.detection_element_dict.set_detector_position(self.detection_element_dict,test_list) == test_list
        
            
    def test_set_detector_orientation(self):
        test_list=create_random_testing_parameters()['test_list']
        assert self.detection_element_dict.set_detector_orientation(self.detection_element_dict,test_list) == test_list
        

    def test_set_detector_size(self):
        test_list=create_random_testing_parameters()['test_list']
        assert self.detection_element_dict.set_detector_size(self.detection_element_dict,test_list) == test_list
        
    
    def test_frequency_response(self):
        test_list=create_random_testing_parameters()['test_list']
        assert self.detection_element_dict.set_frequency_response(self.detection_element_dict,test_list) == test_list
        
 
    def test_set_angular_response(self):
        test_list=create_random_testing_parameters()['test_list']
        assert self.detection_element_dict.set_angular_response(self.detection_element_dict, test_list) == test_list
        
    def test_get_dictionary(self):
        
        assert get_dictionary()
        
        os.remove(self.detection_element_dict.save_file_name)
