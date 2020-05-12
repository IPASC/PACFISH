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

from core.metadata_tags import MetadataDeviceTags
import copy


class IlluminationElementCreator(object):
    def __init__(self):
        self.illuminator_element_dict = dict()

    def set_illuminator_position(self, illuminator_position:list):
         """
        :param illuminator_position: is a list of three float values that describe the position of the illumination element in the
                    x1, x2, and x3 direction.
                    The units can be found in MetadataDeviceTags.ILLUMINATOR_POSITION.info.unit.
        :return: void
        """
        self.illuminator_element_dict[MetadataDeviceTags.ILLUMINATOR_POSITION.info.tag] = illuminator_position

    def set_illuminator_orientation(self, orientation:list):
        """
        :param orientation: is a list of three float values that describe the orientation of the illumination element in the
                    x1, x2, and x3 direction.
                    The units can be found in MetadataDeviceTags.ILLUMINATOR_ORIENTATION.info.unit.
        :return: void
        """
        self.illuminator_element_dict[MetadataDeviceTags.ILLUMINATOR_ORIENTATION.info.tag] = orientation

    def set_illuminator_shape(self, shape:list):
        """
        :param shape: is a list of three float values that describe the shape of the illuminator in the
                    x1, x2, and x3 direction.
                    The units can be found in MetadataDeviceTags.ILLUMINATOR_SHAPE.info.unit.
        :return: void
        """
        self.illuminator_element_dict[MetadataDeviceTags.ILLUMINATOR_SHAPE.info.tag] = shape

    def set_wavelength_range(self, wl_range:list):
        """
        :param wl_range: is a list of three float values that describe the minimum wavelength lambda_min, 
        the maximum wavelength lambda_max and a metric for the accuracy lambda_accuracy.
        The units can be found in MetadataDeviceTags.WAVELENGTH_RANGE.info.unit.
        :return: void
        """
        self.illuminator_element_dict[MetadataDeviceTags.WAVELENGTH_RANGE.info.tag] = wl_range

    def set_laser_energy_profile(self, energy_profile:list):
        """
        :param enery_profile: a two element list [wavelengths, laser_energy] describing the laser energy profile.
                    Laser energy and wavelengths are also lists where len(laser_energy) == len(profile)
                    The units can be found in MetadataDeviceTags.LASER_ENERGY_PROFILE.info.unit.
        :return: void
        """
        self.illuminator_element_dict[MetadataDeviceTags.LASER_ENERGY_PROFILE.info.tag] = energy_profile
        

    def set_laser_stability_profile(self, stability_profile:list):
         """
        :param stability_profile: a two element list [wavelengths,laser_stability,] describing the laser stability profile.
                    Laser stability and wavelengths are also lists where len(stability_profile) == len(wavelengths).
                    The units can be found in MetadataDeviceTags.LASER_STABILITY_PROFILE.info.unit.
        :return: void
        """
        self.illuminator_element_dict[MetadataDeviceTags.LASER_STABILITY_PROFILE.info.tag] = stability_profile

    def set_pulse_width(self, pulse_width:float):
        """
        :param pulse_width: a floating point value describing the pulse width of the laser 
                    in the units of MetadataDeviceTags.PULSE_WIDTH.info.unit.
        :return: void
        """
        self.illuminator_element_dict[MetadataDeviceTags.PULSE_WIDTH.info.tag] = pulse_width

    def set_beam_intensity_profile(self, intensity_profile:list):
         """
        :param intensity_profile: a two element list [wavelengths, intensity_profile] describing the beam itensity profile.
                    Wavelengths and intensity_profile are also lists where len(wavelengths) == len(intensity_profile)
                    The units can be found in MetadataDeviceTags.BEAM_INTENSITY_PROFILE.info.unit.
        :return: void
        """
        self.illuminator_element_dict[MetadataDeviceTags.BEAM_INTENSITY_PROFILE.info.tag] = intensity_profile

    def set_beam_divergence_angles(self, angle:float):
        """
        :param angle: a value describing the opening angle of the laser beam from the illuminator shape with respect 
                    to the orientation vector. This angle is represented by the standard deviation of the beam divergence.
                    The units can be found in MetadataDeviceTags.BEAM_DIVERGENCE_ANGLES.info.unit.
                    
        :return: void
        """
        self.illuminator_element_dict[MetadataDeviceTags.BEAM_DIVERGENCE_ANGLES.info.tag] = angle

    def get_dictionary(self):
        return copy.deepcopy(self.illuminator_element_dict)


class DetectionElementCreator(object):
    def __init__(self):
        self.detection_element_dict = dict()

    def set_detector_position(self, detector_position:list):
         """
        :param detector_position: a list of three float values that describe the position of the detection element in the
                    x1, x2, and x3 direction.
                    The units can be found in MetadataDeviceTags.DETECTOR_POSITION.info.unit.
        :return: void
        """
        self.detection_element_dict[MetadataDeviceTags.DETECTOR_POSITION.info.tag] = detector_position

    def set_detector_orientation(self, orientation:list):
        """
        :param orientation: a list of three float values that describe the orientation of the detector element in the
                    x1, x2, and x3 direction.
                    The units can be found in MetadataDeviceTags.DETECTOR_ORIENTATION.info.unit.
        :return: void
        """
        self.detection_element_dict[MetadataDeviceTags.DETECTOR_ORIENTATION.info.tag] = orientation

    def set_detector_size(self, size:list):
         """
        :param size: a three element list [x1, x2, x3] describing the extent of the detector size in x1, x2, and x3 direction.
                    The units can be found in MetadataDeviceTags.DETECTOR_SIZE.info.unit.
        :return: void
        """
        self.detection_element_dict[MetadataDeviceTags.DETECTOR_SIZE.info.tag] = size

    def set_frequency_response(self, frequency_response:list):
        """
        :param frequency_response: a two element list [frequency, response] describing the frequency response of the detector.
                    Frequency and response are also lists where len(frequency) == len(response).
                    The units can be found in MetadataDeviceTags.FREQUENCY_RESPONSE.info.unit.
        :return: void
        """
        self.detection_element_dict[MetadataDeviceTags.FREQUENCY_RESPONSE.info.tag] = frequency_response

    def set_angular_response(self, angular_response: list):
        """
        :param angular_response: a two element list [angles, response] describing the angular response of the detecor.
                    Angles and response are also lists where len(angles) == len(response).
                    The units can be found in MetadataDeviceTags.ANGULAR_RESPONSE.info.unit.
        :return: void
        """
        self.detection_element_dict[MetadataDeviceTags.ANGULAR_RESPONSE.info.tag] = angular_response

    def get_dictionary(self):
        return copy.deepcopy(self.detection_element_dict)


class DeviceMetaDataCreator(object):
    def __init__(self):
        self.device_dict = dict()
        self.device_dict['general'] = dict()
        self.device_dict['illuminators'] = dict()
        self.device_dict['detectors'] = dict()

    def set_general_information(self, uuid: str, fov: list):
        """
        :param uuid: is a string that uniquely identifies the photoacoustic device
        :param fov: is a list of three float values that describe the extent of the field of view of the device in the
                    x1, x2, and x3 direction (x1, x2, x3 is defined in TODO).
        :return: void
        """
        self.device_dict['general']['UUID'] = uuid
        self.device_dict['general']['field_of_view'] = fov

    def add_detection_element(self, uid: str, detection_element: dict):
         """
        :param uid: is a string that uniquely identifies the detection element
        :param detection_element: is a dictionary for the detection element specific parameters
        :return: void
        """
        self.device_dict['detectors'][uid] = detection_element

    def add_illumination_element(self, uid: str, illumination_element: dict):
        """
        :param uid: is a string that uniquely identifies the illumination element
        :param illumination_element: is a dictionary for the illumination element specific parameters
        :return: void
        """
        self.device_dict['illuminators'][uid] = illumination_element

    def finalize_device_meta_data(self):

        self.device_dict['general'][MetadataDeviceTags.NUMBER_OF_DETECTORS.info.tag] = len(
            self.device_dict['detectors'])
        self.device_dict['general'][MetadataDeviceTags.NUMBER_OF_ILLUMINATORS.info.tag] = len(
            self.device_dict['illuminators'])

        return copy.deepcopy(self.device_dict)
