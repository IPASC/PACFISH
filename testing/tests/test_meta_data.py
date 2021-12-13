"""
SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
SPDX-License-Identifier: BSD 3-Clause License
"""

import os
from unittest.case import TestCase
from pacfish import MetadataDeviceTags
from pacfish.core.Metadata import NonNegativeNumber, NonNegativeWholeNumber, NonNegativeNumbersInArray, \
    NumberWithUpperAndLowerLimit, NDimensionalNumpyArray, EnumeratedString, UnconstrainedMetaDatum, Units
from pacfish import CompletenessChecker
from testing.tests.utils import create_complete_device_metadata_dictionary
import numpy as np


class MetaDataTest(TestCase):

    def setUp(self):
        self.completeness_checker = CompletenessChecker(True, "")
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_completeness_checker_device(self):
        device_dictionary = create_complete_device_metadata_dictionary()
        assert self.completeness_checker.check_meta_data_device(device_dictionary)

        device_dictionary[MetadataDeviceTags.GENERAL.tag][MetadataDeviceTags.UUID.tag] = None
        assert not self.completeness_checker.check_meta_data_device(device_dictionary)

        device_dictionary = create_complete_device_metadata_dictionary()
        assert self.completeness_checker.check_meta_data_device(device_dictionary)

        device_dictionary[MetadataDeviceTags.GENERAL.tag].pop(MetadataDeviceTags.UUID.tag)
        assert not self.completeness_checker.check_meta_data_device(device_dictionary)

        os.remove(self.completeness_checker.save_file_name)

    def test_meta_data_constraint_classes(self):
        test_field = NonNegativeNumber("tag", True, float, Units.METERS)
        assert test_field.evaluate_value_range(1.23) is True
        assert test_field.evaluate_value_range(0.0) is True
        assert test_field.evaluate_value_range(-1.23) is False

        test_field = NonNegativeWholeNumber("tag", True, int, Units.METERS)
        assert test_field.evaluate_value_range(1) is True
        assert test_field.evaluate_value_range(0) is True
        assert test_field.evaluate_value_range(-2) is False
        exception_raised = False
        try:
            test_field.evaluate_value_range(1.12)
        except TypeError:
            exception_raised = True
        assert exception_raised

        test_field = NonNegativeNumbersInArray("tag", True, np.ndarray, Units.METERS)
        assert test_field.evaluate_value_range(np.asarray([1.23, 17.46])) is True
        assert test_field.evaluate_value_range(np.asarray([0.0, 17.46])) is True
        assert test_field.evaluate_value_range(np.asarray([1.23, -17.46])) is False

        test_field = NumberWithUpperAndLowerLimit("tag", True, float, Units.METERS,
                                                  lower_limit=0, upper_limit=1)
        assert test_field.evaluate_value_range(1.23) is False
        assert test_field.evaluate_value_range(0.0) is True
        assert test_field.evaluate_value_range(0.5) is True
        assert test_field.evaluate_value_range(1.0) is True
        assert test_field.evaluate_value_range(-1.23) is False

        test_field = NDimensionalNumpyArray("tag", True, np.ndarray, Units.METERS,
                                            expected_array_dimension=2)
        assert test_field.evaluate_value_range(np.asarray([1.23])) is False
        assert test_field.evaluate_value_range(np.asarray([[0.0, 17.46], [12, 12]])) is True
        assert test_field.evaluate_value_range(np.asarray([[[1.23, -17.46, 0.0], [1.23, -17.46, 0.0],
                                                          [1.23, -17.46, 0.0]],
                                                           [[1.23, -17.46, 0.0], [1.23, -17.46, 0.0],
                                                            [1.23, -17.46, 0.0]]
                                                           ])) is False

        test_field = EnumeratedString("tag", True, str, Units.METERS,
                                            permissible_strings=["A", "B"])

        assert test_field.evaluate_value_range("A") is True
        assert test_field.evaluate_value_range("AB") is False
        assert test_field.evaluate_value_range("B") is True
        assert test_field.evaluate_value_range("Hallo") is False

        test_field = UnconstrainedMetaDatum("tag", True, str, Units.METERS)
        assert test_field.evaluate_value_range("A") is True
        assert test_field.evaluate_value_range("Hallo") is True
        try:
            test_field.evaluate_value_range(1.12)
        except TypeError:
            exception_raised = True
        assert exception_raised
