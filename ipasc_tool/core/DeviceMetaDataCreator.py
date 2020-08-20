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

from ipasc_tool.core import MetadataDeviceTags
import copy
import numpy as np

class IlluminationElementCreator(object):
    def __init__(self):
        self.illuminator_element_dict = dict()

    def set_illuminator_position(self, illuminator_position: np.ndarray):
        """
        :param illuminator_position: is an array of three float values that describe the position of the illumination element in the
                    x1, x2, and x3 direction.
                    The units can be found in MetadataDeviceTags.ILLUMINATOR_POSITION.unit.
        :return: void
        """
        self.illuminator_element_dict[MetadataDeviceTags.ILLUMINATOR_POSITION.tag] = illuminator_position

    def set_illuminator_orientation(self, orientation: np.ndarray):
        """
        :param orientation: is an array of three float values that describe the orientation of the illumination element in the
                    x1, x2, and x3 direction.
                    The units can be found in MetadataDeviceTags.ILLUMINATOR_ORIENTATION.unit.
        :return: void
        """
        self.illuminator_element_dict[MetadataDeviceTags.ILLUMINATOR_ORIENTATION.tag] = orientation

    def set_illuminator_shape(self, shape: np.ndarray):
        """
        :param shape: is an array of three float values that describe the shape of the illuminator in the
                    x1, x2, and x3 direction.
                    The units can be found in MetadataDeviceTags.ILLUMINATOR_SHAPE.unit.
        :return: void
        """
        self.illuminator_element_dict[MetadataDeviceTags.ILLUMINATOR_SHAPE.tag] = shape

    def set_wavelength_range(self, wl_range: np.ndarray):
        """
        :param wl_range: is an array of three float values that describe the minimum wavelength lambda_min,
        the maximum wavelength lambda_max and a metric for the accuracy lambda_accuracy.
        The units can be found in MetadataDeviceTags.WAVELENGTH_RANGE.unit.
        :return: void
        """
        self.illuminator_element_dict[MetadataDeviceTags.WAVELENGTH_RANGE.tag] = wl_range

    def set_laser_energy_profile(self, energy_profile):
        """
        :param energy_profile: a two element array [wavelengths, laser_energy] describing the laser energy profile.
                    Laser energy and wavelengths are also arrays where len(laser_energy) == len(profile)
                    The units can be found in MetadataDeviceTags.LASER_ENERGY_PROFILE.unit.
        :return: void
        """
        self.illuminator_element_dict[MetadataDeviceTags.LASER_ENERGY_PROFILE.tag] = energy_profile
        
    def set_laser_stability_profile(self, stability_profile):
        """
        :param stability_profile: a two element array [wavelengths,laser_stability,] describing the laser stability profile.
                    Laser stability and wavelengths are also arrays where len(stability_profile) == len(wavelengths).
                    The units can be found in MetadataDeviceTags.LASER_STABILITY_PROFILE.unit.
        :return: void
        """
        self.illuminator_element_dict[MetadataDeviceTags.LASER_STABILITY_PROFILE.tag] = stability_profile

    def set_pulse_width(self, pulse_width: float):
        """
        :param pulse_width: a floating point value describing the pulse width of the laser 
                    in the units of MetadataDeviceTags.PULSE_WIDTH.unit.
        :return: void
        """
        self.illuminator_element_dict[MetadataDeviceTags.PULSE_WIDTH.tag] = pulse_width

    def set_beam_intensity_profile(self, intensity_profile):
        """
        :param intensity_profile: a two element array [wavelengths, intensity_profile] describing the beam itensity profile.
                    Wavelengths and intensity_profile are also arrays where len(wavelengths) == len(intensity_profile)
                    The units can be found in MetadataDeviceTags.BEAM_INTENSITY_PROFILE.unit.
        :return: void
        """
        self.illuminator_element_dict[MetadataDeviceTags.BEAM_INTENSITY_PROFILE.tag] = intensity_profile

    def set_beam_divergence_angles(self, angle: float):
        """
        :param angle: a value describing the opening angle of the laser beam from the illuminator shape with respect 
                    to the orientation vector. This angle is represented by the standard deviation of the beam divergence.
                    The units can be found in MetadataDeviceTags.BEAM_DIVERGENCE_ANGLES.unit.
                    
        :return: void
        """
        self.illuminator_element_dict[MetadataDeviceTags.BEAM_DIVERGENCE_ANGLES.tag] = angle

    def get_dictionary(self):
        return copy.deepcopy(self.illuminator_element_dict)


class DetectionElementCreator(object):
    def __init__(self):
        self.detection_element_dict = dict()

    def set_detector_position(self, detector_position: np.ndarray):
        """
        :param detector_position: an array of three float values that describe the position of the detection element in the
                    x1, x2, and x3 direction.
                    The units can be found in MetadataDeviceTags.DETECTOR_POSITION.unit.
        :return: void
        """
        self.detection_element_dict[MetadataDeviceTags.DETECTOR_POSITION.tag] = detector_position

    def set_detector_orientation(self, orientation: np.ndarray):
        """
        :param orientation: a n array of three float values that describe the orientation of the detector element in the
                    x1, x2, and x3 direction.
                    The units can be found in MetadataDeviceTags.DETECTOR_ORIENTATION.unit.
        :return: void
        """
        self.detection_element_dict[MetadataDeviceTags.DETECTOR_ORIENTATION.tag] = orientation

    def set_detector_size(self, size: np.ndarray):
        """
        :param size: a three element array [x1, x2, x3] describing the extent of the detector size in x1, x2, and x3 direction.
                    The units can be found in MetadataDeviceTags.DETECTOR_SIZE.unit.
        :return: void
        """
        self.detection_element_dict[MetadataDeviceTags.DETECTOR_SIZE.tag] = size

    def set_frequency_response(self, frequency_response):
        """
        :param frequency_response: a two element array [frequency, response] describing the frequency response of the detector.
                    Frequency and response are also arrays where len(frequency) == len(response).
                    The units can be found in MetadataDeviceTags.FREQUENCY_RESPONSE.unit.
        :return: void
        """
        self.detection_element_dict[MetadataDeviceTags.FREQUENCY_RESPONSE.tag] = frequency_response

    def set_angular_response(self, angular_response):
        """
        :param angular_response: a two element array [angles, response] describing the angular response of the detecor.
                    Angles and response are also arrays where len(angles) == len(response).
                    The units can be found in MetadataDeviceTags.ANGULAR_RESPONSE.unit.
        :return: void
        """
        self.detection_element_dict[MetadataDeviceTags.ANGULAR_RESPONSE.tag] = angular_response

    def get_dictionary(self):
        return copy.deepcopy(self.detection_element_dict)


class DeviceMetaDataCreator(object):

    def __init__(self):
        self.GENERAL = MetadataDeviceTags.GENERAL.tag
        self.ILLUMINATORS = MetadataDeviceTags.ILLUMINATORS.tag
        self.DETECTORS = MetadataDeviceTags.DETECTORS.tag
        self.device_dict = dict()
        self.device_dict[self.GENERAL] = dict()
        self.device_dict[self.ILLUMINATORS] = dict()
        self.device_dict[self.DETECTORS] = dict()

    def set_general_information(self, uuid: str, fov: np.ndarray):
        """
        :param uuid: is a string that uniquely identifies the photoacoustic device
        :param fov: is an array of three float values that describe the extent of the field of view of the device in the
                    x1, x2, and x3 direction (x1, x2, x3 is defined in TODO).
        :return: void
        """
        self.device_dict[self.GENERAL][MetadataDeviceTags.UUID.tag] = uuid
        self.device_dict[self.GENERAL][MetadataDeviceTags.FIELD_OF_VIEW.tag] = fov

    def add_detection_element(self, uid: str, detection_element: dict):
        """
        :param uid: is a string that uniquely identifies the detection element
        :param detection_element: is a dictionary for the detection element specific parameters
        :return: void
        """
        self.device_dict[self.DETECTORS][uid] = detection_element

    def add_illumination_element(self, uid: str, illumination_element: dict):
        """
        :param uid: is a string that uniquely identifies the illumination element
        :param illumination_element: is a dictionary for the illumination element specific parameters
        :return: void
        """
        self.device_dict[self.ILLUMINATORS][uid] = illumination_element

    def finalize_device_meta_data(self):

        self.device_dict[self.GENERAL][MetadataDeviceTags.NUMBER_OF_DETECTORS.tag] = len(
            self.device_dict[self.DETECTORS])
        self.device_dict[self.GENERAL][MetadataDeviceTags.NUMBER_OF_ILLUMINATORS.tag] = len(
            self.device_dict[self.ILLUMINATORS])

        return copy.deepcopy(self.device_dict)
