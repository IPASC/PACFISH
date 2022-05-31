import os
import numpy as np
import cv2
from pacfish.api.adapters.Imagio_File_Converter import ImagioFileConverter
from pacfish import write_data
from pacfish import quality_check_pa_data

# input file is a Laser Optic Movie (LOM) from a scan of a phantom using the Seno Imagio system
converter = ImagioFileConverter('./examples/python/input/I0000001.dcm.lom')
#converter = ImagioFileConverter('./examples/python/input/frame2-5.lom')

pa_data = converter.generate_pa_data()

folder = "output"
if (not os.path.exists(folder)):
    os.mkdir(folder)

timestamps = pa_data.get_measurement_time_stamps()
for idx, oa_frame in enumerate(pa_data.binary_time_series_data):
    iTick = timestamps[idx]
    file = folder + "/oa_" + str(iTick) + ".png"
    cv2.imwrite(file, oa_frame)
    print(f"DEBUG: Wrote file '{file}' for OA frame with timestamp {iTick}")

for idx, us_image in enumerate(pa_data.meta_data_acquisition['ultrasound_image_data']):
    iTick = pa_data.meta_data_acquisition['ultrasound_image_timestamps'][idx]
    file = folder + "/us_" + str(iTick) + ".png"
    cv2.imwrite(file, us_image)
    print(f"DEBUG: Wrote file '{file}' for US frame with timestamp {iTick}")
    
write_data("imagio_ipasc.hdf5", pa_data)


