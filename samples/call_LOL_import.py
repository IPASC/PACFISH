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

import os
import numpy as np
import requests
from ipasc_tool.api.adapters.LawsonOpticsLab_360_System_File_Converter import \
    LOLFileConverter
import read_LOL_import_module
import matplotlib.pylab as plt
from ipasc_tool import write_data
from ipasc_tool import quality_check_pa_data
from samples.visualize_device import visualize_device

URL = "http://mitk.org/download/demos/PhotonicsWest2018/demoDataPhantomPA.nrrd"

if not os.path.exists('demodata.nrrd'):
    r = requests.get(URL, allow_redirects=True)
    with open('demodata.nrrd', 'wb') as demo_file:
        demo_file.write(r.content)

converter = DKFZCAMIExperimentalSystemNrrdFileConverter('demodata.nrrd')

pa_data = converter.generate_pa_data()

quality_check_pa_data(pa_data, verbose=True, log_file_path="")

write_data("demodata.hdf5", pa_data)

binary = np.rot90(pa_data.binary_time_series_data[:, 500:-2500, 0], -1)
binary = binary - np.min(binary) + 1
binary = np.log10(binary)
plt.imshow(binary, aspect=0.08, vmin=np.percentile(binary, 1), vmax=np.percentile(binary, 99))
plt.show()
plt.close()

visualize_device(pa_data.meta_data_device)

if os.path.exists("logfile.md"):
    os.remove("logfile.md")
#if os.path.exists("demodata.hdf5"):
#    os.remove("demodata.hdf5")
