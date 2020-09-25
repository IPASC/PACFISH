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
from ipasc_tool.core import MetaDatum, MetadataDeviceTags, MetadataAcquisitionTags


class PAData:
    """
    TODO: Detailed documentation
    """
    def __init__(self, binary_time_series_data: np.ndarray = None,
                 meta_data_acquisition: dict = None,
                 meta_data_device: dict = None):
        """
        TODO: Detailed documentation

        :param binary_time_series_data:
        :param meta_data_acquisition:
        :param meta_data_device:
        """

        if meta_data_acquisition is None:
            meta_data_acquisition = dict()

        if meta_data_device is None:
            meta_data_device = dict()

        self.binary_time_series_data = binary_time_series_data
        self.meta_data_acquisition = meta_data_acquisition
        self.meta_data_device = meta_data_device

    def get_illuminator_ids(self):
        return self.meta_data_device[MetadataDeviceTags.ILLUMINATORS.tag].keys()

    def get_detector_ids(self):
        return self.meta_data_device[MetadataDeviceTags.DETECTORS.tag].keys()

    def get_meta_datum(self, meta_data_tag: MetaDatum) -> object:
        if meta_data_tag.tag in self.meta_data_acquisition:
            return self.meta_data_acquisition[meta_data_tag.tag]
        else:
            return None

    def get_custom_meta_datum(self, meta_data_tag: str) -> object:
        if meta_data_tag in self.meta_data_acquisition:
            return self.meta_data_acquisition[meta_data_tag]
        else:
            return None

    def get_device_uuid(self):
        if MetadataDeviceTags.UUID.tag in self.meta_data_device[MetadataDeviceTags.GENERAL.tag]:
            return self.meta_data_device[MetadataDeviceTags.GENERAL.tag][MetadataDeviceTags.UUID.tag]
        else:
            return None

    def get_field_of_view(self):
        if MetadataDeviceTags.FIELD_OF_VIEW.tag in self.meta_data_device[MetadataDeviceTags.GENERAL.tag]:
            return self.meta_data_device[MetadataDeviceTags.GENERAL.tag][MetadataDeviceTags.FIELD_OF_VIEW.tag]
        else:
            return None

    def get_number_of_illuminators(self):
        if MetadataDeviceTags.NUMBER_OF_ILLUMINATORS.tag in self.meta_data_device[MetadataDeviceTags.GENERAL.tag]:
            return self.meta_data_device[MetadataDeviceTags.GENERAL.tag][MetadataDeviceTags.NUMBER_OF_ILLUMINATORS.tag]
        else:
            return None

    def get_number_of_detectors(self):
        if MetadataDeviceTags.NUMBER_OF_DETECTORS.tag in self.meta_data_device[MetadataDeviceTags.GENERAL.tag]:
            return self.meta_data_device[MetadataDeviceTags.GENERAL.tag][MetadataDeviceTags.NUMBER_OF_DETECTORS.tag]
        else:
            return None

    def get_illuminator_position(self, identifier=None):
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.ILLUMINATOR_POSITION, identifier)

    def get_illuminator_orientation(self, identifier=None):
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.ILLUMINATOR_ORIENTATION, identifier)

    def get_illuminator_size(self, identifier=None):
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.ILLUMINATOR_SIZE, identifier)

    def get_wavelength_range(self, identifier=None):
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.WAVELENGTH_RANGE, identifier)

    def get_energy_profile(self, identifier=None):
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.LASER_ENERGY_PROFILE, identifier)

    def get_stability_profile(self, identifier=None):
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.LASER_STABILITY_PROFILE, identifier)

    def get_pulse_width(self, identifier=None):
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.PULSE_WIDTH, identifier)

    def get_beam_profile(self, identifier=None):
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.BEAM_INTENSITY_PROFILE, identifier)

    def get_beam_divergence(self, identifier=None):
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.BEAM_DIVERGENCE_ANGLES, identifier)

    def get_illuminator_attribute_for_tag(self, metadatum_tag, identifier=None):
        if identifier is not None:
            if isinstance(identifier, int):
                if identifier < 0 or identifier >= self.get_number_of_illuminators():
                    raise ValueError("The illuminator position " + str(identifier) + "was out of range.")
                else:
                    return list(self.meta_data_device[MetadataDeviceTags.ILLUMINATORS.tag].values())[identifier][
                        metadatum_tag.tag]
            elif isinstance(identifier, str):
                if identifier not in self.get_illuminator_ids():
                    raise ValueError("The illuminator id " + str(identifier) + "was not valid.")
                else:
                    return self.meta_data_device[MetadataDeviceTags.ILLUMINATORS.tag][identifier][metadatum_tag.tag]
            else:
                raise ValueError("identifier must be int or string.")
        else:
            positions = []
            for id in self.get_illuminator_ids():
                positions.append(self.meta_data_device[MetadataDeviceTags.ILLUMINATORS.tag][id][metadatum_tag.tag])
            return np.asarray(positions)

    def get_detector_position(self, identifier=None):
        return self.get_detector_attribute_for_tag(MetadataDeviceTags.DETECTOR_POSITION, identifier)

    def get_detector_orientation(self, identifier=None):
        return self.get_detector_attribute_for_tag(MetadataDeviceTags.DETECTOR_POSITION, identifier)

    def get_detector_size(self, identifier=None):
        return self.get_detector_attribute_for_tag(MetadataDeviceTags.DETECTOR_POSITION, identifier)

    def get_frequency_response(self, identifier=None):
        return self.get_detector_attribute_for_tag(MetadataDeviceTags.FREQUENCY_RESPONSE, identifier)

    def get_angular_response(self, identifier=None):
        return self.get_detector_attribute_for_tag(MetadataDeviceTags.ANGULAR_RESPONSE, identifier)

    def get_detector_attribute_for_tag(self, metadatum_tag, identifier=None):
        if identifier is not None:
            if isinstance(identifier, int):
                if identifier < 0 or identifier >= self.get_number_of_detectors():
                    raise ValueError("The detector position " + str(identifier) + "was out of range.")
                else:
                    return list(self.meta_data_device[MetadataDeviceTags.DETECTORS.tag].values())[identifier][
                        metadatum_tag.tag]
            elif isinstance(identifier, str):
                if identifier not in self.get_detector_ids():
                    raise ValueError("The detector id " + str(identifier) + "was not valid.")
                else:
                    return self.meta_data_device[MetadataDeviceTags.DETECTORS.tag][identifier][metadatum_tag.tag]
            else:
                raise ValueError("detector must be int or string.")
        else:
            positions = []
            for id in self.get_detector_ids():
                positions.append(self.meta_data_device[MetadataDeviceTags.DETECTORS.tag][id][metadatum_tag.tag])
            return np.asarray(positions)

    def get_encoding(self):
        return self.get_meta_datum(MetadataAcquisitionTags.ENCODING)

    def get_compression(self):
        return self.get_meta_datum(MetadataAcquisitionTags.COMPRESSION)

    def get_data_UUID(self):
        return self.get_meta_datum(MetadataAcquisitionTags.UUID)

    def get_data_type(self):
        return self.get_meta_datum(MetadataAcquisitionTags.DATA_TYPE)

    def get_dimensionality(self):
        return self.get_meta_datum(MetadataAcquisitionTags.DIMENSIONALITY)

    def get_sizes(self):
        return self.get_meta_datum(MetadataAcquisitionTags.SIZES)

    def get_device_reference(self):
        return self.get_meta_datum(MetadataAcquisitionTags.PHOTOACOUSTIC_IMAGING_DEVICE)

    def get_pulse_laser_energy(self):
        return self.get_meta_datum(MetadataAcquisitionTags.PULSE_LASER_ENERGY)

    def get_time_stamps(self):
        return self.get_meta_datum(MetadataAcquisitionTags.FRAME_ACQUISITION_TIMESTAMPS)

    def get_wavelengths(self):
        return self.get_meta_datum(MetadataAcquisitionTags.ACQUISITION_OPTICAL_WAVELENGTHS)

    def get_time_gain_compensation(self):
        return self.get_meta_datum(MetadataAcquisitionTags.TIME_GAIN_COMPENSATION)

    def get_overall_gain(self):
        return self.get_meta_datum(MetadataAcquisitionTags.OVERALL_GAIN)

    def get_element_dependent_gain(self):
        return self.get_meta_datum(MetadataAcquisitionTags.ELEMENT_DEPENDENT_GAIN)

    def get_temperature(self):
        return self.get_meta_datum(MetadataAcquisitionTags.TEMPERATURE_CONTROL)

    def get_coupling_agent(self):
        return self.get_meta_datum(MetadataAcquisitionTags.ACOUSTIC_COUPLING_AGENT)

    def get_scanning_method(self):
        return self.get_meta_datum(MetadataAcquisitionTags.SCANNING_METHOD)

    def get_sampling_rate(self):
        return self.get_meta_datum(MetadataAcquisitionTags.AD_SAMPLING_RATE)

    def get_frequency_filter(self):
        return self.get_meta_datum(MetadataAcquisitionTags.FREQUENCY_DOMAIN_FILTER)
