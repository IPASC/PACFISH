# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-License-Identifier: BSD 3-Clause License

import numpy as np
from pacfish import MetadataDeviceTags, MetadataAcquisitionTags


def create_complete_acquisition_meta_data_dictionary():

    dictionary = dict()
    dictionary[MetadataAcquisitionTags.UUID.tag] = create_random_testing_parameters()['test_string']
    dictionary[MetadataAcquisitionTags.ENCODING.tag] = create_random_testing_parameters()['test_string']
    dictionary[MetadataAcquisitionTags.COMPRESSION.tag] = create_random_testing_parameters()['test_string']
    dictionary[MetadataAcquisitionTags.PHOTOACOUSTIC_IMAGING_DEVICE_REFERENCE.tag] = create_random_testing_parameters()['test_string']
    dictionary[MetadataAcquisitionTags.DATA_TYPE.tag] = create_random_testing_parameters()['test_string']
    dictionary[MetadataAcquisitionTags.DIMENSIONALITY.tag] = "time"
    dictionary[MetadataAcquisitionTags.REGIONS_OF_INTEREST.tag] = np.asarray([0, 0.001, 0, 0.001, 0, 0.001])
    dictionary[MetadataAcquisitionTags.SIZES.tag] = np.asarray([4, 200])
    dictionary[MetadataAcquisitionTags.PULSE_ENERGY.tag] = np.asarray([2])
    dictionary[MetadataAcquisitionTags.MEASUREMENT_TIMESTAMPS.tag] = np.asarray([2])
    dictionary[MetadataAcquisitionTags.ACQUISITION_WAVELENGTHS.tag] = np.asarray([2])
    dictionary[MetadataAcquisitionTags.TIME_GAIN_COMPENSATION.tag] = create_random_testing_parameters()['test_array']
    dictionary[MetadataAcquisitionTags.OVERALL_GAIN.tag] = 2.2
    dictionary[MetadataAcquisitionTags.ELEMENT_DEPENDENT_GAIN.tag] = np.ones(100)
    dictionary[MetadataAcquisitionTags.TEMPERATURE_CONTROL.tag] = np.ones(100) * 290.3
    dictionary[MetadataAcquisitionTags.ACOUSTIC_COUPLING_AGENT.tag] = create_random_testing_parameters()['test_string']
    dictionary[MetadataAcquisitionTags.SCANNING_METHOD.tag] = create_random_testing_parameters()['test_string']
    dictionary[MetadataAcquisitionTags.AD_SAMPLING_RATE.tag] = 1.2234
    dictionary[MetadataAcquisitionTags.FREQUENCY_DOMAIN_FILTER.tag] = create_random_testing_parameters()['test_array']
    dictionary[MetadataAcquisitionTags.SPEED_OF_SOUND.tag] = np.asarray(1540.0)
    dictionary[MetadataAcquisitionTags.MEASUREMENT_SPATIAL_POSES.tag] = create_random_testing_parameters()['test_array']
    dictionary[MetadataAcquisitionTags.MEASUREMENTS_PER_IMAGE.tag] = 1
    return dictionary


def create_random_testing_parameters():

    test_float = np.random.random()
    test_string = str(np.random.random())
    test_dict = dict()
    test_array = np.random.random((1000, 2))
    return {'test_float': test_float,
            'test_string': test_string,
            'test_dict': test_dict,
            'test_array': test_array}


def create_random_illumination_element(dim_x=None, dim_y=None, dim_z=None):

    illuminator_dict = dict()
    illuminator_dict[MetadataDeviceTags.ILLUMINATOR_POSITION.tag] = np.asarray([
        np.random.random() * 2 * dim_x - dim_x,
        np.random.random() * 2 * dim_y - dim_y,
        -np.random.random() * dim_z / 2])
    illuminator_dict[MetadataDeviceTags.ILLUMINATOR_ORIENTATION.tag] = np.asarray([
        np.random.random()-0.5,
        np.random.random()-0.5,
        np.random.random()-0.5])
    illuminator_dict[MetadataDeviceTags.ILLUMINATOR_GEOMETRY.tag] = np.asarray([0.0001,
                                                                                 0.0001,
                                                                                 0.0001])
    illuminator_dict[MetadataDeviceTags.ILLUMINATOR_GEOMETRY_TYPE.tag] = "CUBOID"
    min_wavelength = np.random.random() * 200 + 600
    illuminator_dict[MetadataDeviceTags.WAVELENGTH_RANGE.tag] = np.asarray([min_wavelength,
                                                                                 min_wavelength +
                                                                                 np.random.random() * 200,
                                                                                 1.0])
    illuminator_dict[MetadataDeviceTags.BEAM_ENERGY_PROFILE.tag] = np.asarray([np.random.random(size=200),
                                                                               np.random.random(size=200)])
    illuminator_dict[MetadataDeviceTags.BEAM_STABILITY_PROFILE.tag] = np.asarray([np.random.random(size=200),
                                                                                  np.random.random(size=200)])
    illuminator_dict[MetadataDeviceTags.PULSE_WIDTH.tag] = 0.00000012
    illuminator_dict[MetadataDeviceTags.BEAM_INTENSITY_PROFILE.tag] = np.random.random(size=(200, 4))
    illuminator_dict[MetadataDeviceTags.INTENSITY_PROFILE_DISTANCE.tag] = 1337.4217
    illuminator_dict[MetadataDeviceTags.BEAM_DIVERGENCE_ANGLES.tag] = np.deg2rad(np.random.random() * 40)
    return illuminator_dict


def create_random_detection_element(dim_x=None, dim_y=None, dim_z=None):

    detector_dict = dict()
    detector_dict[MetadataDeviceTags.DETECTOR_POSITION.tag] = np.asarray([np.random.random() * dim_x,
                                                                          np.random.random() * dim_y,
                                                                          -np.random.random() * dim_z])
    detector_dict[MetadataDeviceTags.DETECTOR_ORIENTATION.tag] = np.asarray(
        [np.random.random() * dim_x - dim_x / 2,
         np.random.random() * dim_y - dim_y / 2,
         np.random.random() * dim_z - dim_z / 2])

    detector_dict[MetadataDeviceTags.DETECTOR_GEOMETRY.tag] = np.asarray([0.0001, 0.0001, 0.0001])
    detector_dict[MetadataDeviceTags.DETECTOR_GEOMETRY_TYPE.tag] = "CUBOID"

    detector_dict[MetadataDeviceTags.FREQUENCY_RESPONSE.tag] = np.asarray([np.random.random(size=200),
                                                                           np.random.random(size=200)])
    detector_dict[MetadataDeviceTags.ANGULAR_RESPONSE.tag] = np.asarray([np.random.random(size=200),
                                                                         np.random.random(size=200)])
    return detector_dict


def create_complete_device_metadata_dictionary(dim_x=None, dim_y=None, dim_z=None):

    if dim_x is None:
        dim_x = 0.001
    if dim_y is None:
        dim_y = 0.03
    if dim_z is None:
        dim_z = 0.03

    dictionary = {
        MetadataDeviceTags.GENERAL.tag: {
            MetadataDeviceTags.UNIQUE_IDENTIFIER.tag: "a2fd-48nbsh-sfiush7-chjs",
            MetadataDeviceTags.FIELD_OF_VIEW.tag: np.asarray([0, dim_x, 0, dim_y, 0, dim_z]),
            MetadataDeviceTags.NUMBER_OF_ILLUMINATION_ELEMENTS.tag: 2,
            MetadataDeviceTags.NUMBER_OF_DETECTION_ELEMENTS.tag: 4
        },
        MetadataDeviceTags.ILLUMINATORS.tag: {
            MetadataDeviceTags.ILLUMINATION_ELEMENT.tag + "_0":
                create_random_illumination_element(dim_x, dim_y, dim_z),
            MetadataDeviceTags.ILLUMINATION_ELEMENT.tag + "_1":
                create_random_illumination_element(dim_x, dim_y, dim_z)
        },
        MetadataDeviceTags.DETECTORS.tag: {
            MetadataDeviceTags.DETECTION_ELEMENT.tag + "_0":
                create_random_detection_element(dim_x, dim_y, dim_z),
            MetadataDeviceTags.DETECTION_ELEMENT.tag + "_1":
                create_random_detection_element(dim_x, dim_y, dim_z),
            MetadataDeviceTags.DETECTION_ELEMENT.tag + "_2":
                create_random_detection_element(dim_x, dim_y, dim_z),
            MetadataDeviceTags.DETECTION_ELEMENT.tag + "_3":
                create_random_detection_element(dim_x, dim_y, dim_z)
        }
    }

    return dictionary
