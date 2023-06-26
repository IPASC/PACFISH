# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-License-Identifier: BSD 3-Clause License

import os
from unittest.case import TestCase
import pacfish as pf
from testing.unit_tests.utils import assert_equal_dicts


class TestBackwardsCompatibility(TestCase):

    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_read_V1_file(self):

        pa_data = pf.load_data("../data/ipasc_compatible_V1.hdf5")

        self.assertTrue(len(pa_data.binary_time_series_data.shape) == 3)

        try:
            pf.write_data("compatible_ipasc_test.hdf5", pa_data)
            test_data = pf.load_data("compatible_ipasc_test.hdf5")
        except Exception as e:
            raise e
        finally:
            # clean up after ipasc_test
            if os.path.exists("compatible_ipasc_test.hdf5"):
                os.remove("compatible_ipasc_test.hdf5")

        pa_data.meta_data_acquisition[pf.MetadataAcquisitionTags.VERSION.tag] = "V2"

        assert_equal_dicts(pa_data.meta_data_acquisition, test_data.meta_data_acquisition)
        assert_equal_dicts(pa_data.meta_data_device, test_data.meta_data_device)
        self.assertTrue((pa_data.binary_time_series_data == test_data.binary_time_series_data).all())
