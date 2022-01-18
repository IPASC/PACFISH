# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-FileCopyrightText: 2021 Janek Gröhl
# SPDX-FileCopyrightText: 2021 Lina Hacker
# SPDX-License-Identifier: BSD 3-Clause License

from abc import ABC, abstractmethod
from pacfish.core.PAData import PAData
from pacfish.core.Metadata import MetadataAcquisitionTags, MetaDatum
import numpy as np


class BaseAdapter(ABC):
    """
    The purpose of the BaseAdapter class is to provide the framework to convert from any
    given input data type into the IPASC format. It can be used as a basis for extension
    for a custom Adapter.

    To achieve this, one needs to inherit from BaseAdapter and implement the abstract methods::

        class CustomAdapter(BaseAdapter):

            def __init__():
                # TODO do all of the loading etc here
                # Then call the __init__ of the BaseAdapter
                super(CustomAdapter, self).__init__()
                # TODO Add custom parameters after calling BaseAdapter.__init__

            def generate_binary_data(self):
                # TODO

            def generate_device_meta_data(self):
                # TODO

            def set_metadata_value(self, metadatum: MetaDatum):
                # TODO
    """

    def __init__(self):
        self.pa_data = PAData()

        binary_data = self.generate_binary_data()
        self.pa_data.binary_time_series_data = binary_data

        meta_data = self.generate_acquisition_meta_data()
        self.pa_data.meta_data_acquisition = meta_data

        meta_data_device = self.generate_device_meta_data()
        self.pa_data.meta_data_device = meta_data_device


    @abstractmethod
    def generate_binary_data(self) -> np.ndarray:
        """
        The binary data is the raw time series data.
        It is internally stored as an N-dimensional numpy array.
        The binary data must be formatted the following way:

        [detectors, samples, wavelengths, measurements]

        Return
        ------
        np.ndarray
            A numpy array containing the binary data
        """
        pass

    @abstractmethod
    def generate_device_meta_data(self) -> dict:
        """
        Must be implemented to define a digital twin of the photoacoustic imaging device.
        This method can be implemented using the DeviceMetaDataCreator.

        Return
        ------
        dict
            A dictionary containing all key-value pair necessary to describe a digital twin of a
            photoacoustic device.
        """
        pass

    @abstractmethod
    def set_metadata_value(self, metadatum: MetaDatum) -> object:
        """

        This method must be implemented to yield appropriate data for all MetaDatum elements in the
        MetadataTags class.

        You are given a certain meta datum nd have to return the appropriate information.

        Parameters
        ----------
        metadatum: MetaDatum
            The MetaDatum for which to return the correct data.

        Return
        ------
        object
            The data corresponding to the given MetaDatum
        """
        pass

    def generate_acquisition_meta_data(self) -> dict:
        """
        Internal method

        Return
        ------
        dict
        """
        meta_data_dictionary = dict()

        for metadatum in MetadataAcquisitionTags.TAGS:
            target_value = self.set_metadata_value(metadatum)
            if target_value is not None:
                meta_data_dictionary[metadatum.tag] = target_value

        return meta_data_dictionary

    def add_custom_meta_datum_field(self, key: str, value: object):
        """
        This method can be used to add a metadata field that is not reflected in the
        standard list of metadata of the IPASC format.
        Must be called after the __init__ method of the BaseAdapter was called.
        The custom meta data are stored in the AcquisitionMetadata dictionary.

        Parameters
        ----------
        key: str
            The unique name with which the value is stored in the dictionary.
        value: object
            The value to store.
        """
        if key is None:
            raise KeyError("A meta datum key must not be None.")
        if value is None:
            raise ValueError("The given value must not be None.")
        self.pa_data.meta_data_acquisition[key] = value

    def generate_pa_data(self) -> PAData:
        """
        Internal method

        Return
        ------
        PAData
        """

        return self.pa_data
