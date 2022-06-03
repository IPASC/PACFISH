#
# This file reads an example Laser Optic Movie (LOM) produced by the Seno (https://senomedical.com/) 
# Imagio System and produces an IPASC-compatible HDF5 file.  In addition, if enabled, graphical 
# representations of the data are written as .png files.
#

import os
import numpy as np
import cv2
import pathlib
from pacfish.api.adapters.Imagio_File_Converter import ImagioFileConverter
from pacfish import write_data
from pacfish import quality_check_pa_data

# input file is a Laser Optic Movie (LOM) from a scan of a phantom using the Seno Imagio system
input_file = './examples/python/input/I0000001.dcm.lom' # Gen2 (4 OA frames, 1 US image, hair target)

# other examples
#input_file = './examples/python/input/2017_12_11-10_54_55_0.lom' # Gen1a (many OA frames, many US images, lesion)
#input_file = './examples/python/input/20211102134837219776.dcm.lom' # Gen2 (many OA frames, many US images, hair target)

converter = ImagioFileConverter(input_file) 

pa_data = converter.generate_pa_data()

quality_check_pa_data(pa_data, verbose=True, log_file_path="")

folder = "output/" + os.path.basename(input_file)
pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

output_png = True # disable if needed
if (output_png):
    timestamps = pa_data.get_measurement_time_stamps()
    wavelengths = pa_data.get_acquisition_wavelengths()
    for idx, oa_frame in enumerate(pa_data.binary_time_series_data):
        iTick = str(int(timestamps[idx] * 1E3)) + "_msec"
        wavelength = str(int(wavelengths[idx] * 1E9)) + "_nm"
        file = folder + "/oa_" + str(iTick) + "_" + wavelength + ".png"
        cv2.imwrite(file, (oa_frame+32768)/256)
        print(f"INFO: Wrote file '{file}' for OA frame")

    for idx, us_image in enumerate(pa_data.meta_data_acquisition['ultrasound_image_data']):
        iTick = str(int(pa_data.meta_data_acquisition['ultrasound_image_timestamps'][idx]*1E3)) + "_msec"
        file = folder + "/us_" + str(iTick) + ".png"
        cv2.imwrite(file, us_image)
        print(f"INFO: Wrote file '{file}' for US frame")

file = folder + "/" + os.path.basename(input_file) + "_imagio_ipasc.hdf5"
write_data(file, pa_data)
print(f"INFO: Wrote file '{file}' with IPASC HDF5 data")

