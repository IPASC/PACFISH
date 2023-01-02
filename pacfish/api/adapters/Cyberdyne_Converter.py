# SPDX-FileCopyrightText: 2023 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-FileCopyrightText: 2023 Janek Gröhl
# SPDX-License-Identifier: BSD 3-Clause License

import numpy as np
from scipy.io import loadmat

from pacfish import BaseAdapter, MetaDatum
from pacfish import MetadataAcquisitionTags
from pacfish import DeviceMetaDataCreator, DetectionElementCreator, IlluminationElementCreator


class CyberdyneConverter(BaseAdapter):
    """
    This converter assumes a linear transducer with 128 elements and an element pitch of 0.315mm.
    It assumes that a MAT file contains the following fields:
       - "Sinogram" with the time series data
       - "Fs" with the sampling rate
       - "Ns" with the number of detectors
       - "Nt" with the number of time samples
    """

    def __init__(self, file_path):
        self.file_path = file_path
        data = loadmat(file_path)

        self.sampling_rate = data["Fs"].item()
        self.pitch = data["Pitch"].item()
        self.n_elements = data["Ns"].item()
        self.n_samples = data["Nt"].item()
        self.data = np.swapaxes(data["Sinogram"], 0, 1).astype(float)
        self.data = np.reshape(self.data, (self.n_elements, -1,  1, 1))

        super().__init__()

    def generate_binary_data(self) -> np.ndarray:
        return self.data

    def generate_device_meta_data(self) -> dict:
        device_creator = DeviceMetaDataCreator()

        device_creator.set_general_information(uuid="Cyberdyne Device",
                                               fov=np.asarray([-2,
                                                               2,
                                                               0, 0, 0, 4]))

        start_position = -self.pitch * (self.n_elements/2) + (self.pitch/2)
        for element_idx in range(self.n_elements):
            cur_position = start_position + self.pitch * element_idx
            detection_element_creator = DetectionElementCreator()
            detection_element_creator.set_detector_position(np.asarray([cur_position, 0, 0]))
            detection_element_creator.set_detector_orientation(np.asarray([0, 0, 1]))
            detection_element_creator.set_detector_geometry_type("CUBOID")
            detection_element_creator.set_detector_geometry(np.asarray([0.00003, 0.00003, 0.00001]))

            device_creator.add_detection_element(detection_element_creator.get_dictionary())

        return device_creator.finalize_device_meta_data()

    def set_metadata_value(self, metadatum: MetaDatum) -> object:
        if metadatum == MetadataAcquisitionTags.UUID:
            return "Cyberdyne Device"
        elif metadatum == MetadataAcquisitionTags.DATA_TYPE:
            return str(self.data.dtype)
        elif metadatum == MetadataAcquisitionTags.AD_SAMPLING_RATE:
            return self.sampling_rate
        elif metadatum == MetadataAcquisitionTags.ACOUSTIC_COUPLING_AGENT:
            return "Water"
        elif metadatum == MetadataAcquisitionTags.ACQUISITION_WAVELENGTHS:
            return np.asarray([700])
        elif metadatum == MetadataAcquisitionTags.COMPRESSION:
            return "None"
        elif metadatum == MetadataAcquisitionTags.DIMENSIONALITY:
            return "time"
        elif metadatum == MetadataAcquisitionTags.ENCODING:
            return "raw"
        elif metadatum == MetadataAcquisitionTags.SCANNING_METHOD:
            return "Freehand"
        elif metadatum == MetadataAcquisitionTags.PHOTOACOUSTIC_IMAGING_DEVICE_REFERENCE:
            return "Cyberdyne Device"
        elif metadatum == MetadataAcquisitionTags.SIZES:
            return np.asarray([self.n_elements, self.n_samples, 1, 1])
        else:
            return None
