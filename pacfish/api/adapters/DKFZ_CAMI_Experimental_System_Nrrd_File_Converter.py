# BSD 3-Clause License
#
# Copyright (c) 2020, IPASC
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import numpy as np
import nrrd

from pacfish import BaseAdapter, MetaDatum
from pacfish import MetadataAcquisitionTags
from pacfish import DeviceMetaDataCreator, DetectionElementCreator, IlluminationElementCreator


class DKFZCAMIExperimentalSystemNrrdFileConverter(BaseAdapter):

    def __init__(self, nrrd_file_path):
        self.nrrd_file_path = nrrd_file_path
        [data, meta] = nrrd.read(nrrd_file_path)
        self.data = data
        self.meta = meta

        super().__init__()

    def generate_binary_data(self) -> np.ndarray:
        # the CAMI_DKFZ_FILE is captured this way: [elements, time_series, frames]
        # Needs to be reshaped in order to be in line with the IPASC definition of
        # [detectors, time_series, wavelength, frames]
        # The sample file only contains images with a single wavelength.
        # TODO adapt for multispectral images as well
        data = np.reshape(self.data, (self.meta['sizes'][0], self.meta['sizes'][1], 1, self.meta['sizes'][2]))
        return data

    def generate_meta_data_device(self) -> dict:
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

            illumination_element_creator.set_laser_energy_profile(np.asarray([np.linspace(700, 900, 100),
                                                                            np.ones(100)]))
            illumination_element_creator.set_laser_stability_profile(np.asarray([np.linspace(700, 900, 100),
                                                                               np.ones(100)]))
            illumination_element_creator.set_pulse_width(7e-9)
            device_creator.add_illumination_element(illumination_element_creator.get_dictionary())

        return device_creator.finalize_device_meta_data()

    def set_metadata_value(self, metadata_tag: MetaDatum) -> object:
        if metadata_tag == MetadataAcquisitionTags.UUID:
            return "TestUUID"
        elif metadata_tag == MetadataAcquisitionTags.DATA_TYPE:
            return self.meta['type']
        elif metadata_tag == MetadataAcquisitionTags.AD_SAMPLING_RATE:
            return 1.0 / (float(self.meta['space directions'][1][1]) / 1000000)
        elif metadata_tag == MetadataAcquisitionTags.ACOUSTIC_COUPLING_AGENT:
            return "Water"
        elif metadata_tag == MetadataAcquisitionTags.ACQUISITION_OPTICAL_WAVELENGTHS:
            return np.asarray([700])
        elif metadata_tag == MetadataAcquisitionTags.COMPRESSION:
            return "None"
        elif metadata_tag == MetadataAcquisitionTags.DIMENSIONALITY:
            return "time"
        elif metadata_tag == MetadataAcquisitionTags.ENCODING:
            return "raw"
        elif metadata_tag == MetadataAcquisitionTags.SCANNING_METHOD:
            return "Freehand"
        elif metadata_tag == MetadataAcquisitionTags.PHOTOACOUSTIC_IMAGING_DEVICE:
            return "c771111c-36ba-425d-9f53-84b8ff092059"
        elif metadata_tag == MetadataAcquisitionTags.SIZES:
            return np.asarray(self.meta['sizes'])
        else:
            return None
