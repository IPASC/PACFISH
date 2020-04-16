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

# display method update

from core.metadata_tags import MetadataTags.names

class DeviceMetaDataCreator():
    def __init__(self):
        self.device_dict = {'general':{},'illuminators':{},'detectors':{}} 

    def set_general_information(self,UUID:int,x1,x2,x3)
        self.device_dict['general']['UUID']=UUID
        self.device_dict['general']['field_of_view']=[x1,x2,x3]
        
        class IlluminationElementCreator()
            def __init__(self, ID):
                self.device_dict['illuminators']['illumination_element']={}

            def add_illuminator_position(self,ID, x1,x2,x3):
                self.device_dict['illuminators']['illuminator_position']=[x1,x2,x3]

            def add_illuminator_orientation(self,ID, r1,r2,r3):
                self.device_dict['illuminators']['illuminator_orientation']=[r1,r2,r3]

            def add_illuminator_shape(self,ID,val):
                self.device_dict['illuminators']['illuminator_shape']=val

            def add_wavelength_range(self,ID, lamda_min, lamda_max, lamda_accuracy):
                self.device_dict['illuminators']['wavelength_range']=[lamda_min, lamda_max, lamda_accuracy]

            def add_laser_energy_profile(self,ID,val):
                self.device_dict['illuminators']['laser_energy_profile']=val

            def add_laser_stability_profile(self,ID,val):
                self.device_dict['illuminators']['laser_stability_profile']=val

            def add_pulse_width(self,ID,val):
                self.device_dict['illuminators']['pulse_width']=val

            def add_beam_intensity_profile(self,ID,val):
                self.device_dict['illuminators']['beam_intensity_profile']=val

            def add_beam_divergence_angles(self,ID,val):
                self.device_dict['illuminators']['beam_divergence_angles']=val
                
        class DetectionElementCreator()
            def __init__(self):
                self.device_dict['detectors']['detection_element']={}

            def add_detector_position(self,ID,x1,x2,x3):
                self.device_dict['detectors']['detector_position']=[x1,x2,x3]

            def add_detector_orientation(self,ID,r1,r2,r3):
                self.device_dict['detectors']['detector_orientation']=[r1,r2,r3]

            def add_detector_size(self,ID,x1,x2,x3):
                self.device_dict['detectors']['detector_size']=[x1,x2,x3]

            def add_frequency_response(self,ID,val):
                self.device_dict['detectors']['frequency_response']=val

            def add_angular_response(self,ID,val):
                self.device_dict['detectors']['angular_response']=val
                                 
#display dictionary, number of detectors, number of illuminators
    def display(self):
        return self.device_dict, len(self.device_dict['detectors']), len(self.device_dict['illuminators'])
