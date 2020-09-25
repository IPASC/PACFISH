import os
from unittest.case import TestCase
from ipasc_tool import PAData
from test.tests.utils import create_complete_device_metadata_dictionary, create_complete_meta_data_dictionary
import numpy as np


class MetaDataTest(TestCase):

    def setUp(self):
        self.acquisition_metadata = create_complete_meta_data_dictionary()
        self.device_metadata = create_complete_device_metadata_dictionary()
        self.pa_data = PAData(binary_time_series_data=np.random.random((4, 200)),
                              meta_data_acquisition=self.acquisition_metadata,
                              meta_data_device=self.device_metadata)
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_get_illuminator_positions(self):
        print(self.pa_data.get_illuminator_position())
        print(self.pa_data.get_illuminator_position(list(self.pa_data.get_illuminator_ids())[0]))
        print(self.pa_data.get_illuminator_position(0))