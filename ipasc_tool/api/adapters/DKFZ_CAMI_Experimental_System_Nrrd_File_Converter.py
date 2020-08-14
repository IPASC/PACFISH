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

from ipasc_tool import BaseAdapter, MetaDatum, MetadataAcquisitionTags


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
        dictionary = dict()

        return dictionary

    def set_metadata_value(self, metadata_tag: MetaDatum) -> object:
        if metadata_tag.tag == MetadataAcquisitionTags.UUID.info.tag:
            return "TestUUID"
        elif metadata_tag.tag == MetadataAcquisitionTags.DATA_TYPE:
            return self.meta['type']
