import numpy as np
import os
import glob

from pacfish import BaseAdapter, MetaDatum
from pacfish import MetadataAcquisitionTags
from pacfish import DeviceMetaDataCreator, DetectionElementCreator, IlluminationElementCreator

class ImagioFileConverter(BaseAdapter):
    """
    For the Seno Imagio system.
    """
    def __init__(self, path):

        #
        # TODO:
        # - how to handle corresponding ultrasound data
        # - how to handle meta-data per frame
        # - .dat binary data format
        meta_variables = [
           "sNumChans",
           "sNumSamplesPerChannel",
           "sDataType",
           "lFrameCounter",
           "iSampleRate",
           "cWavelength",
           "fLaserEnergy",
           "caProbeSN",
           "LaserInfo.uiPulseCounter",
           "Width (Pixels)",
           "Height (Pixels)",
           "Width (mm)",
           "Height (mm)",
           "Speed of Sound",
           "Ts_us[2]",
           ]
        meta_files = glob.glob(path + "/**/*_meta.txt", recursive=True)
        for meta_file in meta_files:
            with open(meta_file) as file:
                for line in file:
                    for meta_var in meta_variables:
                        if meta_var in line:
                            s = line.strip().split() 
                            print(meta_var + ": " + s[-1])


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

