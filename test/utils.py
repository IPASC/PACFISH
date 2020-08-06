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

import numpy as np
from ipasc_tool import MetadataDeviceTags


def create_random_testing_parameters():

    test_float = np.random.random()
    test_list = [np.random.random(), np.random.random(), -np.random.random()]
    test_string = str(np.random.random())
    test_dict = dict()
    test_array = np.random.random((1000, 2))
    return {'test_float': test_float,
            'test_list': test_list,
            'test_string': test_string,
            'test_dict': test_dict,
            'test_array': test_array}


def create_random_illumination_element(dim_x=None, dim_y=None, dim_z=None):

    if dim_x is None:
        dim_x = 0.03
    if dim_y is None:
        dim_y = 0.001
    if dim_z is None:
        dim_z = 0.01

    illuminator_dict = dict()
    illuminator_dict[MetadataDeviceTags.ILLUMINATOR_POSITION.info.tag] = np.asarray([
        np.random.random() * 2 * dim_x - dim_x,
        np.random.random() * 2 * dim_x - dim_x,
        -np.random.random() * dim_x / 2])
    illuminator_dict[MetadataDeviceTags.ILLUMINATOR_ORIENTATION.info.tag] = np.asarray([
        np.random.random() * dim_x - dim_x / 2,
        np.random.random() * dim_y - dim_y / 2,
        np.random.random() * dim_z - dim_z / 2])
    size = np.random.random() * dim_x / 10
    illuminator_dict[MetadataDeviceTags.ILLUMINATOR_SHAPE.info.tag] = np.asarray([size, size, size])
    min_wavelength = np.random.random() * 200 + 600
    illuminator_dict[MetadataDeviceTags.WAVELENGTH_RANGE.info.tag] = np.asarray([min_wavelength,
                                                                                 min_wavelength +
                                                                                 np.random.random() * 200,
                                                                                 1.0])
    illuminator_dict[MetadataDeviceTags.LASER_ENERGY_PROFILE.info.tag] = np.random.random(size=(200,))
    illuminator_dict[MetadataDeviceTags.LASER_STABILITY_PROFILE.info.tag] = np.random.random(size=(200,))
    illuminator_dict[MetadataDeviceTags.PULSE_WIDTH.info.tag] = 0.00000012
    illuminator_dict[MetadataDeviceTags.BEAM_INTENSITY_PROFILE.info.tag] = np.random.random(size=(100, 100))
    illuminator_dict[MetadataDeviceTags.BEAM_DIVERGENCE_ANGLES.info.tag] = np.deg2rad(np.random.random() * 90)
    return illuminator_dict


def create_random_detection_element(dim_x=None, dim_y=None, dim_z=None):

    if dim_x is None:
        dim_x = 0.03
    if dim_y is None:
        dim_y = 0.001
    if dim_z is None:
        dim_z = 0.01

    detector_dict = dict()
    detector_dict[MetadataDeviceTags.DETECTOR_POSITION.info.tag] = np.asarray([np.random.random() * dim_x,
                                                                               np.random.random() * dim_y,
                                                                               -np.random.random() * dim_z])
    detector_dict[MetadataDeviceTags.DETECTOR_ORIENTATION.info.tag] = np.asarray(
        [np.random.random() * dim_x - dim_x / 2,
         np.random.random() * dim_y - dim_y / 2,
         np.random.random() * dim_z - dim_z / 2])
    detector_dict[MetadataDeviceTags.DETECTOR_SIZE.info.tag] = np.asarray([np.random.random() * dim_x,
                                                                           np.random.random() * dim_y,
                                                                           np.random.random() * dim_z])
    detector_dict[MetadataDeviceTags.FREQUENCY_RESPONSE.info.tag] = np.random.random(size=(200,))
    detector_dict[MetadataDeviceTags.ANGULAR_RESPONSE.info.tag] = np.random.random(size=(200,))
    return detector_dict


def create_complete_device_metadata_dictionary(dim_x=None, dim_y=None, dim_z=None):

    if dim_x is None:
        dim_x = 0.03
    if dim_y is None:
        dim_y = 0.001
    if dim_z is None:
        dim_z = 0.01

    dictionary = {
        MetadataDeviceTags.GENERAL.info.tag: {
            MetadataDeviceTags.UUID.info.tag: "a2fd-48nbsh-sfiush7-chjs",
            MetadataDeviceTags.FIELD_OF_VIEW.info.tag: np.asarray([0.03, 0.002, 0.03]),
            MetadataDeviceTags.NUMBER_OF_ILLUMINATORS.info.tag: 2,
            MetadataDeviceTags.NUMBER_OF_DETECTORS.info.tag: 4
        },
        MetadataDeviceTags.ILLUMINATORS.info.tag: {
            MetadataDeviceTags.ILLUMINATION_ELEMENT.info.tag + "_0":
                create_random_illumination_element(dim_x, dim_y, dim_z),
            MetadataDeviceTags.ILLUMINATION_ELEMENT.info.tag + "_1":
                create_random_illumination_element(dim_x, dim_y, dim_z)
        },
        MetadataDeviceTags.DETECTORS.info.tag: {
            MetadataDeviceTags.DETECTION_ELEMENT.info.tag + "_0":
                create_random_detection_element(dim_x, dim_y, dim_z),
            MetadataDeviceTags.DETECTION_ELEMENT.info.tag + "_1":
                create_random_detection_element(dim_x, dim_y, dim_z),
            MetadataDeviceTags.DETECTION_ELEMENT.info.tag + "_2":
                create_random_detection_element(dim_x, dim_y, dim_z),
            MetadataDeviceTags.DETECTION_ELEMENT.info.tag + "_3":
                create_random_detection_element(dim_x, dim_y, dim_z)
        }
    }

    return dictionary
