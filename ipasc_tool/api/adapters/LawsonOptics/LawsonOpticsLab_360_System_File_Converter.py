# -*- coding: utf-8 -*-

# BSD 3-Clause License
#
# Copyright (c) 2020, Lawson Health Research Institute
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

"""
File converter/adapter
Converts into IPASC HDF5 format

Lawson Optics Lab
Lawson Health Research Institute
Western University
London, ON, Canada

Created by: Lawrence Yip
Last Modified 2020-10-05
"""
import numpy as np


from ipasc_tool import BaseAdapter, MetaDatum
from ipasc_tool import MetadataAcquisitionTags
from ipasc_tool import DeviceMetaDataCreator, DetectionElementCreator, IlluminationElementCreator
# from ipasc_tool import read_LOL_import_module
from ipasc_tool.api.adapters.LawsonOptics import read_LOL_import_module as LOL


class LOLFileConverter(BaseAdapter):

    def __init__(self, raw_data_folder_path, scan_log_file_path, homePath, wavelength, signal_inv=True, left_shift=12,
                 thresholding=0, photodiode=65, CheckAveraging=True, end_remove=80, numIllum = 2, scanIllumSwitch = "Scanned", 
                 fixed_illum_file_path = None):
       
        self.raw_data_folder_path = raw_data_folder_path #absolute path?
        self.scan_log_file_path = scan_log_file_path #absolute path? 
        self.homePath = homePath #absolute path? of home position file (of illuminators and detectors)
        self.signal_inv = signal_inv # whether to flip polarity of signals (yes for current system)
        self.left_shift = left_shift # account for delay between laser Q-switch trigger and actual firing of laser
        self.thresholding = thresholding # whether to threshold out noise. 0 = none
        self.photodiode = photodiode # Which channel the photodiode signal power level is in
        self.CheckAveraging = CheckAveraging # Were serial acquisitions performed in each raw file for averaging?
        self.end_remove = end_remove # how many points at the end of each acquisition to zero?
        self.numIllum = numIllum # how many physical illuminators were used?
        self.scanIllumSwitch = scanIllumSwitch # Check if the illuminators were fixed or scanned with the array ("Scanned" or "Fixed")
        self.wavelength = wavelength # wavelengths used for the scan. np.ndarray
        self.fixed_illum_file_path = fixed_illum_file_path # if fixed illuminators, link to .m or .h5 file with positions
        super().__init__() 
        
        

    def generate_binary_data(self) -> np.ndarray:
        import pandas as pd
        scan_positions = pd.read_csv(self.scan_log_file_path)
        num_scans = scan_positions.shape[0] # Determine number of scans based on log file
        # Load data 
        RFdata = LOL.import_and_process_binary(self.raw_data_folder_path, num_scans, self.signal_inv, self.left_shift,
                 self.thresholding, self.photodiode, self.CheckAveraging, self.end_remove, fluence_correc=False)
        RFdata = np.swapaxes(RFdata,1,2) # swap axes to make it easier to reshape
        RFdata = np.reshape(RFdata,(np.shape(RFdata)[0]*np.shape(RFdata)[1],-1),order = "C") # reshape to squash scan number and detectors into one dimension
        
        return RFdata

    def generate_meta_data_device(self) -> dict:
        device_creator = DeviceMetaDataCreator()

        all_positions, illum_positions, time_taken = LOL.load_scan_log(self.scan_log_file_path, self.homePath) #call file to load scan log, return all positions of illum and det
        all_positions_metres = all_positions/1000 # convert to metres
        illum_positions_metres = illum_positions/1000 # convert to metres

        #add general device meta, FOV is approximate
        device_creator.set_general_information(uuid="97cc5c0d-2a83-4935-9820-2aa2161ff703",
                                               fov=np.asarray([-0.025, 0.025, 0.435, 0.485, -20, 30]))
        # Waiting for base adapter to be updated
        # device_creator.set_general_information(uuid="97cc5c0d-2a83-4935-9820-2aa2161ff703",
        #                                        fov=np.asarray([-0.025, 0.025, 0.435, 0.485, -20, 30]), 
        #                                        illumination_elements = self.numIllum*np.shape(illum_positions)[2], detection_elements = 64*np.shape(all_positions)[2])


        
        #Add detector elements, looping through all elements at each scan position
        for scan_position in range(np.shape(all_positions)[2]):
            for detector_position in range(np.shape(all_positions)[0]):
                
                detection_element_creator = DetectionElementCreator()
                detection_element_creator.set_detector_position(all_positions_metres[detector_position,0:3,scan_position])
                # Calculate orientation vector for each element(position)
                orientation = LOL.findVec(all_positions_metres[detector_position, 0:3, scan_position],all_positions_metres[detector_position, 3:6, scan_position], unitSphere = True)
                detection_element_creator.set_detector_orientation(np.asarray(orientation))
                
                #Note needs to be changed to detector_shape once the base adapter is updated
                
                detection_element_creator.set_detector_shape([0.007]) # assume 14mm elements, approx.
                #Add once freq response confirmed
                # detection_element_creator.set_frequency_response(np.stack([np.linspace(700, 900, 100),
                #                                                            np.ones(100)]))
                # detection_element_creator.set_angular_response(np.stack([np.linspace(700, 900, 100),
                #                                                          np.ones(100)]))
    
                device_creator.add_detection_element("detection_element_scan_" + str(scan_position) + "_detector_" + str(detector_position),  
                                                        detection_element_creator.get_dictionary())


        # #Add illumination elements, looping through all elements at each scan position
        # if self.scanIllumSwitch == "Fixed": #if illumination sources are fixed throughout the scan
        #     try:
        #         import tables
        #         file = tables.open_file(self.fixed_illum_file_path)
        #         illum_positions_metres = file.root.illum_positions[:]/1000
        #         centre_fixed_illum = file.root.centre_fixed_illum[:]/1000
        #     except:
        #         import scipy.io as sio
        #         homepos = sio.loadmat(self.fixed_illum_file_path)
        #         illum_positions_metres = homepos.get("illum_positions")/1000
        #         centre_fixed_illum = homepos.get("centre_fixed_illum")/1000
                
        #     for illum_position in range(self.numIllum):
        #         illumination_element_creator = IlluminationElementCreator()
        #         # illumination_element_creator.set_beam_divergence_angles(0.20944) #arbitrary
        #         illumination_element_creator.set_wavelength_range(np.asarray([680, 950, 1]))
        #         illumination_element_creator.set_illuminator_position(illum_positions_metres[illum_position,:])
        #         # Calculate orientation vector for each element(position)
        #         orientation = LOL.findVec(illum_positions_metres[illum_position,:], centre_fixed_illum[:], unitSphere = True)
        #         illumination_element_creator.set_illuminator_orientation(np.asarray(orientation))
        #         illumination_element_creator.set_illuminator_shape(np.asarray([0.0015])) #assume 3mm exit fibre bundle
        #         # illumination_element_creator.set_laser_energy_profile(np.stack([np.linspace(700, 900, 100),
        #         #                                                                 np.ones(100)]))
        #         # illumination_element_creator.set_laser_stability_profile(np.stack([np.linspace(700, 900, 100),
        #         #                                                                     np.ones(100)]))
        #         illumination_element_creator.set_pulse_width(6e-9)
        #         device_creator.add_illumination_element("illuminator_" + str(illum_position),
        #                                                 illumination_element_creator.get_dictionary())
        # elif self.scanIllumSwitch == "Scanned":# for moving elements
        #     for scan_position in range(np.shape(all_positions)[2]): 
        #         for illum_position in range(self.numIllum):
        #             illumination_element_creator = IlluminationElementCreator()
        #             # illumination_element_creator.set_beam_divergence_angles(0.20944) #arbitrary
        #             illumination_element_creator.set_wavelength_range(np.asarray([680, 950, 1]))
        #             illumination_element_creator.set_illuminator_position(illum_positions_metres[illum_position,0:3,scan_position])
        #             # Calculate orientation vector for each element(position)
        #             orientation = LOL.findVec(illum_positions_metres[illum_position, 0:3, scan_position],illum_positions_metres[illum_position, 3:6, scan_position], unitSphere = True)
        #             illumination_element_creator.set_illuminator_orientation(np.asarray(orientation))
        #             illumination_element_creator.set_illuminator_shape(np.asarray([0.0015])) #assume 3mm exit fibre bundle
        #             # illumination_element_creator.set_laser_energy_profile(np.stack([np.linspace(700, 900, 100),
        #             #                                                                 np.ones(100)]))
        #             # illumination_element_creator.set_laser_stability_profile(np.stack([np.linspace(700, 900, 100),
        #             #                                                                     np.ones(100)]))
        #             illumination_element_creator.set_pulse_width(6e-9)
        #             device_creator.add_illumination_element("illumination_element_scan_" + str(scan_position) + "_illuminator_" + str(illum_position),
        #                                                     illumination_element_creator.get_dictionary())

        return device_creator.finalize_device_meta_data()

    def set_metadata_value(self, metadata_tag: MetaDatum) -> object:
        if metadata_tag == MetadataAcquisitionTags.UUID:
            return "04cdc4f2-3d55-49c6-b871-aea9e6dc380f"
        elif metadata_tag == MetadataAcquisitionTags.DATA_TYPE:
            return "float"
        elif metadata_tag == MetadataAcquisitionTags.AD_SAMPLING_RATE:
            return 50000000.0
        elif metadata_tag == MetadataAcquisitionTags.ACOUSTIC_COUPLING_AGENT:
            return "Water"
        elif metadata_tag == MetadataAcquisitionTags.ACQUISITION_OPTICAL_WAVELENGTHS:
            return self.wavelength
        elif metadata_tag == MetadataAcquisitionTags.COMPRESSION:
            return "None"
        elif metadata_tag == MetadataAcquisitionTags.DIMENSIONALITY:
            return "N/A"
        elif metadata_tag == MetadataAcquisitionTags.ENCODING:
            return "UTF-8’"
        elif metadata_tag == MetadataAcquisitionTags.SCANNING_METHOD:
            return "6DoF robotic, translation + rotation"
        elif metadata_tag == MetadataAcquisitionTags.PHOTOACOUSTIC_IMAGING_DEVICE:
            return "97cc5c0d-2a83-4935-9820-2aa2161ff703"
        # elif metadata_tag == MetadataAcquisitionTags.SIZES:
        #     return np.asarray(self.meta['sizes'])
        else:
            return None
