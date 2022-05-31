import os
import numpy as np
from pacfish.api.adapters.Imagio_File_Converter import ImagioFileConverter
from pacfish import write_data
from pacfish import quality_check_pa_data

# input file is a Laser Optic Movie (LOM) from a scan of a phantom using the Seno Imagio system
converter = ImagioFileConverter('./examples/python/input/I0000001.dcm.lom')
#converter = ImagioFileConverter('./examples/python/input/frame2-5.lom')

pa_data = converter.generate_pa_data()

write_data("imagio_ipasc.hdf5", pa_data)


