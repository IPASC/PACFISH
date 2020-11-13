# BSD 3-Clause License
#
# Copyright (c) 2020, IPASC
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import numpy as np
from ipasc_tool.core import MetaDatum, MetadataDeviceTags, MetadataAcquisitionTags


class PAData:
    """
    The PAData class is the core class for accessing the information contained in the HDF5 files.
    Using the iohandler.file_reader.load_data method yields an instance of this class.

    It is structured into three main parts:
    (1) a numpy array containing the binary data
    (2) a dictionary with the acquisition metadata
    (3) a dictionary with the device meta data

    Furthermore, this class contains convenience methods to access all fields within the HDF5 dictionary, without
    the necessity to know the internal structure by heart.
    """

    def __init__(self, binary_time_series_data: np.ndarray = None,
                 meta_data_acquisition: dict = None,
                 meta_data_device: dict = None):
        """
        Creates an instance of the PAData class.

        :param binary_time_series_data: a numpy array that must not be None
        :param meta_data_acquisition: a dictionary. If None will be initialized as an empty dictionary.
        :param meta_data_device: a dictionary. If None will be initialized as an empty dictionary.
        """

        if binary_time_series_data is None:
            binary_time_series_data = None

        if meta_data_acquisition is None:
            meta_data_acquisition = dict()

        if meta_data_device is None:
            meta_data_device = dict()

        self.binary_time_series_data = binary_time_series_data
        self.meta_data_acquisition = meta_data_acquisition
        self.meta_data_device = meta_data_device

    def get_illuminator_ids(self) -> list:
        """
        :return: a list of all ids of the illumination elements
        """
        return list(self.meta_data_device[MetadataDeviceTags.ILLUMINATORS.tag].keys())

    def get_detector_ids(self):
        """
        :return: a list of all ids of the detection elements
        """
        return self.meta_data_device[MetadataDeviceTags.DETECTORS.tag].keys()

    def get_acquisition_meta_datum(self, meta_data_tag: MetaDatum) -> object:
        """
        This method returns data from the acquisition meta data dictionary

        :param meta_data_tag: the MetaDatum instance for which to get the information.
        :return: return value might be None, if the specified meta data tag was not found in the dictionary.
        """
        if meta_data_tag.tag in self.meta_data_acquisition:
            return self.meta_data_acquisition[meta_data_tag.tag]
        else:
            return None

    def get_custom_meta_datum(self, meta_data_tag: str) -> object:
        """
        This method returns data from the acquisition meta data dictionary.

        :param meta_data_tag: a string instance for which to get the information.
        :return: return value might be None, if the specified meta data tag was not found in the dictionary.
        """
        if meta_data_tag in self.meta_data_acquisition:
            return self.meta_data_acquisition[meta_data_tag]
        else:
            return None

    def get_device_uuid(self):
        """
        The UUID is a universally unique identifier to the device description that can be referenced.
        :return: return value can be None, of no UUID was found in the meta data.
        """
        if MetadataDeviceTags.UUID.tag in self.meta_data_device[MetadataDeviceTags.GENERAL.tag]:
            return self.meta_data_device[MetadataDeviceTags.GENERAL.tag][MetadataDeviceTags.UUID.tag]
        else:
            return None

    def get_field_of_view(self):
        """
        The field of view defines an approximate cube of the area detectable by the PA imaging device in 3D cartesian
        coordinates [x1, x2, x3]. The field of view always starts in the origin of the coordinate system (which is
        defined as the centroid of the top-left transducer element when looking at the device normal to the imaging
        plane) and expands in the positive x1, x2, x3 directions.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        if MetadataDeviceTags.FIELD_OF_VIEW.tag in self.meta_data_device[MetadataDeviceTags.GENERAL.tag]:
            return self.meta_data_device[MetadataDeviceTags.GENERAL.tag][MetadataDeviceTags.FIELD_OF_VIEW.tag]
        else:
            return None

    def get_number_of_illuminators(self):
        """
        The number of illuminators quantifies the number of illuminators that are used in the respective PA imaging
        device. Each of these illuminators is described by a set of illumination geometry parameters.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        if MetadataDeviceTags.NUMBER_OF_ILLUMINATION_ELEMENTS.tag in self.meta_data_device[MetadataDeviceTags.GENERAL.tag]:
            return self.meta_data_device[MetadataDeviceTags.GENERAL.tag][MetadataDeviceTags.NUMBER_OF_ILLUMINATION_ELEMENTS.tag]
        else:
            return None

    def get_number_of_detectors(self):
        """
        The number of detectors quantifies the number of transducer elements that are used in the respective PA imaging
        device. Each of these transducer elements is described by a set of detection geometry parameters.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        if MetadataDeviceTags.NUMBER_OF_DETECTION_ELEMENTS.tag in self.meta_data_device[MetadataDeviceTags.GENERAL.tag]:
            return self.meta_data_device[MetadataDeviceTags.GENERAL.tag][MetadataDeviceTags.NUMBER_OF_DETECTION_ELEMENTS.tag]
        else:
            return None

    def get_illuminator_position(self, identifier=None):
        """
        The illuminator position defines the position of the illuminator centroid in 3D cartesian coordinates
        [x1, x2, x3] .

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.ILLUMINATOR_POSITION, identifier)

    def get_illuminator_orientation(self, identifier=None):
        """
        The illuminator orientation defines the rotation of the illuminator in 3D cartesian coordinates [r1, r2, r3].
        It is the normal of the planar illuminator surface.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.ILLUMINATOR_ORIENTATION, identifier)

    def get_illuminator_size(self, identifier=None):
        """
        The illuminator shape defines the shape of the optical fibres, so it describes  whether the illuminator is a
        point illuminator, or has a more continuous form. Illuminators can only have planar emitting surfaces.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.ILLUMINATOR_SHAPE, identifier)

    def get_wavelength_range(self, identifier=None):
        """
        The wavelength range quantifies the wavelength  range that the illuminator is capable of generating by
        reporting three values: the minimum wavelength max, the maximum wavelength  max and a metric for the
        accuracy accuracy: (min, max, accuracy). This parameter could for instance be (700, 900, 1.2), meaning
        that this illuminator can be tuned from 700 nm to 900 nm with an accuracy of 1.2 nm.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.WAVELENGTH_RANGE, identifier)

    def get_energy_profile(self, identifier=None):
        """
        The laser energy profile field is a discretized functional of wavelength (nm) that represents the laser energy
        of the illuminator with regard to the wavelength. Thereby, systematic differences in multispectral image
        acquisitions can be accounted for.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.LASER_ENERGY_PROFILE, identifier)

    def get_stability_profile(self, identifier=None):
        """
        The laser  noise profile field is a functional of wavelength (nm) that represents the standard deviation
        of the pulse-to-pulse laser energy of the illuminator with regard to the wavelength.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.LASER_STABILITY_PROFILE, identifier)

    def get_pulse_width(self, identifier=None):
        """
        The pulse duration or pulse width describes the total length of a laser pulse, measured as the time interval
        between the half-power points on the leading and trailing edges of the pulse.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.PULSE_WIDTH, identifier)

    def get_beam_profile(self, identifier=None):
        """
        The beam intensity profile is a function of a spatial position that specifies the relative laser beam
        intensity according to the planar emitting surface of the illuminator shape.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.BEAM_INTENSITY_PROFILE, identifier)

    def get_beam_divergence(self, identifier=None):
        """
        The beam divergence angles represent the opening angles of the laser beam from the illuminator shape with
        respect to the orientation vector. This angle represented by the standard deviation of the beam divergence.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.BEAM_DIVERGENCE_ANGLES, identifier)

    def get_illuminator_attribute_for_tag(self, metadatum_tag, identifier=None):
        if identifier is not None:
            if isinstance(identifier, int):
                if identifier < 0 or identifier >= self.get_number_of_illuminators():
                    raise ValueError("The illuminator position " + str(identifier) + "was out of range.")
                else:
                    return list(self.meta_data_device[MetadataDeviceTags.ILLUMINATORS.tag].values())[identifier][
                        metadatum_tag.tag]
            elif isinstance(identifier, str):
                if identifier not in self.get_illuminator_ids():
                    raise ValueError("The illuminator id " + str(identifier) + "was not valid.")
                else:
                    return self.meta_data_device[MetadataDeviceTags.ILLUMINATORS.tag][identifier][metadatum_tag.tag]
            else:
                raise ValueError("identifier must be int or string.")
        else:
            positions = []
            for id in self.get_illuminator_ids():
                positions.append(self.meta_data_device[MetadataDeviceTags.ILLUMINATORS.tag][id][metadatum_tag.tag])
            if metadatum_tag.dtype == np.ndarray:
                return np.asarray(positions)
            else:
                return positions

    def get_detector_position(self, identifier=None):
        """
        The element position defines the position of the detection element centroid in 3D cartesian coordinates
        [x1, x2, x3].

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_detector_attribute_for_tag(MetadataDeviceTags.DETECTOR_POSITION, identifier)

    def get_detector_orientation(self, identifier=None):
        """
        The element orientation defines the rotation of the detection element in 3D cartesian coordinates
        [r1, r2, r3] in radians.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_detector_attribute_for_tag(MetadataDeviceTags.DETECTOR_POSITION, identifier)

    def get_detector_size(self, identifier=None):
        """
        The element size defines the size of the detection element in 3D cartesian coordinates [x1, x2, x3]
        relative to its position and orientation.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_detector_attribute_for_tag(MetadataDeviceTags.DETECTOR_POSITION, identifier)

    def get_frequency_response(self, identifier=None):
        """
        The frequency response is a functional that characterizes the response of the detection element to the
        frequency of the incident pressure waves.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_detector_attribute_for_tag(MetadataDeviceTags.FREQUENCY_RESPONSE, identifier)

    def get_angular_response(self, identifier=None):
        """
        The angular response field characterizes the angular sensitivity of the detection element to the incident
        angle (relative to the elements orientation) of the incoming pressure wave.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_detector_attribute_for_tag(MetadataDeviceTags.ANGULAR_RESPONSE, identifier)

    def get_detector_attribute_for_tag(self, metadatum_tag, identifier=None):
        if identifier is not None:
            if isinstance(identifier, int):
                if identifier < 0 or identifier >= self.get_number_of_detectors():
                    raise ValueError("The detector position " + str(identifier) + "was out of range.")
                else:
                    return list(self.meta_data_device[MetadataDeviceTags.DETECTORS.tag].values())[identifier][
                        metadatum_tag.tag]
            elif isinstance(identifier, str):
                if identifier not in self.get_detector_ids():
                    raise ValueError("The detector id " + str(identifier) + "was not valid.")
                else:
                    return self.meta_data_device[MetadataDeviceTags.DETECTORS.tag][identifier][metadatum_tag.tag]
            else:
                raise ValueError("detector must be int or string.")
        else:
            positions = []
            for id in self.get_detector_ids():
                positions.append(self.meta_data_device[MetadataDeviceTags.DETECTORS.tag][id][metadatum_tag.tag])
            return np.asarray(positions)

    def get_encoding(self):
        """
        The encoding field is representative of the character set that was used to encode the binary data and the
        metadata. E.g. one of ‘UTF-8’, ‘ASCII’, ‘CP-1252’, …

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.ENCODING)

    def get_compression(self):
        """
        The compression field is representative of the compression method that was used to compress the binary data.
        E.g. one of ‘raw’, ‘gzip’, …

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.COMPRESSION)

    def get_data_UUID(self):
        """
        128-bit Integer displayed as a hexadecimal string in 5 groups separated by hyphens, in the form 8-4-4-4-12 for
        a total of 36 characters. The UUID is randomly generated using the UUID Version 4 standard.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.UUID)

    def get_data_type(self):
        """
        The data type field represents the datatype of the binary data. This field is given in the C++ data type naming
        convention. E.g. ‘short’, ‘unsigned short’, ‘int’, ‘unsigned int’, ‘long’, ‘unsigned long’, ‘long long’,
        ‘float’, ‘double’, ‘long double’.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.DATA_TYPE)

    def get_dimensionality(self):
        """
        The dimensionality field represents the acquisition format of the binary data and specifies the number of
        spatiotemporal dimensions of the data that is comprised of one or more frames. E.g. ‘1D’, ‘2D’, ‘3D’, ‘1D+t’,
        2D+t’, ‘3D+t’. In this notion, the time series sampling of one transducer would count as a “spatial” dimension.
        These are defined as 1D = [𝝉], 2D = [x1, 𝝉], 3D = [x1, 𝝉, x2]. The “+t” will then add a time dimension for
        multiple of these frames.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.DIMENSIONALITY)

    def get_sizes(self):
        """
        The sizes field quantifies the number of data points in each of the dimensions specified in the dimensionality
        field. e.g. [128, 2560, 26] with a “2D+t” dimensionality.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.SIZES)

    def get_device_reference(self):
        """
        A reference to the UUID of the PA imaging device description as defined in part 1.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.PHOTOACOUSTIC_IMAGING_DEVICE)

    def get_pulse_laser_energy(self):
        """
        The pulse laser energy field specifies the pulse-to-pulse laser energy that was measured for the acquisition
        of the raw time series data.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.PULSE_LASER_ENERGY)

    def get_time_stamps(self):
        """
        The frame acquisition timestamps field indicates the timestamp of the acquisition system.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.FRAME_ACQUISITION_TIMESTAMPS)

    def get_wavelengths(self):
        """
        The acquisition optical wavelengths field is a 1D array that contains a list of all wavelengths used for the
        image acquisition.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.ACQUISITION_OPTICAL_WAVELENGTHS)

    def get_time_gain_compensation(self):
        """
        The time gain compensation field is a 1D array that contains the relative factors which have been used to modify
        the time series data to correct for the effect of attenuation.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.TIME_GAIN_COMPENSATION)

    def get_overall_gain(self):
        """
        The overall gain is a single value describing a factor that has been applied to all values of the raw time
        series data.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.OVERALL_GAIN)

    def get_element_dependent_gain(self):
        """
        The element-dependent gain field is a 2D array that contains the relative factors which have been used to
        perform apodization.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.ELEMENT_DEPENDENT_GAIN)

    def get_temperature(self):
        """
        The temperature control field indicates the temperature during image acquisition.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.TEMPERATURE_CONTROL)

    def get_coupling_agent(self):
        """
        A string representation of the acoustic coupling agent that was used. For example, the following options are
        possible: D2O, H2O and US-gel.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.ACOUSTIC_COUPLING_AGENT)

    def get_scanning_method(self):
        """
        A string representation of the scanning method that was used.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.SCANNING_METHOD)

    def get_sampling_rate(self):
        """
        The A/D sampling rate refers to the rate at which samples of the analog signal are taken to be converted into
        digital form.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.AD_SAMPLING_RATE)

    def get_frequency_filter(self):
        """
         The frequency threshold levels that have been applied to filter the raw time series data.

        :return: return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.FREQUENCY_DOMAIN_FILTER)
