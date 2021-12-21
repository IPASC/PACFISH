# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-License-Identifier: BSD 3-Clause License

from unittest.case import TestCase
import pacfish as pf
from testing.unit_tests.utils import create_complete_device_metadata_dictionary
import os
import numpy as np
import imageio


class VisualisationTest(TestCase):

    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_visualisation_runs_though_and_produces_non_empty_png(self):
        device_metadata = create_complete_device_metadata_dictionary()
        pf.visualize_device(device_dictionary=device_metadata,
                            save_path="")

        self.assertTrue(os.path.exists("figure.png"))
        im = np.asarray(imageio.imread("figure.png"))
        self.assertTrue((np.mean(im) > 0) and (np.mean(im) < 255))
        os.remove("figure.png")
        self.assertFalse(os.path.exists("figure.png"))
