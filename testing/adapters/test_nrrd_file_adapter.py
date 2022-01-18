import os
from testing.adapters.utils import create_nrrd_file
from pacfish.api.adapters import NrrdFileConverter
import pacfish as pf
from unittest import TestCase


class DeviceMetaDataCreatorTest(TestCase):

    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_using_converter(self):

        if not os.path.exists('demodata.nrrd'):
            create_nrrd_file('demodata.nrrd')

        converter = NrrdFileConverter('demodata.nrrd')

        pa_data = converter.generate_pa_data()
        self.assertIsNotNone(pa_data)
        pf.quality_check_pa_data(pa_data)

        if os.path.exists("demodata.nrrd"):
            os.remove("demodata.nrrd")
