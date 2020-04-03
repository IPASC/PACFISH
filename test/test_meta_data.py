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
from unittest.case import TestCase
from core.metadata_tags import MetadataTags
from core.metadata_tags import MetadataDeviceTags
from qualitycontrol.CompletenessChecker import CompletenessChecker
import numpy as np

class MetaDataTest(TestCase):

    def setUp(self):
        self.completeness_checker = CompletenessChecker()
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def create_complete_metadata_dictionary(self):
        dictionary = dict()

        for metadatum in MetadataTags:
            if issubclass(metadatum.info.dtype, str):
                dictionary[metadatum] = "Test"
            elif issubclass(metadatum.info.dtype, np.ndarray):
                dictionary[metadatum] = np.ones(120)
            elif issubclass(metadatum.info.dtype, float):
                dictionary[metadatum] = 17.42

        return dictionary

    def test_completenes_checker(self):
        dictionary = self.create_complete_metadata_dictionary()
        assert self.completeness_checker.check_meta_data(dictionary, True, "")

        dictionary[MetadataTags.UUID] = None
        assert not self.completeness_checker.check_meta_data(dictionary)

        dictionary = self.create_complete_metadata_dictionary()
        assert self.completeness_checker.check_meta_data(dictionary)

        dictionary.pop(MetadataTags.UUID)
        assert not self.completeness_checker.check_meta_data(dictionary)

        os.remove(self.completeness_checker.save_file_name)
