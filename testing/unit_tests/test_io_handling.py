# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-License-Identifier: BSD 3-Clause License

import os
import numpy as np
from unittest.case import TestCase
import pacfish as pf
from testing.unit_tests.utils import create_complete_device_metadata_dictionary, \
    create_complete_acquisition_meta_data_dictionary, assert_equal_dicts


class IOHandlingTest(TestCase):

    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_write_and_read_random_dictionary(self):

        device_dict = create_complete_device_metadata_dictionary()
        acquisition_dict = create_complete_acquisition_meta_data_dictionary()

        pa_data = pf.PAData(binary_time_series_data=np.zeros([256, 2048]),
                            meta_data_acquisition=acquisition_dict,
                            meta_data_device=device_dict)


        try:
            pf.write_data("ipasc_test.hdf5", pa_data)
            test_data = pf.load_data("ipasc_test.hdf5")
        except Exception as e:
            raise e
        finally:
            # clean up after ipasc_test
            if os.path.exists("ipasc_test.hdf5"):
                os.remove("ipasc_test.hdf5")

        assert_equal_dicts(pa_data.meta_data_acquisition, test_data.meta_data_acquisition)
        assert_equal_dicts(pa_data.meta_data_device, test_data.meta_data_device)
        self.assertTrue((pa_data.binary_time_series_data == test_data.binary_time_series_data).all())

    def test_write_and_read_random_dictionary_with_None_values(self):

        device_dict = create_complete_device_metadata_dictionary()
        acquisition_dict = create_complete_acquisition_meta_data_dictionary()
        acquisition_dict[pf.MetadataAcquisitionTags.MEASUREMENT_TIMESTAMPS.tag] = None
        acquisition_dict[pf.MetadataAcquisitionTags.SCANNING_METHOD.tag] = None

        pa_data = pf.PAData(binary_time_series_data=np.zeros([256, 2048]),
                            meta_data_acquisition=acquisition_dict,
                            meta_data_device=device_dict)

        try:
            pf.write_data("ipasc_test.hdf5", pa_data)
            test_data = pf.load_data("ipasc_test.hdf5")
        except Exception as e:
            raise e
        finally:
            # clean up after ipasc_test
            if os.path.exists("ipasc_test.hdf5"):
                os.remove("ipasc_test.hdf5")

        assert_equal_dicts(pa_data.meta_data_acquisition, test_data.meta_data_acquisition)
        assert_equal_dicts(pa_data.meta_data_device, test_data.meta_data_device)
        self.assertTrue((pa_data.binary_time_series_data == test_data.binary_time_series_data).all())

    def test_overwrite_hdf5_file(self):

        device_dict = create_complete_device_metadata_dictionary()
        acquisition_dict = create_complete_acquisition_meta_data_dictionary()

        pa_data = pf.PAData(binary_time_series_data=np.zeros([256, 2048]),
                            meta_data_acquisition=acquisition_dict,
                            meta_data_device=device_dict)


        try:
            pf.write_data("ipasc_test.hdf5", pa_data)
            test_data_1 = pf.load_data("ipasc_test.hdf5")

            pf.write_data("ipasc_test.hdf5", pa_data)
            test_data_2 = pf.load_data("ipasc_test.hdf5")
        except Exception as e:
            raise e
        finally:
            # clean up after ipasc_test
            if os.path.exists("ipasc_test.hdf5"):
                os.remove("ipasc_test.hdf5")

        assert_equal_dicts(pa_data.meta_data_acquisition, test_data_1.meta_data_acquisition)
        assert_equal_dicts(pa_data.meta_data_device, test_data_1.meta_data_device)
        self.assertTrue((pa_data.binary_time_series_data == test_data_1.binary_time_series_data).all())

        assert_equal_dicts(pa_data.meta_data_acquisition, test_data_2.meta_data_acquisition)
        assert_equal_dicts(pa_data.meta_data_device, test_data_2.meta_data_device)
        self.assertTrue((pa_data.binary_time_series_data == test_data_2.binary_time_series_data).all())
