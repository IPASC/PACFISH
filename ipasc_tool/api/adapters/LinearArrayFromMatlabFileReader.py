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
from scipy.io import loadmat

from ipasc_tool import BaseAdapter, MetaDatum
from ipasc_tool import MetadataAcquisitionTags
from ipasc_tool import DeviceMetaDataCreator, DetectionElementCreator, IlluminationElementCreator
from ipasc_tool.visualize_device import visualize_device
from ipasc_tool.iohandler import write_data

import matplotlib.pyplot as plt

class LinearArrayTransducerMatlabFile(BaseAdapter):

    def __init__(self, mat_file_path,
                 binary_data_field_name,
                 num_detectors=128,
                 detector_pitch_m=2.5e-4,
                 sampling_rate=41066075.0,
                 speed_of_sound=1540,
                 fov=None):
        self.mat_file_path = mat_file_path
        data = loadmat(self.mat_file_path)
        print(data)
        local_num_detectors = num_detectors
        if "ElementNum" in data:
            local_num_detectors = data["ElementNum"]

        if local_num_detectors != num_detectors:
            print("WARN: The number of detectors extracted from mat file dio not match argument.")
            num_detectors = local_num_detectors

        self.data = data[binary_data_field_name]

        if len(np.shape(self.data)) == 3:
            self.data = np.stack(self.data, axis=2).reshape(-1, num_detectors)

        self.data = np.swapaxes(self.data, 0, 1)
        self.data[:, 0:100] = 0
        self.data = self.data.reshape((num_detectors, -1, 1, 1))
        print(np.shape(self.data))
        print(np.max(self.data), np.min(self.data))
        plt.imshow(self.data[:, :, 0], aspect=12)
        plt.show()

        self.num_elements = num_detectors
        self.sampling_rate = sampling_rate
        self.element_pitch = detector_pitch_m
        self.speed_of_sound = speed_of_sound

        if fov is None:
            self.fov = np.asarray([0,
                                   self.num_elements*self.element_pitch,
                                   0,
                                   0,
                                   0,
                                   self.num_elements*self.element_pitch * 1.5])
        else:
            self.fov = fov

        super().__init__()

    def generate_binary_data(self) -> np.ndarray:
        # Needs to be reshaped in order to be in line with the IPASC definition of
        # [detectors, time_series, wavelength, frames]
        # The sample file only contains images with a single wavelength.
        # TODO adapt for multispectral images as well
        return self.data

    def generate_meta_data_device(self) -> dict:
        device_creator = DeviceMetaDataCreator()

        device_creator.set_general_information(uuid="c771111c-36ba-425d-9f53-84b8ff092059",
                                               fov=self.fov)

        start_x_position = self.element_pitch/2
        for x_idx in range(self.num_elements):
            cur_x_position = start_x_position + self.element_pitch * x_idx
            detection_element_creator = DetectionElementCreator()
            detection_element_creator.set_detector_position(np.asarray([cur_x_position, 0, 0]))
            detection_element_creator.set_detector_orientation(np.asarray([0, 0, 1]))
            detection_element_creator.set_detector_geometry_type("CUBOID")
            detection_element_creator.set_detector_geometry(np.asarray([self.element_pitch, self.element_pitch, 0.0001]))
            device_creator.add_detection_element(detection_element_creator.get_dictionary())

        return device_creator.finalize_device_meta_data()

    def set_metadata_value(self, metadata_tag: MetaDatum) -> object:
        if metadata_tag == MetadataAcquisitionTags.UUID:
            return "TestUUID"
        elif metadata_tag == MetadataAcquisitionTags.DATA_TYPE:
            return str(type(self.data))
        elif metadata_tag == MetadataAcquisitionTags.AD_SAMPLING_RATE:
            return self.sampling_rate
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
            return np.asarray(np.shape(self.data))
        elif metadata_tag == MetadataAcquisitionTags.ASSUMED_GLOBAL_SPEED_OF_SOUND:
            return self.speed_of_sound
        else:
            return None


# # Read manojits data:
# if __name__=="__main__":
#     path = r"C:\Users\grohl01\Downloads\PA_Recon_handHeldPAT_LinearArray\PA_Recon_handHeldPAT_LinearArray\
#     1_layer0_idx1_BDATA_RF.mat"
#     converter = LinearArrayTransducerMatlabFile(mat_file_path=path,
#                                                 binary_data_field_name="AdcData_frame000",
#                                                 num_detectors=128,
#                                                 detector_pitch_m=0.0003,
#                                                 sampling_rate=40 * 1e6,
#                                                 speed_of_sound=1540
#                                                )
#     pa_data = converter.generate_pa_data()
#     visualize_device(pa_data.meta_data_device)
#     write_data(r"C:\Users\grohl01\Downloads\PA_Recon_handHeldPAT_LinearArray\PA_Recon_handHeldPAT_LinearArray\
#     1_layer0_idx1_BDATA_RF.hdf5", pa_data)
#
#
# # Read Francois data:
# if __name__=="__main__":
#     path = r"C:\Users\grohl01\Downloads\IPASC_simulation_fvarray.mat"
#     converter = LinearArrayTransducerMatlabFile(mat_file_path=path,
#                                                 binary_data_field_name="raw",
#                                                 num_detectors=128,
#                                                 detector_pitch_m=2.5e-4,
#                                                 sampling_rate=41066075,
#                                                 speed_of_sound=1540
#                                                )
#     pa_data = converter.generate_pa_data()
#     visualize_device(pa_data.meta_data_device)
#     write_data(r"C:\Users\grohl01\Downloads\IPASC_simulation_fvarray.hdf5", pa_data)


# Read Mengjie data A:
if __name__=="__main__":
    path = r"C:\Users\grohl01\Downloads\IPASC-testdata\PS-carbonfibres.mat"
    converter = LinearArrayTransducerMatlabFile(mat_file_path=path,
                                                binary_data_field_name="DataAfterAvePA",
                                                num_detectors=128,
                                                detector_pitch_m=3e-4,
                                                sampling_rate=40000000,
                                                speed_of_sound=1540,
                                                fov=np.asarray([0, 0.04, 0, 0, 0.005, 0.04]))
    pa_data = converter.generate_pa_data()
    visualize_device(pa_data.meta_data_device)
    write_data(r"C:\Users\grohl01\Downloads\IPASC-testdata\PS-carbonfibres.hdf5", pa_data)

# Read Mengjie data B:
if __name__ == "__main__":
    path = r"C:\Users\grohl01\Downloads\IPASC-testdata\PS-PencilLead0.5mm.mat"
    converter = LinearArrayTransducerMatlabFile(mat_file_path=path,
                                                binary_data_field_name="DataAfterAvePA",
                                                num_detectors=128,
                                                detector_pitch_m=3e-4,
                                                sampling_rate=40000000,
                                                speed_of_sound=1540,
                                                fov=np.asarray([0, 0.04, 0, 0, 0.005, 0.04]))
    pa_data = converter.generate_pa_data()
    visualize_device(pa_data.meta_data_device)
    write_data(r"C:\Users\grohl01\Downloads\IPASC-testdata\PS-PencilLead0.5mm.hdf5", pa_data)
