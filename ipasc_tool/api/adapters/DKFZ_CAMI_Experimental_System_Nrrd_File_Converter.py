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

from ipasc_tool import BaseAdapter, MetaDatum
from ipasc_tool import MetadataAcquisitionTags
from ipasc_tool import DeviceMetaDataCreator, DetectionElementCreator, IlluminationElementCreator


class DKFZCAMIExperimentalSystemNrrdFileConverter(BaseAdapter):

    def __init__(self, nrrd_file_path):
        super().__init__()
        self.nrrd_file_path = nrrd_file_path
        [data, meta] = nrrd.read(nrrd_file_path)
        self.data = data
        self.meta = meta
        print(self.meta)

    def generate_binary_data(self) -> np.ndarray:
        return self.data

    def generate_meta_data_device(self) -> dict:
        device_creator = DeviceMetaDataCreator()

        device_creator.set_general_information(uuid="c771111c-36ba-425d-9f53-84b8ff092059",
                                               fov=np.asarray([0.0384, 0, 0.0384]))

        start_y_position = 0.00015
        for y_idx in range(128):
            cur_y_position = start_y_position + 0.0003 * y_idx
            detection_element_creator = DetectionElementCreator()
            detection_element_creator.set_detector_position(np.asarray([cur_y_position, 0, 0]))
            detection_element_creator.set_detector_orientation(np.asarray([0, 0, 1]))
            detection_element_creator.set_detector_size(np.asarray([0.0003, 0.0003, 0.0003]))

            device_creator.add_detection_element("detection_element_" + str(y_idx),
                                                 detection_element_creator.get_dictionary())

        for y_idx in range(2):
            illumination_element_creator = IlluminationElementCreator()
            illumination_element_creator.set_beam_divergence_angles(0.20944)
            illumination_element_creator.set_wavelength_range(np.asarray([700, 950, 1]))
            if y_idx == 0:
                illumination_element_creator.set_illuminator_position(np.asarray([0.0192, 0.0083, -0.001]))
                illumination_element_creator.set_illuminator_orientation(np.asarray([0, -0.383972, 0]))
            elif y_idx == 1:
                illumination_element_creator.set_illuminator_position(np.asarray([0.0192, -0.0083, -0.001]))
                illumination_element_creator.set_illuminator_orientation(np.asarray([0, 0.383972, 0]))
            illumination_element_creator.set_illuminator_shape(np.asarray([0.0245, 0, 0]))
            device_creator.add_illumination_element("illumination_element_" + str(y_idx),
                                                    illumination_element_creator.get_dictionary())

        return device_creator.finalize_device_meta_data()

    def set_metadata_value(self, metadata_tag: MetaDatum) -> object:
        if metadata_tag == MetadataAcquisitionTags.UUID:
            return "TestUUID"
        elif metadata_tag == MetadataAcquisitionTags.DATA_TYPE:
            return self.meta['type']
