# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-License-Identifier: BSD 3-Clause License
import unittest

import numpy as np
from unittest.case import TestCase
import pacfish as pf
from testing.tests.utils import create_complete_device_metadata_dictionary, create_complete_acquisition_meta_data_dictionary
import os


class CompletenessAndConsistencyTest(TestCase):

    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_wrong_input_type(self):
        device_dict = create_complete_device_metadata_dictionary()
        device_dict[pf.MetadataDeviceTags.GENERAL.tag][pf.MetadataDeviceTags.NUMBER_OF_ILLUMINATION_ELEMENTS.tag] = "4"
        device_dict[pf.MetadataDeviceTags.GENERAL.tag][pf.MetadataDeviceTags.FIELD_OF_VIEW.tag] = "Wrong"
        acquisition_dict = create_complete_acquisition_meta_data_dictionary()

        pa_data = pf.PAData(binary_time_series_data=np.zeros([256, 2048]),
                            meta_data_acquisition=acquisition_dict,
                            meta_data_device=device_dict)

        self.assertFalse(pf.quality_check_pa_data(pa_data))

    def test_empty_dictionaries(self):
        completeness_checker = pf.CompletenessChecker()
        self.assertFalse(completeness_checker.check_device_meta_data(dict()))
        self.assertFalse(completeness_checker.check_acquisition_meta_data(dict()))

        consistency_checker = pf.ConsistencyChecker()
        self.assertFalse(consistency_checker.check_device_meta_data(dict()))
        self.assertFalse(consistency_checker.check_acquisition_meta_data(dict()))

    def test_None_input_to_completeness_checker(self):
        completeness_checker = pf.CompletenessChecker(verbose=True)
        failed = False
        try:
            completeness_checker.check_device_meta_data(None)
        except ValueError:
            failed = True
        self.assertTrue(failed)

        failed = False
        try:
            completeness_checker.check_acquisition_meta_data(None)
        except ValueError:
            failed = True
        self.assertTrue(failed)

        failed = False
        try:
            completeness_checker.check_device_meta_data("None")
        except TypeError:
            failed = True
        self.assertTrue(failed)

        failed = False
        try:
            completeness_checker.check_acquisition_meta_data("None")
        except TypeError:
            failed = True
        self.assertTrue(failed)

    def test_None_input_to_consistency_checker(self):
        consistency_checker = pf.ConsistencyChecker(verbose=True)
        failed = False
        try:
            consistency_checker.check_device_meta_data(None)
        except ValueError:
            failed = True
        self.assertTrue(failed)

        failed = False
        try:
            consistency_checker.check_acquisition_meta_data(None)
        except ValueError:
            failed = True
        self.assertTrue(failed)

        failed = False
        try:
            consistency_checker.check_device_meta_data("None")
        except TypeError:
            failed = True
        self.assertTrue(failed)

        failed = False
        try:
            consistency_checker.check_acquisition_meta_data("None")
        except TypeError:
            failed = True
        self.assertTrue(failed)

    def test_log_file_writing(self):
        device_dict = create_complete_device_metadata_dictionary()
        acquisition_dict = create_complete_acquisition_meta_data_dictionary()

        pa_data = pf.PAData(binary_time_series_data=np.zeros([256, 2048]),
                            meta_data_acquisition=acquisition_dict,
                            meta_data_device=device_dict)

        completeness_checker = pf.CompletenessChecker(verbose=False, log_file_path="")
        self.assertFalse(os.path.exists(completeness_checker.save_file_name))

        completeness_checker.check_acquisition_meta_data(acquisition_dict)
        self.assertTrue(os.path.exists(completeness_checker.save_file_name))
        os.remove(completeness_checker.save_file_name)

        completeness_checker.check_device_meta_data(device_dict)
        self.assertTrue(os.path.exists(completeness_checker.save_file_name))
        os.remove(completeness_checker.save_file_name)

        consistency_checker = pf.ConsistencyChecker(verbose=False, log_file_path="")
        self.assertFalse(os.path.exists(consistency_checker.save_file_name))

        consistency_checker.check_acquisition_meta_data(acquisition_dict)
        self.assertTrue(os.path.exists(consistency_checker.save_file_name))
        os.remove(consistency_checker.save_file_name)

        consistency_checker.check_device_meta_data(device_dict)
        self.assertTrue(os.path.exists(consistency_checker.save_file_name))
        os.remove(consistency_checker.save_file_name)

    def test_pa_data_check(self):
        device_dict = create_complete_device_metadata_dictionary()
        acquisition_dict = create_complete_acquisition_meta_data_dictionary()

        pa_data = pf.PAData(binary_time_series_data=np.zeros([256, 2048]),
                            meta_data_acquisition=acquisition_dict,
                            meta_data_device=device_dict)

        self.assertTrue(pf.quality_check_pa_data(pa_data))

    def test_check_a_complete_and_consistent_pa_data_instance(self):
        device_dict = create_complete_device_metadata_dictionary()
        acquisition_dict = create_complete_acquisition_meta_data_dictionary()

        pa_data = pf.PAData(binary_time_series_data=np.zeros([256, 2048]),
                            meta_data_acquisition=acquisition_dict,
                            meta_data_device=device_dict)

        completeness_checker = pf.CompletenessChecker(verbose=True)
        consistency_checker = pf.ConsistencyChecker(verbose=True)

        assert completeness_checker.check_acquisition_meta_data(pa_data.meta_data_acquisition)
        assert completeness_checker.check_device_meta_data(pa_data.meta_data_device)

        assert consistency_checker.check_binary_data(pa_data.binary_time_series_data)
        assert consistency_checker.check_acquisition_meta_data(pa_data.meta_data_acquisition)
        assert consistency_checker.check_device_meta_data(pa_data.meta_data_device)

    def test_check_a_complete_but_inconsistent_pa_data_instance(self):
        device_dict = create_complete_device_metadata_dictionary()
        for illuminator_tag in device_dict[pf.MetadataDeviceTags.ILLUMINATORS.tag]:
            device_dict[pf.MetadataDeviceTags.ILLUMINATORS.tag][illuminator_tag]\
                [pf.MetadataDeviceTags.PULSE_WIDTH.tag] = -0.1
        acquisition_dict = create_complete_acquisition_meta_data_dictionary()
        acquisition_dict[pf.MetadataAcquisitionTags.DIMENSIONALITY.tag] = "Wrong string"

        pa_data = pf.PAData(binary_time_series_data=np.zeros([256, 2048]),
                            meta_data_acquisition=acquisition_dict,
                            meta_data_device=device_dict)

        completeness_checker = pf.CompletenessChecker(verbose=True)
        consistency_checker = pf.ConsistencyChecker(verbose=True)

        assert completeness_checker.check_acquisition_meta_data(pa_data.meta_data_acquisition)
        assert completeness_checker.check_device_meta_data(pa_data.meta_data_device)

        assert consistency_checker.check_binary_data(pa_data.binary_time_series_data)
        assert consistency_checker.check_acquisition_meta_data(pa_data.meta_data_acquisition) is False
        assert consistency_checker.check_device_meta_data(pa_data.meta_data_device) is False
