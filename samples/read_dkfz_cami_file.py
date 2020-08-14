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
from ipasc_tool.api.adapters.DKFZ_CAMI_Experimental_System_Nrrd_File_Converter import DKFZCAMIExperimentalSystemNrrdFileConverter
import matplotlib.pylab as plt
from ipasc_tool import write_data

URL = "http://mitk.org/download/demos/PhotonicsWest2018/demoDataPhantomPA.nrrd"

if not os.path.exists('demodata.nrrd'):
    r = requests.get(URL, allow_redirects=True)
    with open('demodata.nrrd', 'wb') as demo_file:
        demo_file.write(r.content)

converter = DKFZCAMIExperimentalSystemNrrdFileConverter('demodata.nrrd')

pa_data = converter.generate_pa_data()

write_data("demodata.hdf5", pa_data)

print(pa_data)
binary = np.rot90(pa_data.binary_time_series_data[:, :, 0], -1)
plt.imshow(binary, aspect=0.04, vmin=-10000, vmax=10000)
plt.show()
plt.close()

