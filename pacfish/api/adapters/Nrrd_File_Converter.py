# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-FileCopyrightText: 2021 Janek Gröhl
# SPDX-License-Identifier: BSD 3-Clause License

import numpy as np
import nrrd

from pacfish import BaseAdapter, MetaDatum
from pacfish import MetadataAcquisitionTags
from pacfish import DeviceMetaDataCreator, DetectionElementCreator, IlluminationElementCreator


class NrrdFileConverter(BaseAdapter):
    """
    This converter assumes a linear transducer with 128 elements and an element pitch of 0.3mm.
    It assumes that the NRRD file metadata contains a 'sizes', 'type' and 'space directions' field.
    """

    def __init__(self, nrrd_file_path):
        self.nrrd_file_path = nrrd_file_path
        [data, meta] = nrrd.read(nrrd_file_path)
        self.data = data
        self.meta = meta

        print(np.shape(data))
        print(meta)

        super().__init__()

    def generate_binary_data(self) -> np.ndarray:
        data = np.reshape(self.data, (self.meta['sizes'][0], self.meta['sizes'][1], 1, self.meta['sizes'][2]))
        return data

    def generate_device_meta_data(self) -> dict:
        device_creator = DeviceMetaDataCreator()

        device_creator.set_general_information(uuid="c771111c-36ba-425d-9f53-84b8ff092059",
                                               fov=np.asarray([0, 0, 0, 0.0384, 0, 0.0384]))

        start_y_position = 0.00015
        for y_idx in range(128):
            cur_y_position = start_y_position + 0.0003 * y_idx
            detection_element_creator = DetectionElementCreator()
            detection_element_creator.set_detector_position(np.asarray([0, cur_y_position, 0]))
            detection_element_creator.set_detector_orientation(np.asarray([0, 0, 1]))
            detection_element_creator.set_detector_geometry_type("CUBOID")
            detection_element_creator.set_detector_geometry(np.asarray([0.0003, 0.0003, 0.0001]))
            detection_element_creator.set_frequency_response(np.asarray([np.linspace(700, 900, 100),
                                                                         np.ones(100)]))
            detection_element_creator.set_angular_response(np.asarray([np.linspace(700, 900, 100),
                                                                       np.ones(100)]))

            device_creator.add_detection_element(detection_element_creator.get_dictionary())

        for y_idx in range(2):
            illumination_element_creator = IlluminationElementCreator()
            illumination_element_creator.set_beam_divergence_angles(0.20944)
            illumination_element_creator.set_wavelength_range(np.asarray([700, 950, 1]))
            if y_idx == 0:
                illumination_element_creator.set_illuminator_position(np.asarray([0.0083, 0.0192, -0.001]))
                illumination_element_creator.set_illuminator_orientation(np.asarray([-0.383972, 0, 1]))
            elif y_idx == 1:
                illumination_element_creator.set_illuminator_position(np.asarray([-0.0083, 0.0192, -0.001]))
                illumination_element_creator.set_illuminator_orientation(np.asarray([0.383972, 0, 1]))
            illumination_element_creator.set_illuminator_geometry(np.asarray([0, 0.025, 0]))
            illumination_element_creator.set_illuminator_geometry_type("CUBOID")

            illumination_element_creator.set_beam_energy_profile(np.asarray([np.linspace(700, 900, 100),
                                                                             np.ones(100)]))
            illumination_element_creator.set_beam_stability_profile(np.asarray([np.linspace(700, 900, 100),
                                                                                np.ones(100)]))
            illumination_element_creator.set_pulse_width(7e-9)
            device_creator.add_illumination_element(illumination_element_creator.get_dictionary())

        return device_creator.finalize_device_meta_data()

    def set_metadata_value(self, metadatum: MetaDatum) -> object:
        if metadatum == MetadataAcquisitionTags.UUID:
            return "TestUUID"
        elif metadatum == MetadataAcquisitionTags.DATA_TYPE:
            return self.meta['type']
        elif metadatum == MetadataAcquisitionTags.AD_SAMPLING_RATE:
            return 1.0 / (float(self.meta['space directions'][1][1]) / 1000000)
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
            return "c771111c-36ba-425d-9f53-84b8ff092059"
        elif metadatum == MetadataAcquisitionTags.SIZES:
            return np.asarray(self.meta['sizes'])
        else:
            return None
