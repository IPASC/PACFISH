import numpy as np
import os
import glob
import struct

from pacfish import BaseAdapter, MetaDatum
from pacfish import MetadataAcquisitionTags
from pacfish import DeviceMetaDataCreator, DetectionElementCreator, IlluminationElementCreator

class ImagioFileConverter(BaseAdapter):

    # see OAFrameHeader.h
    OAFRAMETYPE_OA = 1
    OAFRAMETYPE_US = 2
    OAFRAMETYPE_CONFIG = 3
    OAFRAMETYPE_ANNOTATION = 4
    OAFRAMETYPE_AUDIO = 5
    OAFRAMETYPE_VERSION = 6
    OAFRAMETYPE_PROBE = 7
    OAFRAMETYPE_TGC = 8
    OAFRAMETYPE_PROBE_POSITION = 9
    OAFRAME_MAGIC = 0xbee5

    """
    For the Seno Imagio system.
    """
    def __init__(self, filename):

        #
        # TODO:
        # - how to handle corresponding ultrasound data
        # - how to handle meta-data per frame
        # - binary data within lom
        #
        
        # parse the .lom file. see OAFrameHeader.h for binary format.
        with open(filename, "rb") as f:

            while True:
                data = f.read(1024)

                if not data:
                    print("no data left!")
                    break

                metaData = (sMagic, sVersion, iTick, lSize, lFrameCounter, sType, sDummy) = struct.unpack("<HHIIIhh", data[0:20]) 
                frameHeader = bytes(struct.unpack("1000B", data[20:1020]))
                lCRC = struct.unpack("i", data[1020:1024])
                frameData = f.read(lSize) 

                if (sType == self.OAFRAMETYPE_OA):
                    laserInfo = struct.unpack("<ddddiiffIiiiii", frameHeader[0:72]) # TODO parse out sub-fields as necessary
                    (sNumChans, sNumSamplesPerChannel, sDataType, lFrameCounter, sProbeID, sAcquireHardwareID, iSampleRate) = struct.unpack("<hhHIhhi", frameHeader[72:90])
                    cChannelsReceived = struct.unpack("<32B", frameHeader[90:122])
                    s = (sFrameStatus, cWavelength, isCalibrationFrame) = struct.unpack("<HBB", frameHeader[122:126])
                    print(s)


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

