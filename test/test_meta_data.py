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
from ipasc_tool import MetadataDeviceTags
from ipasc_tool import CompletenessChecker
from test.utils import create_complete_device_metadata_dictionary
import numpy as np


class MetaDataTest(TestCase):

    def setUp(self):
        self.completeness_checker = CompletenessChecker()
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_completenes_checker_device(self):
        device_dictionary = create_complete_device_metadata_dictionary()
        assert self.completeness_checker.check_meta_data_device(device_dictionary, False, "")

        device_dictionary[MetadataDeviceTags.GENERAL.info.tag][MetadataDeviceTags.UUID.info.tag] = None
        assert not self.completeness_checker.check_meta_data_device(device_dictionary, True, "")

        device_dictionary = create_complete_device_metadata_dictionary()
        assert self.completeness_checker.check_meta_data_device(device_dictionary, False, "")

        device_dictionary[MetadataDeviceTags.GENERAL.info.tag].pop(MetadataDeviceTags.UUID.info.tag)
        assert not self.completeness_checker.check_meta_data_device(device_dictionary, False, "")

        os.remove(self.completeness_checker.save_file_name)
