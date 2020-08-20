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

from abc import ABC, abstractmethod
from ipasc_tool.core.PAData import PAData
from ipasc_tool.core.Metadata import MetadataAcquisitionTags, MetaDatum
import numpy as np


class BaseAdapter(ABC):

    @abstractmethod
    def generate_binary_data(self) -> np.ndarray:
        """
        #TODO very detailed decription of how the binary meta data dump should be organized.
        :return: numpy array
        """
        pass

    def generate_meta_data(self) -> dict:
        """

        :return:
        """
        meta_data_dictionary = dict()

        for metadata_enum in MetadataAcquisitionTags.TAGS:
            target_value = self.set_metadata_value(metadata_enum)
            if target_value is not None:
                meta_data_dictionary[metadata_enum.tag] = target_value

        return meta_data_dictionary

    @abstractmethod
    def generate_meta_data_device(self) -> dict:
        """
        # TODO this method can be implemented using the DeviceMetaDataCreator
        :return:
        """
        pass

    def generate_pa_data(self) -> PAData:
        pa_data = PAData()

        binary_data = self.generate_binary_data()
        pa_data.binary_time_series_data = binary_data

        meta_data = self.generate_meta_data()
        pa_data.meta_data = meta_data

        meta_data_device = self.generate_meta_data_device()
        pa_data.meta_data_device = meta_data_device

        return pa_data

    @abstractmethod
    def set_metadata_value(self, metadata_tag: MetaDatum) -> object:
        """

        This method must be implemented to yield appropriate data for all MetaDatum elements in the
        MetadataTags class.

        :param metadata_tag:
        :return:
        """
        pass
