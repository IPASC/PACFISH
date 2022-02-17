import os
import numpy as np
from testing.adapters.utils import create_nrrd_file
from pacfish.api.adapters.Imagio_File_Converter import ImagioFileConverter
from pacfish import write_data
from pacfish import quality_check_pa_data
from pacfish.visualize_device import visualize_device

converter = ImagioFileConverter('imagio_raw.bin')

pa_data = converter.generate_pa_data()

# write_data("imagio_ipasc.hdf5", pa_data)

