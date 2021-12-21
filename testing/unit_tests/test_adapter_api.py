# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-License-Identifier: BSD 3-Clause License
import unittest
from unittest.case import TestCase
import pacfish as pf
import numpy as np

from examples.python.create_a_pat_device import illuminator
from .utils import create_complete_device_metadata_dictionary, create_complete_acquisition_meta_data_dictionary

from pacfish import MetaDatum


class EmptyTestAdapter(pf.BaseAdapter):
    def generate_binary_data(self) -> np.ndarray:
        return None

    def generate_device_meta_data(self) -> dict:
        return {pf.MetadataDeviceTags.DETECTORS.tag: dict(),
                pf.MetadataDeviceTags.ILLUMINATORS.tag: dict(),
                pf.MetadataDeviceTags.GENERAL.tag: dict()}

    def set_metadata_value(self, metadatum: MetaDatum) -> object:
        return None


class AdapterAPITest(TestCase):

    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    @unittest.expectedFailure
    def test_instantiate_base_adapter(self):
        base_adapter = pf.BaseAdapter()

    def test_empty_adapter_returns_None(self):

        eta = EmptyTestAdapter()
        pa_data = eta.generate_pa_data()

        # empty lists:
        self.assertTrue(len(pa_data.get_detector_ids()) == 0)
        self.assertTrue(len(pa_data.get_illuminator_ids()) == 0)

        # None return
        self.assertIsNone(pa_data.get_sampling_rate())
        self.assertIsNone(pa_data.get_acquisition_wavelengths())
        self.assertIsNone(pa_data.get_photoacoustic_imaging_device_reference())
        self.assertIsNone(pa_data.get_measurements_per_image())
        self.assertIsNone(pa_data.get_measurement_spatial_poses())
        self.assertIsNone(pa_data.get_acoustic_coupling_agent())
        self.assertIsNone(pa_data.get_angular_response())
        self.assertIsNone(pa_data.get_beam_divergence())
        self.assertIsNone(pa_data.get_beam_energy_profile())
        self.assertIsNone(pa_data.get_beam_profile())
        self.assertIsNone(pa_data.get_beam_profile_distance())
        self.assertIsNone(pa_data.get_compression())
        self.assertIsNone(pa_data.get_beam_stability_profile())
        self.assertIsNone(pa_data.get_data_type())
        self.assertIsNone(pa_data.get_data_UUID())
        self.assertIsNone(pa_data.get_device_uuid())
        self.assertIsNone(pa_data.get_measurement_time_stamps())
        self.assertIsNone(pa_data.get_scanning_method())
        self.assertIsNone(pa_data.get_detector_position())
        self.assertIsNone(pa_data.get_detector_geometry())
        self.assertIsNone(pa_data.get_detector_orientation())
        self.assertIsNone(pa_data.get_detector_geometry_type())
        self.assertIsNone(pa_data.get_illuminator_position())
        self.assertIsNone(pa_data.get_illuminator_geometry())
        self.assertIsNone(pa_data.get_illuminator_orientation())
        self.assertIsNone(pa_data.get_illuminator_geometry_type())

    def test_adding_custom_data_fields(self):

        eta = EmptyTestAdapter()
        eta.add_custom_meta_datum_field("test1", "value1")
        eta.add_custom_meta_datum_field("test2", 17.11)
        eta.add_custom_meta_datum_field("test3", np.asarray([1, 2, 3, 4]))

        pa_data = eta.generate_pa_data()

        self.assertEqual(pa_data.get_custom_meta_datum("test1"), "value1")
        self.assertEqual(pa_data.get_custom_meta_datum("test2"), 17.11)
        self.assertTrue((pa_data.get_custom_meta_datum("test3") == np.asarray([1, 2, 3, 4])).all())

        failed = False
        try:
            eta.add_custom_meta_datum_field("test1", None)
        except ValueError:
            failed = True
        self.assertTrue(failed)

        failed = False
        try:
            eta.add_custom_meta_datum_field(None, "Test1")
        except KeyError:
            failed = True
        self.assertTrue(failed)

    def test_custom_adapter_generates_expected_output(self):

        class FunctioningAdapter(pf.BaseAdapter):

            def __init__(self):
                self.acquisition_metadata_test = create_complete_acquisition_meta_data_dictionary()
                self.device_metadata_test = create_complete_device_metadata_dictionary()
                self.num_detectors = len(self.device_metadata_test[pf.MetadataDeviceTags.DETECTORS.tag])
                self.binary_data = np.random.random((self.num_detectors, 2000))
                super(FunctioningAdapter, self).__init__()

            def generate_binary_data(self) -> np.ndarray:
                return self.binary_data

            def generate_device_meta_data(self) -> dict:
                return self.device_metadata_test

            def set_metadata_value(self, metadatum: MetaDatum) -> object:
                return self.acquisition_metadata_test[metadatum.tag]

        fa = FunctioningAdapter()
        pa_data = fa.generate_pa_data()

        amd = fa.generate_acquisition_meta_data()
        dmd = fa.generate_device_meta_data()

        # non empty lists:
        self.assertTrue(len(pa_data.get_detector_ids()) > 0)
        self.assertTrue(len(pa_data.get_illuminator_ids()) > 0)

        # Acquisition Metadata
        self.assertEqual(pa_data.get_data_UUID(),
                          amd[pf.MetadataAcquisitionTags.UUID.tag])
        self.assertEqual(pa_data.get_encoding(),
                          amd[pf.MetadataAcquisitionTags.ENCODING.tag])
        self.assertEqual(pa_data.get_compression(),
                          amd[pf.MetadataAcquisitionTags.COMPRESSION.tag])
        self.assertEqual(pa_data.get_data_type(),
                          amd[pf.MetadataAcquisitionTags.DATA_TYPE.tag])
        self.assertEqual(pa_data.get_dimensionality(),
                          amd[pf.MetadataAcquisitionTags.DIMENSIONALITY.tag])
        self.assertTrue((pa_data.get_sizes() ==
                          amd[pf.MetadataAcquisitionTags.SIZES.tag]).all())
        self.assertEqual(pa_data.get_compression(),
                          amd[pf.MetadataAcquisitionTags.COMPRESSION.tag])
        self.assertEqual(pa_data.get_regions_of_interest(),
                          amd[pf.MetadataAcquisitionTags.REGIONS_OF_INTEREST.tag])
        self.assertEqual(pa_data.get_photoacoustic_imaging_device_reference(),
                          amd[pf.MetadataAcquisitionTags.PHOTOACOUSTIC_IMAGING_DEVICE_REFERENCE.tag])
        self.assertEqual(pa_data.get_measurement_time_stamps(),
                          amd[pf.MetadataAcquisitionTags.MEASUREMENT_TIMESTAMPS.tag])
        self.assertTrue((pa_data.get_measurement_spatial_poses() ==
                          amd[pf.MetadataAcquisitionTags.MEASUREMENT_SPATIAL_POSES.tag]).all())
        self.assertEqual(pa_data.get_acquisition_wavelengths(),
                          amd[pf.MetadataAcquisitionTags.ACQUISITION_WAVELENGTHS.tag])
        self.assertTrue((pa_data.get_time_gain_compensation() ==
                         amd[pf.MetadataAcquisitionTags.TIME_GAIN_COMPENSATION.tag]).all())
        self.assertEqual(pa_data.get_overall_gain(),
                         amd[pf.MetadataAcquisitionTags.OVERALL_GAIN.tag])
        self.assertTrue((pa_data.get_element_dependent_gain() ==
                         amd[pf.MetadataAcquisitionTags.ELEMENT_DEPENDENT_GAIN.tag]).all())
        self.assertTrue((pa_data.get_temperature() ==
                         amd[pf.MetadataAcquisitionTags.TEMPERATURE_CONTROL.tag]).all())
        self.assertEqual(pa_data.get_acoustic_coupling_agent(),
                         amd[pf.MetadataAcquisitionTags.ACOUSTIC_COUPLING_AGENT.tag])
        self.assertEqual(pa_data.get_scanning_method(),
                         amd[pf.MetadataAcquisitionTags.SCANNING_METHOD.tag])
        self.assertEqual(pa_data.get_speed_of_sound(),
                         amd[pf.MetadataAcquisitionTags.SPEED_OF_SOUND.tag])
        self.assertEqual(pa_data.get_sampling_rate(),
                         amd[pf.MetadataAcquisitionTags.AD_SAMPLING_RATE.tag])
        self.assertTrue((pa_data.get_frequency_domain_filter() ==
                         amd[pf.MetadataAcquisitionTags.FREQUENCY_DOMAIN_FILTER.tag]).all())
        self.assertEqual(pa_data.get_measurements_per_image(),
                         amd[pf.MetadataAcquisitionTags.MEASUREMENTS_PER_IMAGE.tag])

        # Detector metadata
        for detector_id in pa_data.get_detector_ids():
            self.assertTrue((pa_data.get_detector_position(detector_id) ==
                              dmd[pf.MetadataDeviceTags.DETECTORS.tag][detector_id]
                              [pf.MetadataDeviceTags.DETECTOR_POSITION.tag]).all())
            self.assertTrue((pa_data.get_detector_geometry(detector_id) ==
                              dmd[pf.MetadataDeviceTags.DETECTORS.tag][detector_id]
                              [pf.MetadataDeviceTags.DETECTOR_GEOMETRY.tag]).all())
            self.assertTrue((pa_data.get_detector_orientation(detector_id) ==
                              dmd[pf.MetadataDeviceTags.DETECTORS.tag][detector_id]
                              [pf.MetadataDeviceTags.DETECTOR_ORIENTATION.tag]).all())
            self.assertEqual(pa_data.get_detector_geometry_type(detector_id),
                              dmd[pf.MetadataDeviceTags.DETECTORS.tag][detector_id]
                              [pf.MetadataDeviceTags.DETECTOR_GEOMETRY_TYPE.tag])
            self.assertTrue((pa_data.get_angular_response(detector_id) ==
                              dmd[pf.MetadataDeviceTags.DETECTORS.tag][detector_id]
                              [pf.MetadataDeviceTags.ANGULAR_RESPONSE.tag]).all())
            self.assertTrue((pa_data.get_frequency_response(detector_id) ==
                              dmd[pf.MetadataDeviceTags.DETECTORS.tag][detector_id]
                              [pf.MetadataDeviceTags.FREQUENCY_RESPONSE.tag]).all())

        # Illuminator metadata
        for illuminator_id in pa_data.get_illuminator_ids():
            self.assertTrue((pa_data.get_illuminator_position(illuminator_id) ==
                              dmd[pf.MetadataDeviceTags.ILLUMINATORS.tag][illuminator_id]
                              [pf.MetadataDeviceTags.ILLUMINATOR_POSITION.tag]).all())
            self.assertTrue((pa_data.get_illuminator_geometry(illuminator_id) ==
                              dmd[pf.MetadataDeviceTags.ILLUMINATORS.tag][illuminator_id]
                              [pf.MetadataDeviceTags.ILLUMINATOR_GEOMETRY.tag]).all())
            self.assertTrue((pa_data.get_illuminator_orientation(illuminator_id) ==
                              dmd[pf.MetadataDeviceTags.ILLUMINATORS.tag][illuminator_id]
                              [pf.MetadataDeviceTags.ILLUMINATOR_ORIENTATION.tag]).all())
            self.assertEqual(pa_data.get_illuminator_geometry_type(illuminator_id),
                              dmd[pf.MetadataDeviceTags.ILLUMINATORS.tag][illuminator_id]
                              [pf.MetadataDeviceTags.ILLUMINATOR_GEOMETRY_TYPE.tag])
            self.assertEqual(pa_data.get_beam_divergence(illuminator_id),
                              dmd[pf.MetadataDeviceTags.ILLUMINATORS.tag][illuminator_id]
                              [pf.MetadataDeviceTags.BEAM_DIVERGENCE_ANGLES.tag])
            self.assertTrue((pa_data.get_beam_energy_profile(illuminator_id) ==
                              dmd[pf.MetadataDeviceTags.ILLUMINATORS.tag][illuminator_id]
                              [pf.MetadataDeviceTags.BEAM_ENERGY_PROFILE.tag]).all())
            self.assertTrue((pa_data.get_beam_profile(illuminator_id) ==
                              dmd[pf.MetadataDeviceTags.ILLUMINATORS.tag][illuminator_id]
                              [pf.MetadataDeviceTags.BEAM_INTENSITY_PROFILE.tag]).all())
            self.assertEqual(pa_data.get_beam_profile_distance(illuminator_id),
                              dmd[pf.MetadataDeviceTags.ILLUMINATORS.tag][illuminator_id]
                              [pf.MetadataDeviceTags.INTENSITY_PROFILE_DISTANCE.tag])
            self.assertTrue((pa_data.get_beam_stability_profile(illuminator_id) ==
                              dmd[pf.MetadataDeviceTags.ILLUMINATORS.tag][illuminator_id]
                              [pf.MetadataDeviceTags.BEAM_STABILITY_PROFILE.tag]).all())
            self.assertTrue((pa_data.get_wavelength_range(illuminator_id) ==
                             dmd[pf.MetadataDeviceTags.ILLUMINATORS.tag][illuminator_id]
                             [pf.MetadataDeviceTags.WAVELENGTH_RANGE.tag]).all())
            self.assertEqual(pa_data.get_pulse_width(illuminator_id),
                             dmd[pf.MetadataDeviceTags.ILLUMINATORS.tag][illuminator_id]
                             [pf.MetadataDeviceTags.PULSE_WIDTH.tag])
