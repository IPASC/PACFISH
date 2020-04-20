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

from ipasc_tool.core import MetadataTags
from ipasc_tool.core import MetadataDeviceTags
from ipasc_tool.core import MetaDatum


class CompletenessChecker:

    def __init__(self):
        self.save_file_name = "logfile.md"

    def check_meta_data(self, meta_data_dictionary: dict, verbose: bool = False,
                        log_file_path: str = None) -> bool:
        """
        This function will evaluate the completeness of the reported metadata.
        It can be used to generate a report to the console by setting `verbose`
        to True. When setting a file path to log_file, it will also save the
        report as a txt file in the designated path.

        :param meta_data_dictionary: A dictionary containing all PA image
        meta data.
        :param verbose: A flag to indicate whether the log should be printed
                        to the console.
        :param log_file_path: If given a string with the path to where the log
                              file should be written to.

        :return: True, if the meta_data_dictionary is complete

        :raises ValueError: if meta_data_dictionary was None
        :raises TypeError: if one of the arguments ws not of the correct type
        """

        # Input data validation
        if meta_data_dictionary is None:
            raise ValueError("the field meta_data_dictionary must not be None!")

        if not isinstance(meta_data_dictionary, dict):
            raise TypeError("The field meta_data_dictionary was not of " +
                            "type dict")

        # Creation of the completenes report
        incompletenes_count = 0

        log_string = "#Completeness Report\n\n"

        log_string += "##Individual fields\n\n"
        for metadatum in MetadataTags:
            [log, count] = check_metadatum_from_dict(meta_data_dictionary, metadatum)
            incompletenes_count += count
            log_string += log

        log_string += "## Result\n\n"

        log_string += (str(incompletenes_count) + " metadata fields were "
                       "found to be incomplete or missing.\n\n")

        if incompletenes_count > 0:
            log_string += "The metadata dictionary is incomplete\n"
        else:
            log_string += "The metadata dictionary is complete\n"

        # Reporting of the results
        if verbose:
            print(log_string)

        if log_file_path is not None:
            with open(log_file_path + self.save_file_name, "w") as log_file_handle:
                log_file_handle.writelines(log_string)

        return incompletenes_count == 0

    def check_meta_data_device(self, device_meta_data: dict, verbose: bool = False,
                               log_file_path: str = None):

        incompletenes_count = 0

        # Input data validation
        if device_meta_data is None:
            raise ValueError("the field device_meta_data must not be None!")

        if not isinstance(device_meta_data, dict):
            raise TypeError("The field device_meta_data was not of type dict")

        log_string = "#Device Metadata Completeness Report\n\n"

        log_string += "##General information\n\n"

        general_tags = [MetadataDeviceTags.UUID, MetadataDeviceTags.FIELD_OF_VIEW]

        if MetadataDeviceTags.GENERAL.info.tag not in device_meta_data:
            log_string += "General device meta data is missing!\n\n"
            incompletenes_count += len(general_tags)
        else:
            for general_meta_datum in general_tags:
                [log, count] = check_metadatum_from_dict(device_meta_data[MetadataDeviceTags.GENERAL.info.tag],
                                                         general_meta_datum)
                log_string += log
                incompletenes_count += count

        log_string += "##Detection Elements\n\n"

        detection_tags = [MetadataDeviceTags.DETECTOR_SIZE, MetadataDeviceTags.DETECTOR_ORIENTATION,
                          MetadataDeviceTags.DETECTOR_POSITION, MetadataDeviceTags.FREQUENCY_RESPONSE,
                          MetadataDeviceTags.ANGULAR_RESPONSE]

        if MetadataDeviceTags.DETECTORS.info.tag not in device_meta_data:
            log_string += "Detection elements data is missing!\n\n"
            incompletenes_count += len(detection_tags)
        else:
            log_string += ("Found " + str(len(device_meta_data[MetadataDeviceTags.DETECTORS.info.tag])) +
                           " detection elements.\n\n")
            for detector_dict in device_meta_data[MetadataDeviceTags.DETECTORS.info.tag]:
                log_string += ("Now analyzing detector element \"" +
                               detector_dict + "\"\n\n")
                for detector_meta_datum in detection_tags:
                    [log, count] = check_metadatum_from_dict(device_meta_data[MetadataDeviceTags.DETECTORS.info.tag][detector_dict],
                                                             detector_meta_datum)
                    log_string += log
                    incompletenes_count += count

        log_string += "##Illumination Elements\n\n"

        illumination_tags = [MetadataDeviceTags.ILLUMINATOR_SHAPE, MetadataDeviceTags.ILLUMINATOR_ORIENTATION,
                             MetadataDeviceTags.ILLUMINATOR_POSITION, MetadataDeviceTags.WAVELENGTH_RANGE,
                             MetadataDeviceTags.LASER_ENERGY_PROFILE, MetadataDeviceTags.PULSE_WIDTH,
                             MetadataDeviceTags.LASER_STABILITY_PROFILE, MetadataDeviceTags.BEAM_INTENSITY_PROFILE,
                             MetadataDeviceTags.BEAM_DIVERGENCE_ANGLES]

        if MetadataDeviceTags.ILLUMINATORS.info.tag not in device_meta_data:
            log_string += "Detection elements data is missing!\n\n"
            incompletenes_count += len(illumination_tags)
        else:
            log_string += ("Found " + str(len(device_meta_data[MetadataDeviceTags.ILLUMINATORS.info.tag])) +
                           " detection elements.\n\n")
            for illuminator_dict in device_meta_data[MetadataDeviceTags.ILLUMINATORS.info.tag]:
                log_string += ("Now analyzing illumination element \"" +
                               illuminator_dict + "\"\n\n")
                for illuminator_meta_datum in illumination_tags:
                    [log, count] = check_metadatum_from_dict(device_meta_data[MetadataDeviceTags.ILLUMINATORS.info.tag][illuminator_dict],
                                                             illuminator_meta_datum)
                    log_string += log
                    incompletenes_count += count

        log_string += "## Result\n\n"

        log_string += (str(incompletenes_count) + " metadata fields were "
                       "found to be incomplete or missing.\n\n")

        if incompletenes_count > 0:
            log_string += "The metadata dictionary is incomplete!\n"
        else:
            log_string += "The metadata dictionary is complete.\n"

        if verbose:
            print(log_string)

        if log_file_path is not None:
            with open(log_file_path + self.save_file_name, "w") as log_file_handle:
                log_file_handle.writelines(log_string)

        return incompletenes_count == 0


def check_metadatum_from_dict(dictionary: dict, metadatum: MetadataDeviceTags):
    """

    :param dictionary:
    :param meta_datum:
    :return: [log, count]
    """
    log_string = ""
    count = 0
    if metadatum.info.tag not in dictionary:
        log_string += "* missing entry \"" + metadatum.info.tag + "\"\n"
        log_string += "  * metadatum not found in dictionary\n\n"
        count += 1
    elif dictionary[metadatum.info.tag] is None:
        log_string += "* missing entry \"" + metadatum.info.tag + "\"\n"
        log_string += "  * metadatum found in dictionary\n"
        log_string += "  * but the mapped field was None\n\n"
        count += 1
    elif not isinstance(dictionary[metadatum.info.tag], metadatum.info.dtype):
        log_string += "* corrupt entry \"" + metadatum.info.tag + "\"\n"
        log_string += "  * metadatum found in dictionary\n"
        log_string += "  * and the mapped field was not None\n"
        log_string += ("  * but the mapped field was not of type " +
                       str(metadatum.info.dtype) + "\n\n")
        count += 1

    return [log_string, count]

