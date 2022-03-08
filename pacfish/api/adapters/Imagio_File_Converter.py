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

    metadata = {}

    """
    For the Seno Imagio system.
    """
    def __init__(self, filename):

        #
        # TODO:
        # - corresponding ultrasound data
        #
        
        # parse the Laser Optic Movie (.lom) file. see OAFrameHeader.h for binary format.
        with open(filename, "rb") as f:

            self.metadata[MetadataAcquisitionTags.PULSE_ENERGY] = []
            self.metadata[MetadataAcquisitionTags.MEASUREMENT_TIMESTAMPS] = []

            while True:
                data = f.read(1024)

                if not data:
                    break

                metaData = (sMagic, sVersion, iTick, lSize, lFrameCounter, sType, sDummy) = struct.unpack("<HHIIIhh", data[0:20]) 
                if (sMagic != self.OAFRAME_MAGIC):
                    print(f"ERROR: Unexpected magic number (read 0x{sMagic:04x}, expected 0x{self.OAFRAME_MAGIC:04x})")
                frameHeader = bytes(struct.unpack("1000B", data[20:1020]))
                lCRC = struct.unpack("i", data[1020:1024])
                frameData = f.read(lSize) 

                if (sType == self.OAFRAMETYPE_OA):

                    laserInfo = struct.unpack("<ddddiiffIiiiii", frameHeader[0:72]) 
                    (sNumChans, sNumSamplesPerChannel, sDataType, lFrameCounter, sProbeID, sAcquireHardwareID, iSampleRate) = struct.unpack("<hhHIhhi", frameHeader[72:90])

                    a = np.frombuffer(frameData, dtype="<H")
                    a = a.reshape((1216, sNumChans))
                    np.set_printoptions(linewidth=1000, edgeitems=15)
                    print(a)

                    #print(f"DEBUG: {sNumSamplesPerChannel = }, {sNumChans = }")
                    cChannelsReceived = struct.unpack("<32B", frameHeader[90:122])
                    (sFrameStatus, cWavelength, isCalibrationFrame) = struct.unpack("<HBB", frameHeader[122:126])
                    (fLaserEnergy, fGain) = struct.unpack("<ff", frameHeader[190:198])

                    self.metadata[MetadataAcquisitionTags.PULSE_ENERGY].append(fLaserEnergy / 1000) # mJ -> J
                    self.metadata[MetadataAcquisitionTags.MEASUREMENT_TIMESTAMPS].append(iTick / 1000) # msec -> sec

        super().__init__()


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
        if metadatum in self.metadata:
            return self.metadata[metadatum]

