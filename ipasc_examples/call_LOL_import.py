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
Main interface to load raw files and detector positions
This version is for IPASC adapter

Lawson Optics Lab
Lawson Health Research Institute
Western University
London, ON, Canada

Created by: Lawrence Yip
Last Modified 2021-04-01
"""
# import numpy as np
from ipasc_tool.api.adapters.LawsonOptics import \
    LawsonOpticsLab_360_System_File_Converter
# import matplotlib.pylab as plt
from ipasc_tool import write_data
from ipasc_tool import quality_check_pa_data
# from ipasc_examples.visualize_device import visualize_device
from pathlib import Path
import os

filepath = os.path.join("C:/Users/jgroe/Downloads", "lawrence_data/")

demo_file_path = filepath + "/LOL_demo"
log_file_path = demo_file_path + "/log_2020-10-07-17-18-07.csv"
home_pos_path = demo_file_path + "/Transducer_Position_Home.mat"

converter = LawsonOpticsLab_360_System_File_Converter.LOLFileConverter(demo_file_path, log_file_path, home_pos_path,
                             [680], signal_inv=True, left_shift=12, thresholding=0, photodiode=65, CheckAveraging=True,
                             end_remove=80, numIllum=2, Method = 'trans', fluence_correc = False, 
                             scanIllumSwitch="Scanned", fixed_illum_file_path=None)

pa_data = converter.generate_pa_data()

quality_check_pa_data(pa_data, verbose=True, log_file_path="")

write_data("demodataLOL.hdf5", pa_data)

import numpy as np
import matplotlib.pyplot as plt
from ipasc_examples.visualize_device import visualize_device

print(np.shape(pa_data.binary_time_series_data))

binary = np.rot90(pa_data.binary_time_series_data[:, :], -1)
binary = binary - np.min(binary) + 1
binary = np.log10(binary)
plt.imshow(binary, aspect=0.08)
plt.show()
plt.close()

visualize_device(pa_data.meta_data_device)
