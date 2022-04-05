import numpy as np
import os
import glob
import struct
import cv2

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
    OAFRAME_HEADER_SIZE = 1024
    OAFRAME_SUBHEADER_SIZE = 20
    OAFRAME_CRC_SIZE = 4 
    OAFRAME_META_LASER_INFO_OFFSET = 72
    OAFRAME_META_SAMPLE_INFO_OFFSET = 90
    OAFRAME_META_LASER_ENERGY_OFFSET =  190
    OAFRAME_DATATYPE_SHORT = 2
    OAFRAME_MAX_SAMPLE_NUMBER = 1216

    metadata = {}

    """
    For the Seno Imagio system.
    """
    def __init__(self, filename):

        #
        # TODO:
        # - corresponding ultrasound data as image (already that way in LOM file)
        #
        
        # parse the Laser Optic Movie (.lom) file. see OAFrameHeader.h for binary format.
        with open(filename, "rb") as f:

            self.metadata[MetadataAcquisitionTags.PULSE_ENERGY] = []
            self.metadata[MetadataAcquisitionTags.MEASUREMENT_TIMESTAMPS] = []

            while True:
                data = f.read(self.OAFRAME_HEADER_SIZE)

                if not data:
                    break

                metaData = (sMagic, sVersion, iTick, lSize, lFrameCounter, sType, sDummy) = struct.unpack("<HHIIIhh", data[0:self.OAFRAME_SUBHEADER_SIZE]) 
                if (sMagic != self.OAFRAME_MAGIC):
                    print(f"ERROR: Unexpected magic number (read 0x{sMagic:04x}, expected 0x{self.OAFRAME_MAGIC:04x})")

                size = self.OAFRAME_HEADER_SIZE - self.OAFRAME_SUBHEADER_SIZE - self.OAFRAME_CRC_SIZE
                start = self.OAFRAME_SUBHEADER_SIZE
                end = self.OAFRAME_HEADER_SIZE - self.OAFRAME_CRC_SIZE
                headerFrameMeta = bytes(struct.unpack(str(size) + "B", data[start:end]))

                lCRC = struct.unpack("i", data[(self.OAFRAME_HEADER_SIZE - self.OAFRAME_CRC_SIZE):self.OAFRAME_HEADER_SIZE])
                frameData = f.read(lSize) 

                if (sType == self.OAFRAMETYPE_OA):

                    (sNumChans, sNumSamplesPerChannel, sDataType, lFrameCounter, sProbeID, sAcquireHardwareID, iSampleRate) = \
                        struct.unpack("<hhHIhhi", headerFrameMeta[self.OAFRAME_META_LASER_INFO_OFFSET:self.OAFRAME_META_SAMPLE_INFO_OFFSET])
                    fLaserEnergy = struct.unpack("<f", headerFrameMeta[self.OAFRAME_META_LASER_ENERGY_OFFSET:(self.OAFRAME_META_LASER_ENERGY_OFFSET + 4)])[0]

                    if (sDataType != self.OAFRAME_DATATYPE_SHORT):
                        print("WARNING: Data type ({sDataType}) not as expected for frame.  Skipping to next.")
                        continue

                    # len(frameData) = OAFRAME_MAX_SAMPLE_NUMBER * sNumChans (128) * 2 (size of short)
                    print(f"DEBUG: {sDataType = }, {sNumSamplesPerChannel = }, {sNumChans = }, {lSize = }, {len(frameData) = }")
                    frameData = frameData[:-((self.OAFRAME_MAX_SAMPLE_NUMBER - sNumSamplesPerChannel)*sNumChans*2)] # throw away data not from the pulse (because pulses are variable length from shot to shot)
                    self.binary_data = np.frombuffer(frameData, dtype=np.int16)
                    self.binary_data = self.binary_data.reshape((sNumChans, sNumSamplesPerChannel))
                    cv2.imwrite("out" + str(iTick) + ".png", self.binary_data)
                    np.set_printoptions(linewidth=1000, edgeitems=15)
                    print(self.binary_data)

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
        # TODO add other requested data
        return self.binary_data

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

