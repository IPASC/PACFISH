import numpy as np
import os
import glob
import struct
import cv2

from pacfish import BaseAdapter, MetaDatum
from pacfish import MetadataAcquisitionTags
from pacfish import DeviceMetaDataCreator, DetectionElementCreator, IlluminationElementCreator

class ImagioFileConverter(BaseAdapter):

    # from OAFrameHeader.h in Seno Imagio Sw
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
    OAFRAME_META_WAVELENGTH_OFFSET = 124
    OAFRAME_META_LASER_ENERGY_OFFSET =  190
    OAFRAME_DATATYPE_SHORT = 2
    OAFRAME_MAX_SAMPLE_NUMBER = 1216

    meta = {}

    """
    For the Seno Imagio system.
    """
    def __init__(self, filename):

        # parse through the entire Laser Optic Movie (.lom) file. see OAFrameHeader.h for binary format.
        with open(filename, "rb") as f:

            self.meta[MetadataAcquisitionTags.PULSE_ENERGY] = []
            self.meta[MetadataAcquisitionTags.MEASUREMENT_TIMESTAMPS] = []
            self.data = []

            print(f"DEBUG: Reading in Seno Imagio Optoacoustic data file '{filename}'")
            while True:
                data = f.read(self.OAFRAME_HEADER_SIZE)

                if not data:
                    break

                # extracted variables (i.e. "sMagic", "iTick", etc..) line up with those defined in ObjectBufferMetaDataDefinitions.h in the Seno Imagio SW
                metaData = (sMagic, sVersion, iTick, lSize, lFrameCounter, sType, sDummy) = struct.unpack("<HHIIIhh", data[0:self.OAFRAME_SUBHEADER_SIZE]) 
                if (sMagic != self.OAFRAME_MAGIC):
                    print(f"ERROR: Unexpected magic number (read 0x{sMagic:04x}, expected 0x{self.OAFRAME_MAGIC:04x})")

                size = self.OAFRAME_HEADER_SIZE - self.OAFRAME_SUBHEADER_SIZE - self.OAFRAME_CRC_SIZE
                start = self.OAFRAME_SUBHEADER_SIZE
                end = self.OAFRAME_HEADER_SIZE - self.OAFRAME_CRC_SIZE
                headerFrameMeta = bytes(struct.unpack(str(size) + "B", data[start:end]))

                lCRC = struct.unpack("i", data[(self.OAFRAME_HEADER_SIZE - self.OAFRAME_CRC_SIZE):self.OAFRAME_HEADER_SIZE])
                frameData = f.read(lSize) 

                if (sType == self.OAFRAMETYPE_OA): # Opto-Acoustic frame

                    (sNumChans, sNumSamplesPerChannel, sDataType, lFrameCounter, sProbeID, sAcquireHardwareID, iSampleRate) = \
                        struct.unpack("<hhHIhhi", headerFrameMeta[self.OAFRAME_META_LASER_INFO_OFFSET:self.OAFRAME_META_SAMPLE_INFO_OFFSET])
                    cWavelength = struct.unpack("<B", headerFrameMeta[self.OAFRAME_META_WAVELENGTH_OFFSET:self.OAFRAME_META_WAVELENGTH_OFFSET+1])[0] # 1 = Alex, 2 = YAG
                    fLaserEnergy = struct.unpack("<f", headerFrameMeta[self.OAFRAME_META_LASER_ENERGY_OFFSET:self.OAFRAME_META_LASER_ENERGY_OFFSET+4])[0]

                    if (sDataType != self.OAFRAME_DATATYPE_SHORT):
                        print("WARNING: Data type ({sDataType}) not as expected for frame.  Skipping to next.")
                        continue

                    print(f"DEBUG: {sDataType = }, {sNumSamplesPerChannel = }, {sNumChans = }, {lSize = }, {cWavelength = }, {len(frameData) = }")
                    frameData = frameData[:-((self.OAFRAME_MAX_SAMPLE_NUMBER - sNumSamplesPerChannel)*sNumChans*2)] # throw away data not from the pulse (because pulses are variable length from shot to shot)
                    self.data.append([cWavelength, np.frombuffer(frameData, dtype=np.int16).reshape((sNumChans, sNumSamplesPerChannel))])
               
                    folder = "output"
                    if (not os.path.exists(folder)):
                        os.mkdir(folder)
                    file = folder + "/oa_" + str(iTick) + ".png"
                    cv2.imwrite(file, self.data[-1][1])
                    print(f"DEBUG: Wrote file '{file}' for OA frame with timestamp {iTick}")

                    self.meta[MetadataAcquisitionTags.PULSE_ENERGY].append(fLaserEnergy / 1000) # mJ -> J
                    self.meta[MetadataAcquisitionTags.MEASUREMENT_TIMESTAMPS].append(iTick / 1000) # msec -> sec

                elif (sType == self.OAFRAMETYPE_US): # Ultrasound frame

                    (w, h, ss) = struct.unpack("<iii", headerFrameMeta[28:40]) # width, height and sample size
                    print(f"DEBUG: {len(frameData) = }, {w = }, {h = }, {ss = }")

                    folder = "output"
                    if (not os.path.exists(folder)):
                        os.mkdir(folder)
                    file = folder + "/us_" + str(iTick) + ".png"
    
                    # TODO write into ancillary array
                    cv2.imwrite(file, np.frombuffer(frameData[0:h*w], dtype=np.uint8).reshape(h, w))
                    print(f"DEBUG: Wrote file '{file}' for US frame with timestamp {iTick}")


            # DEBUG
            #np.set_printoptions(linewidth=1000, edgeitems=15)
            #print(self.data)

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
        return self.data

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
        if metadatum in self.meta:
            return self.meta[metadatum]

