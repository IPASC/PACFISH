# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-FileCopyrightText: 2021 Janek Gröhl
# SPDX-FileCopyrightText: 2021 Lina Hacker
# SPDX-License-Identifier: BSD 3-Clause License

from abc import ABC, abstractmethod
from pacfish.core.PAData import PAData
from pacfish.core.Metadata import MetadataAcquisitionTags, MetaDatum
import numpy as np


class BaseAdapter(ABC):

    def __init__(self):
        self.pa_data = PAData()

        binary_data = self.generate_binary_data()
        self.pa_data.binary_time_series_data = binary_data

        meta_data = self.generate_meta_data()
        self.pa_data.meta_data_acquisition = meta_data

        meta_data_device = self.generate_meta_data_device()
        self.pa_data.meta_data_device = meta_data_device


    @abstractmethod
    def generate_binary_data(self) -> np.ndarray:
        """
        #TODO very detailed decription of how the binary meta data dump should be organized.
        :return: numpy array
        """
        pass

    @abstractmethod
    def generate_meta_data_device(self) -> dict:
        """
        # TODO this method can be implemented using the DeviceMetaDataCreator
        :return:
        """
        pass

    @abstractmethod
    def set_metadata_value(self, metadata_tag: MetaDatum) -> object:
        """

        This method must be implemented to yield appropriate data for all MetaDatum elements in the
        MetadataTags class.

        :param metadata_tag:
        :return:
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

    def add_custom_meta_datum_field(self, key: str, value: object):
        if key is None:
            raise KeyError("A meta datum key must not be None.")
        if value is None:
            raise ValueError("The given value must not be None.")
        self.pa_data.meta_data_acquisition[key] = value

    def generate_pa_data(self) -> PAData:

        return self.pa_data


