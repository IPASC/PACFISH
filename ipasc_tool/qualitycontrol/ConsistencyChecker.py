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
import numbers
from ipasc_tool import MetaDatum, MetadataAcquisitionTags, MetadataDeviceTags


class ConsistencyChecker:

    def __init__(self, verbose: bool = False, log_file_path: str = None):
        """
        :param verbose: A flag to indicate whether the log should be printed
                to the console.
        :param log_file_path: If given a string with the path to where the log
              file should be written to.
        """
        self.save_file_name = "logfile.md"
        self.verbose = verbose
        self.log_file_path = log_file_path

    def check_binary(self, binary_data) -> bool:
        is_consistent = True
        if not isinstance(binary_data, np.ndarray):
            is_consistent = False
            #TODO

        for number in np.reshape(binary_data, (-1, )):
            if not isinstance(number, numbers.Number):
                is_consistent = False
                # TODO
        print("Test")
        return is_consistent

    def check_meta_data(self, meta_data: dict) -> bool:
        is_consistent = True
        num_inconsistencies = 0
        log_message = ""
        log_message += "#Consistency Report for Acquisition Meta Data\n\n"
        for metadatum in MetadataAcquisitionTags.TAGS:
            if metadatum.tag in meta_data:
                result = metadatum.evaluate_value_range(meta_data[metadatum.tag])
                if result is False:
                    is_consistent = False
                    log_message += metadatum.tag + " was found not to be consistent.\n"
                    num_inconsistencies += 1
        log_message += "##Results\n\n"
        if num_inconsistencies == 0:
            log_message += "No inconsistencies were found in the meta data.\n\n"
        else:
            log_message += "!! " + str(num_inconsistencies) + " inconsistencies were found in the meta data!!\n\n"

        if self.verbose:
            print(log_message)

        if self.log_file_path is not None:
            with open(self.log_file_path + self.save_file_name, "a") as log_file_handle:
                log_file_handle.writelines(log_message)

        return is_consistent

    def check_meta_data_device(self, device_meta_data: dict) -> bool:
        is_consistent = True
        num_inconsistencies = 0
        log_message = ""
        log_message += "#Consistency Report for Device Meta Data\n\n"
        log_message += "##General Tags\n\n"

        general_tags = [MetadataDeviceTags.UUID, MetadataDeviceTags.FIELD_OF_VIEW]
        for metadatum in general_tags:
            if metadatum.tag in device_meta_data[MetadataDeviceTags.GENERAL.tag]:
                result = metadatum.evaluate_value_range(
                    device_meta_data[MetadataDeviceTags.GENERAL.tag][metadatum.tag])
                if result is False:
                    is_consistent = False
                    log_message += metadatum.tag + " was found not to be consistent.\n"
                    num_inconsistencies += 1

        log_message += "##Detection Elements\n\n"
        detection_tags = [MetadataDeviceTags.DETECTOR_SIZE, MetadataDeviceTags.DETECTOR_ORIENTATION,
                          MetadataDeviceTags.DETECTOR_POSITION, MetadataDeviceTags.FREQUENCY_RESPONSE,
                          MetadataDeviceTags.ANGULAR_RESPONSE]
        for metadatum in detection_tags:
            for detector_dict in device_meta_data[MetadataDeviceTags.DETECTORS.tag]:
                if metadatum.tag in device_meta_data[MetadataDeviceTags.DETECTORS.tag][detector_dict]:
                    result = metadatum.evaluate_value_range(
                        device_meta_data[MetadataDeviceTags.DETECTORS.tag][detector_dict][metadatum.tag])
                    if result is False:
                        is_consistent = False
                        num_inconsistencies += 1
                        log_message += metadatum.tag + " was found not to be consistent.\n"

        log_message += "##Illumination Elements\n\n"
        illumination_tags = [MetadataDeviceTags.ILLUMINATOR_SIZE, MetadataDeviceTags.ILLUMINATOR_ORIENTATION,
                             MetadataDeviceTags.ILLUMINATOR_POSITION, MetadataDeviceTags.WAVELENGTH_RANGE,
                             MetadataDeviceTags.LASER_ENERGY_PROFILE, MetadataDeviceTags.PULSE_WIDTH,
                             MetadataDeviceTags.LASER_STABILITY_PROFILE, MetadataDeviceTags.BEAM_INTENSITY_PROFILE,
                             MetadataDeviceTags.BEAM_DIVERGENCE_ANGLES]
        for metadatum in illumination_tags:
            for illumination_dict in device_meta_data[MetadataDeviceTags.ILLUMINATORS.tag]:
                if metadatum.tag in device_meta_data[MetadataDeviceTags.ILLUMINATORS.tag][illumination_dict]:
                    result = metadatum.evaluate_value_range(
                        device_meta_data[MetadataDeviceTags.ILLUMINATORS.tag][illumination_dict][metadatum.tag])
                    if result is False:
                        is_consistent = False
                        num_inconsistencies += 1
                        log_message += metadatum.tag + " was found not to be consistent.\n"

        log_message += "##Results\n\n"
        if num_inconsistencies == 0:
            log_message += "No inconsistencies were found in the meta data.\n\n"
        else:
            log_message += "!! " + str(num_inconsistencies) + " inconsistencies were found in the meta data!!\n\n"

        if self.verbose:
            print(log_message)

        if self.log_file_path is not None:
            with open(self.log_file_path + self.save_file_name, "a") as log_file_handle:
                log_file_handle.writelines(log_message)

        return is_consistent
