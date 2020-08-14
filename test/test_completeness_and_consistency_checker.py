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
from unittest.case import TestCase
from test.utils import create_complete_device_metadata_dictionary, create_complete_meta_data_dictionary
from ipasc_tool import PAData, CompletenessChecker, ConsistencyChecker, MetadataDeviceTags, MetadataAcquisitionTags


class CompletenessAndConsistencyTest(TestCase):

    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_check_a_complete_and_consistent_pa_data_instance(self):
        device_dict = create_complete_device_metadata_dictionary()
        acquisition_dict = create_complete_meta_data_dictionary()

        pa_data = PAData(time_series_data=np.zeros([256, 2048]),
                         meta_data=acquisition_dict,
                         meta_data_device=device_dict)

        completeness_checker = CompletenessChecker(verbose=True)
        consistency_checker = ConsistencyChecker(verbose=True)

        assert completeness_checker.check_meta_data(pa_data.meta_data)
        assert completeness_checker.check_meta_data_device(pa_data.meta_data_device)

        assert consistency_checker.check_binary(pa_data.binary_time_series_data)
        assert consistency_checker.check_meta_data(pa_data.meta_data)
        assert consistency_checker.check_meta_data_device(pa_data.meta_data_device)

    def test_check_a_complete_but_inconsistent_pa_data_instance(self):
        device_dict = create_complete_device_metadata_dictionary()
        for illuminator_tag in device_dict[MetadataDeviceTags.ILLUMINATORS.tag]:
            device_dict[MetadataDeviceTags.ILLUMINATORS.tag][illuminator_tag]\
                [MetadataDeviceTags.PULSE_WIDTH.tag] = -0.1
        acquisition_dict = create_complete_meta_data_dictionary()
        acquisition_dict[MetadataAcquisitionTags.DIMENSIONALITY.tag] = "Wrong string"

        pa_data = PAData(time_series_data=np.zeros([256, 2048]),
                         meta_data=acquisition_dict,
                         meta_data_device=device_dict)

        completeness_checker = CompletenessChecker(verbose=True)
        consistency_checker = ConsistencyChecker(verbose=True)

        assert completeness_checker.check_meta_data(pa_data.meta_data)
        assert completeness_checker.check_meta_data_device(pa_data.meta_data_device)

        assert consistency_checker.check_binary(pa_data.binary_time_series_data)
        assert consistency_checker.check_meta_data(pa_data.meta_data) is False
        assert consistency_checker.check_meta_data_device(pa_data.meta_data_device) is False
