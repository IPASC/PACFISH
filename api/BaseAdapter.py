from abc import ABC, abstractmethod
from core.PAData import PAData
from qualitycontrol.ConsistencyChecker import ConsistencyChecker
from core.metadata_tags import MetadataBinaryTags

class BaseAdapter(ABC):

    def generate_binary_data(self):
        """
        #TODO very detailed decription of how the binary meta data dump should be organized.
        :return: numpy array
        """
        pass

    def generate_meta_data_binary(self):
        meta_data_binary_dictionary = dict()

        meta_data_binary_dictionary[MetadataBinaryTags.DIMENSIONALITY] = self.set_binary_dimensionality()

        # ... TODO add all

        return meta_data_binary_dictionary

    def generate_meta_data_device(self):
        """
        # TODO this method can be implemented using the DeviceMetaDataCreator
        :return:
        """
        pass

    def generate_pa_data(self):
        consistency_checker = ConsistencyChecker()
        pa_data = PAData()

        binary_data = self.generate_binary_data()
        consistency_checker.check_binary(binary_data)
        pa_data.binary_time_series_data = binary_data

        binary_data = self.generate_binary_data()
        consistency_checker.check_binary(binary_data)
        pa_data.binary_time_series_data = binary_data

        meta_data_binary = self.generate_meta_data_binary()
        consistency_checker.check_meta_data_binary(meta_data_binary)
        pa_data.meta_data_binary = meta_data_binary

        meta_data_device = self.generate_meta_data_device()
        consistency_checker.check_meta_data_device(meta_data_device)
        pa_data.meta_data_device = meta_data_device

        return pa_data


    def set_binary_dimensionality(self):
        """
        # TODO very detailed description of what this value should look like
        :return:
        """
        pass