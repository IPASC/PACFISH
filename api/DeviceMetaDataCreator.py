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

    def set_illuminator_position(self, x1, x2, x3):
        self.illuminator_element_dict[MetadataDeviceTags.ILLUMINATOR_POSITION.info.tag] = [x1, x2, x3]

    def set_illuminator_orientation(self, r1, r2, r3):
        self.illuminator_element_dict[MetadataDeviceTags.ILLUMINATOR_ORIENTATION.info.tag] = [r1, r2, r3]

    def set_illuminator_shape(self, val):
        self.illuminator_element_dict[MetadataDeviceTags.ILLUMINATOR_SHAPE.info.tag] = val

    def set_wavelength_range(self, lamda_min, lamda_max, lamda_accuracy):
        self.illuminator_element_dict[MetadataDeviceTags.WAVELENGTH_RANGE.info.tag] = [
            lamda_min, lamda_max, lamda_accuracy]

    def set_laser_energy_profile(self, val):
        self.illuminator_element_dict[MetadataDeviceTags.LASER_ENERGY_PROFILE.info.tag] = val

    def set_laser_stability_profile(self, val):
        self.illuminator_element_dict[MetadataDeviceTags.LASER_STABILITY_PROFILE.info.tag] = val

    def set_pulse_width(self, val):
        """

        :param val: a floating point value in the units of MetadataDeviceTags.PULSE_WIDTH.info.unit.
        :return:
        """
        self.illuminator_element_dict[MetadataDeviceTags.PULSE_WIDTH.info.tag] = val

    def set_beam_intensity_profile(self, val):
        self.illuminator_element_dict[MetadataDeviceTags.BEAM_INTENSITY_PROFILE.info.tag] = val

    def set_beam_divergence_angles(self, angle):
        self.illuminator_element_dict[MetadataDeviceTags.BEAM_DIVERGENCE_ANGLES.info.tag] = angle

    def get_dictionary(self):
        return copy.deepcopy(self.illuminator_element_dict)


class DetectionElementCreator(object):
    def __init__(self):
        self.detection_element_dict = dict()

    def set_detector_position(self, x1, x2, x3):
        self.detection_element_dict[MetadataDeviceTags.DETECTOR_POSITION.info.tag] = [x1, x2, x3]

    def set_detector_orientation(self, r1, r2, r3):
        self.detection_element_dict[MetadataDeviceTags.DETECTOR_ORIENTATION.info.tag] = [r1, r2, r3]

    def set_detector_size(self, x1, x2, x3):
        self.detection_element_dict[MetadataDeviceTags.DETECTOR_SIZE.info.tag] = [x1, x2, x3]

    def set_frequency_response(self, val):
        """

        :param val: a two element list [frequency, response] frequency and response are also lists where
                    len(frequency) == len(response)
        :return:
        """
        self.detection_element_dict[MetadataDeviceTags.FREQUENCY_RESPONSE.info.tag] = val

    def set_angular_response(self, val):
        self.detection_element_dict[MetadataDeviceTags.ANGULAR_RESPONSE.info.tag] = val

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
        self.device_dict['detectors'][uid] = detection_element

    def add_illumination_element(self, uid: str, illumination_element: dict):
        self.device_dict['illuminators'][uid] = illumination_element

    def finalize_device_meta_data(self):

        self.device_dict['general'][MetadataDeviceTags.NUMBER_OF_DETECTORS.info.tag] = len(
            self.device_dict['detectors'])
        self.device_dict['general'][MetadataDeviceTags.NUMBER_OF_ILLUMINATORS.info.tag] = len(
            self.device_dict['illuminators'])

        return copy.deepcopy(self.device_dict)
