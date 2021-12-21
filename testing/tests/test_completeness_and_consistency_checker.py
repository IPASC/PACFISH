# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-License-Identifier: BSD 3-Clause License

import numpy as np
from unittest.case import TestCase
from pacfish import PAData, CompletenessChecker, ConsistencyChecker, MetadataDeviceTags, MetadataAcquisitionTags
from testing.tests.utils import create_complete_device_metadata_dictionary, create_complete_acquisition_meta_data_dictionary


class CompletenessAndConsistencyTest(TestCase):

    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_check_a_complete_and_consistent_pa_data_instance(self):
        device_dict = create_complete_device_metadata_dictionary()
        acquisition_dict = create_complete_acquisition_meta_data_dictionary()

        pa_data = PAData(binary_time_series_data=np.zeros([256, 2048]),
                         meta_data_acquisition=acquisition_dict,
                         meta_data_device=device_dict)

        completeness_checker = CompletenessChecker(verbose=True)
        consistency_checker = ConsistencyChecker(verbose=True)

        assert completeness_checker.check_acquisition_meta_data(pa_data.meta_data_acquisition)
        assert completeness_checker.check_device_meta_data(pa_data.meta_data_device)

        assert consistency_checker.check_binary_data(pa_data.binary_time_series_data)
        assert consistency_checker.check_acquisition_meta_data(pa_data.meta_data_acquisition)
        assert consistency_checker.check_device_meta_data(pa_data.meta_data_device)

    def test_check_a_complete_but_inconsistent_pa_data_instance(self):
        device_dict = create_complete_device_metadata_dictionary()
        for illuminator_tag in device_dict[MetadataDeviceTags.ILLUMINATORS.tag]:
            device_dict[MetadataDeviceTags.ILLUMINATORS.tag][illuminator_tag]\
                [MetadataDeviceTags.PULSE_WIDTH.tag] = -0.1
        acquisition_dict = create_complete_acquisition_meta_data_dictionary()
        acquisition_dict[MetadataAcquisitionTags.DIMENSIONALITY.tag] = "Wrong string"

        pa_data = PAData(binary_time_series_data=np.zeros([256, 2048]),
                         meta_data_acquisition=acquisition_dict,
                         meta_data_device=device_dict)

        completeness_checker = CompletenessChecker(verbose=True)
        consistency_checker = ConsistencyChecker(verbose=True)

        assert completeness_checker.check_acquisition_meta_data(pa_data.meta_data_acquisition)
        assert completeness_checker.check_device_meta_data(pa_data.meta_data_device)

        assert consistency_checker.check_binary_data(pa_data.binary_time_series_data)
        assert consistency_checker.check_acquisition_meta_data(pa_data.meta_data_acquisition) is False
        assert consistency_checker.check_device_meta_data(pa_data.meta_data_device) is False
