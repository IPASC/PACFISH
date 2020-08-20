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
from ipasc_tool.core import MetaDatum, MetadataDeviceTags


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
        return self.meta_data_device[MetadataDeviceTags.ILLUMINATORS].keys()

    def get_illuminator_property_by_tag(self, illuminator_id: str, metadata_device_tag: MetaDatum) -> object:
        if illuminator_id not in self.meta_data_device[MetadataDeviceTags.ILLUMINATORS]:
            raise KeyError("Iluminator ID " + illuminator_id + " not found in dictionary. Use get_illuminator_ids " +
                           "to get a list of al valid illuminator ids")
        if metadata_device_tag.tag in self.meta_data_device[MetadataDeviceTags.ILLUMINATORS][illuminator_id]:
            return self.meta_data_device[MetadataDeviceTags.ILLUMINATORS][illuminator_id][metadata_device_tag.tag]
        else:
            return None

    def get_detector_ids(self):
        return self.meta_data_device[MetadataDeviceTags.DETECTORS].keys()

    def get_detector_property_by_tag(self, detector_id: str, metadata_device_tag: MetaDatum) -> object:
        if detector_id not in self.meta_data_device[MetadataDeviceTags.DETECTORS]:
            raise KeyError("Device ID " + detector_id + " not found in dictionary. Use get_detector_ids to get a " +
                           "list of al valid detector ids")
        if metadata_device_tag.tag in self.meta_data_device[MetadataDeviceTags.DETECTORS][detector_id]:
            return self.meta_data_device[MetadataDeviceTags.DETECTORS][detector_id][metadata_device_tag.tag]
        else:
            return None

    def get_meta_datum(self, meta_data_tag: MetaDatum) -> object:
        if meta_data_tag in self.meta_data_acquisition:
            return self.meta_data_acquisition[meta_data_tag]
        else:
            return None

    def get_custom_meta_datum(self, meta_data_tag: str) -> object:
        if meta_data_tag in self.meta_data_acquisition:
            return self.meta_data_acquisition[meta_data_tag]
        else:
            return None
