# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-FileCopyrightText: 2021 Janek Gröhl
# SPDX-FileCopyrightText: 2021 Lina Hacker
# SPDX-License-Identifier: BSD 3-Clause License

import numpy as np
from pacfish.core import MetaDatum, MetadataDeviceTags, MetadataAcquisitionTags


class PAData:
    """
    The PAData class is the core class for accessing the information contained in the HDF5 files.
    Using the `pacfish.load_data` method yields an instance of this class.

    It is structured into three main parts:

        1. a numpy array containing the binary data
        2. a dictionary with the acquisition metadata
        3. a dictionary with the device meta data

    Furthermore, this class contains convenience methods to access all fields within the HDF5 dictionary, without
    the necessity to know the internal structure by heart.
    """

    def __init__(self, binary_time_series_data: np.ndarray = None,
                 meta_data_acquisition: dict = None,
                 meta_data_device: dict = None):
        """
        Creates an empty instance of the PAData class.
        To instantiate with a path to an HDF5 file, please use
        the `pacfish.load_data` method.

        Parameters
        ----------
        binary_time_series_data: np.ndarray
            a numpy array that must not be None
        meta_data_acquisition: dict
            If None will be initialized as an empty dictionary.
        meta_data_device: dict
            If None will be initialized as an empty dictionary.

        Return
        ------
        pacfish.PAData
            An empty PADta instance to be populated
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
        Returns a list of all IDs of the illumination elements
        that are added in this PAData instance.

        Return
        ------
        list
            a list of all ids of the illumination elements
        """
        return list(self.meta_data_device[MetadataDeviceTags.ILLUMINATORS.tag].keys())

    def get_detector_ids(self) -> list:
        """
        Returns a list of all IDs of the detection elements
        that are added in this PAData instance.

        Return
        ------
        list
            a list of all ids of the detection elements
        """
        return self.meta_data_device[MetadataDeviceTags.DETECTORS.tag].keys()

    def get_acquisition_meta_datum(self, meta_data_tag: MetaDatum) -> object:
        """
        This method returns data from the acquisition meta data dictionary

        Parameters
        ----------
        meta_data_tag:
            the MetaDatum instance for which to get the information.

        Return
        ------
        object
            return value might be None, if the specified meta data tag was not found in the dictionary.
        """
        if meta_data_tag.tag in self.meta_data_acquisition:
            return self.meta_data_acquisition[meta_data_tag.tag]
        else:
            return None

    def get_custom_meta_datum(self, meta_data_tag: str) -> object:
        """
        This method returns data from the acquisition meta data dictionary.

        Parameters
        ----------
        meta_data_tag:
            a string instance for which to get the information.

        Return
        ------
        object
            return value might be None, if the specified meta data tag was not found in the dictionary.
        """
        if meta_data_tag in self.meta_data_acquisition:
            return self.meta_data_acquisition[meta_data_tag]
        else:
            return None

    def get_device_uuid(self):
        """
        The UUID is a universally unique identifier to the device description that can be referenced.

        Return
        ------
        str
            return value can be None, of no UUID was found in the meta data.
        """
        if MetadataDeviceTags.UNIQUE_IDENTIFIER.tag in self.meta_data_device[MetadataDeviceTags.GENERAL.tag]:
            return self.meta_data_device[MetadataDeviceTags.GENERAL.tag][MetadataDeviceTags.UNIQUE_IDENTIFIER.tag]
        else:
            return None

    def get_field_of_view(self):
        """
        An array defining an approximate cuboid (3D) area that should be reconstructed in 3D Cartesian
        coordinates [x1_start, x1_end, x2_start, x2_end, x3_start, x3_end].
        A 2D Field of View can be defined by setting the start and end coordinate of
        the respective dimension to the same value.

        Return
        ------
        np.ndarray
            return value can be None, of the key was not found in the meta data dictionary.
        """
        if MetadataDeviceTags.FIELD_OF_VIEW.tag in self.meta_data_device[MetadataDeviceTags.GENERAL.tag]:
            return self.meta_data_device[MetadataDeviceTags.GENERAL.tag][MetadataDeviceTags.FIELD_OF_VIEW.tag]
        else:
            return None

    def get_number_of_illuminators(self):
        """
        The number of illuminators quantifies the number of illuminators that are used in the respective PA imaging
        device. Each of these illuminators is described by a set of illumination geometry parameters.

        Return
        ------
        int
            return value can be None, of the key was not found in the meta data dictionary.
        """
        if MetadataDeviceTags.NUMBER_OF_ILLUMINATION_ELEMENTS.tag in self.meta_data_device[MetadataDeviceTags.GENERAL.tag]:
            return self.meta_data_device[MetadataDeviceTags.GENERAL.tag][MetadataDeviceTags.NUMBER_OF_ILLUMINATION_ELEMENTS.tag]
        else:
            return None

    def get_number_of_detectors(self):
        """
        The number of detectors quantifies the number of transducer elements that are used in the respective PA imaging
        device. Each of these transducer elements is described by a set of detection geometry parameters.

        Return
        ------
        int
            return value can be None, of the key was not found in the meta data dictionary.
        """
        if MetadataDeviceTags.NUMBER_OF_DETECTION_ELEMENTS.tag in self.meta_data_device[MetadataDeviceTags.GENERAL.tag]:
            return self.meta_data_device[MetadataDeviceTags.GENERAL.tag][MetadataDeviceTags.NUMBER_OF_DETECTION_ELEMENTS.tag]
        else:
            return None

    def get_illuminator_position(self, identifier=None):
        """
        The illuminator position defines the position of the illuminator centroid in 3D cartesian coordinates
        [x1, x2, x3] .

        Parameters
        ----------
        identifier: str
            The ID of a specific illumination element. If `None` then all illumination elements are queried.

        Return
        ------
        np.ndarray
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.ILLUMINATOR_POSITION, identifier)

    def get_illuminator_orientation(self, identifier=None):
        """
        The illuminator orientation defines the rotation of the illuminator in 3D cartesian coordinates [r1, r2, r3].
        It is the normal of the planar illuminator surface.

        Parameters
        ----------
        identifier: str
            The ID of a specific illumination element. If `None` then all illumination elements are queried.

        Return
        ------
        np.ndarray
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.ILLUMINATOR_ORIENTATION, identifier)

    def get_illuminator_geometry(self, identifier=None):
        """
        The illuminator shape defines the shape of the optical fibres, so it describes  whether the illuminator is a
        point illuminator, or has a more continuous form. Illuminators can only have planar emitting surfaces.

        Parameters
        ----------
        identifier: str
            The ID of a specific illumination element. If `None` then all illumination elements are queried.

        Return
        ------
        np.ndarray
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.ILLUMINATOR_GEOMETRY, identifier)

    def get_illuminator_geometry_type(self, identifier=None):
        """
        The illuminator geometry type defines the shape of the optical fibre (bundle) output.
        It determines the interpretation of the data in the illuminator geometry field.
        The following geometry types are currently supported::

            - "CIRCULAR" - defined by a single value that determines the radius of the circle
            - "SPHERE" - defined by a single value that determines the radius of the sphere
            - "CUBOID" - defined by three values that determine the extent of the cuboid in x, y,nand z dimensions before the position and orientation transforms.
            - "MESH" - defined by a STL-formatted string that determines the positions of points and faces before the position and orientation transforms.


        Parameters
        ----------
        identifier: str
            The ID of a specific illumination element. If `None` then all illumination elements are queried.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.ILLUMINATOR_GEOMETRY_TYPE, identifier)

    def get_wavelength_range(self, identifier=None):
        """
        The wavelength range quantifies the wavelength  range that the illuminator is capable of generating by
        reporting three values: the minimum wavelength max, the maximum wavelength  max and a metric for the
        accuracy accuracy: (min, max, accuracy). This parameter could for instance be (700, 900, 1.2), meaning
        that this illuminator can be tuned from 700 nm to 900 nm with an accuracy of 1.2 nm.

        Parameters
        ----------
        identifier: str
            The ID of a specific illumination element. If `None` then all illumination elements are queried.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.WAVELENGTH_RANGE, identifier)

    def get_beam_energy_profile(self, identifier=None):
        """
        The beam energy profile field is a discretized functional of wavelength (nm) that represents the light energy
        of the illuminator with regard to the wavelength. Thereby, systematic differences in multispectral image
        acquisitions can be accounted for.

        Parameters
        ----------
        identifier: str
            The ID of a specific illumination element. If `None` then all illumination elements are queried.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.BEAM_ENERGY_PROFILE, identifier)

    def get_beam_stability_profile(self, identifier=None):
        """
        The beam noise profile field is a functional of wavelength (nm) that represents the standard deviation
        of the pulse-to-pulse energy of the illuminator with regard to the wavelength.

        Parameters
        ----------
        identifier: str
            The ID of a specific illumination element. If `None` then all illumination elements are queried.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.BEAM_STABILITY_PROFILE, identifier)

    def get_pulse_width(self, identifier=None):
        """
        The pulse duration or pulse width describes the total length of a light pulse, measured as the time interval
        between the half-power points on the leading and trailing edges of the pulse.

        Parameters
        ----------
        identifier: str
            The ID of a specific illumination element. If `None` then all illumination elements are queried.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.PULSE_WIDTH, identifier)

    def get_beam_profile(self, identifier=None):
        """
        The beam intensity profile is a function of a spatial position that specifies the relative beam
        intensity according to the planar emitting surface of the illuminator shape.

        Parameters
        ----------
        identifier: str
            The ID of a specific illumination element. If `None` then all illumination elements are queried.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.BEAM_INTENSITY_PROFILE, identifier)

    def get_beam_profile_distance(self, identifier=None):
        """
        The distance from the light source for measuring its beam intensity profile.

        Parameters
        ----------
        identifier: str
            The ID of a specific illumination element. If `None` then all illumination elements are queried.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.INTENSITY_PROFILE_DISTANCE, identifier)

    def get_beam_divergence(self, identifier=None):
        """
        The beam divergence angles represent the opening angles of the beam from the illuminator shape with
        respect to the orientation vector. This angle represented by the standard deviation of the beam divergence.

        Parameters
        ----------
        identifier: str
            The ID of a specific illumination element. If `None` then all illumination elements are queried.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_illuminator_attribute_for_tag(MetadataDeviceTags.BEAM_DIVERGENCE_ANGLES, identifier)

    def get_illuminator_attribute_for_tag(self, metadatum, identifier=None):
        """
        Method all convenience functions regarding the illumination elements are delegated to.

        Parameters
        ----------
        metadatum: MetaDatum
            The metadatum that corresponds to the information that should be extracted from the metadata dictionary.
        identifier: str
            The ID of a specific illumination element. If `None` then all illumination elements are queried.

        Return
        ------
        object
            return value can be None, of the key was not found in the meta data dictionary.
        """
        if identifier is not None:
            if isinstance(identifier, int):
                if identifier < 0 or identifier >= self.get_number_of_illuminators():
                    raise ValueError("The illuminator position " + str(identifier) + "was out of range.")
                else:
                    return list(self.meta_data_device[MetadataDeviceTags.ILLUMINATORS.tag].values())[identifier][
                        metadatum.tag]
            elif isinstance(identifier, str):
                if identifier not in self.get_illuminator_ids():
                    raise ValueError("The illuminator id " + str(identifier) + "was not valid.")
                else:
                    return self.meta_data_device[MetadataDeviceTags.ILLUMINATORS.tag][identifier][metadatum.tag]
            else:
                raise ValueError("identifier must be int or string.")
        else:
            positions = []
            for id in self.get_illuminator_ids():
                positions.append(self.meta_data_device[MetadataDeviceTags.ILLUMINATORS.tag][id][metadatum.tag])
            if metadatum.dtype == np.ndarray:
                return np.asarray(positions)
            else:
                return positions

    def get_detector_position(self, identifier=None):
        """
        The positions of each detection element in 3D Cartesian coordinates [x1, x2, x3].

        Parameters
        ----------
        identifier: str
            The ID of a specific detection element. If `None` then all detection elements are queried.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_detector_attribute_for_tag(MetadataDeviceTags.DETECTOR_POSITION, identifier)

    def get_regions_of_interest(self):
        """
        A list of named regions within the underlying 3D Cartesian coordinate system (cf. Device Metadata).
        Strings containing the region names are mapped to arrays that define either an approximate cuboid
        area (cf. Field of View) or a list of coordinates describing a set of 3D Cartesian
        coordinates surrounding the named region.

        Return
        ------
        np.ndarray
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.REGIONS_OF_INTEREST)

    def get_detector_orientation(self, identifier=None):
        """
        The element orientation defines the rotation of the detection element in 3D cartesian coordinates
        [r1, r2, r3] in radians.

        Parameters
        ----------
        identifier: str
            The ID of a specific detection element. If `None` then all detection elements are queried.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_detector_attribute_for_tag(MetadataDeviceTags.DETECTOR_ORIENTATION, identifier)

    def get_detector_geometry(self, identifier=None):
        """
        The element size defines the size of the detection element in 3D cartesian coordinates [x1, x2, x3]
        relative to its position and orientation.

        Parameters
        ----------
        identifier: str
            The ID of a specific detection element. If `None` then all detection elements are queried.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_detector_attribute_for_tag(MetadataDeviceTags.DETECTOR_GEOMETRY, identifier)

    def get_detector_geometry_type(self, identifier=None):
        """
        The detector geometry type defines how to interpret the data in the detector geometry field.
        The following geometry types are currently supported:

            - "CIRCULAR" - defined by a single value that determines the radius of the circle
            - "SPHERE" - defined by a single value that determines the radius of the sphere
            - "CUBOID" - defined by three values that determine the extent of the cuboid in x, y, and z dimensions before the position and orientation transforms.
            - "MESH" - defined by a STL-formatted string that determines the positions of points and faces before the position and orientation transforms.

        Parameters
        ----------
        identifier: str
            The ID of a specific detection element. If `None` then all detection elements are queried.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_detector_attribute_for_tag(MetadataDeviceTags.DETECTOR_GEOMETRY_TYPE, identifier)

    def get_frequency_response(self, identifier=None):
        """
        The frequency response is a functional that characterizes the response of the detection element to the
        frequency of the incident pressure waves.

        Parameters
        ----------
        identifier: str
            The ID of a specific detection element. If `None` then all detection elements are queried.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_detector_attribute_for_tag(MetadataDeviceTags.FREQUENCY_RESPONSE, identifier)

    def get_angular_response(self, identifier=None):
        """
        The angular response field characterizes the angular sensitivity of the detection element to the incident
        angle (relative to the elements orientation) of the incoming pressure wave.

        Parameters
        ----------
        identifier: str
            The ID of a specific detection element. If `None` then all detection elements are queried.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_detector_attribute_for_tag(MetadataDeviceTags.ANGULAR_RESPONSE, identifier)

    def get_detector_attribute_for_tag(self, metadatum, identifier=None):
        """
        Method all convenience functions regarding the detection elements are delegated to.

        Parameters
        ----------
        metadatum: MetaDatum
            The metadatum that corresponds to the information that should be extracted from the metadata dictionary.
        identifier: str
            The ID of a specific detection element. If `None` then all detection elements are queried.

        Return
        ------
        object
            return value can be None, of the key was not found in the meta data dictionary.
        """
        if identifier is not None:
            if isinstance(identifier, int):
                if identifier < 0 or identifier >= self.get_number_of_detectors():
                    raise ValueError("The detector position " + str(identifier) + "was out of range.")
                else:
                    return list(self.meta_data_device[MetadataDeviceTags.DETECTORS.tag].values())[identifier][
                        metadatum.tag]
            elif isinstance(identifier, str):
                if identifier not in self.get_detector_ids():
                    raise ValueError("The detector id " + str(identifier) + "was not valid.")
                else:
                    return self.meta_data_device[MetadataDeviceTags.DETECTORS.tag][identifier][metadatum.tag]
            else:
                raise ValueError("detector must be int or string.")
        else:
            positions = []
            for id in self.get_detector_ids():
                positions.append(self.meta_data_device[MetadataDeviceTags.DETECTORS.tag][id][metadatum.tag])
            return np.asarray(positions)

    def get_encoding(self):
        """
        The encoding field is representative of the character set that was used to encode the binary data and the
        metadata. E.g. one of ‘UTF-8’, ‘ASCII’, ‘CP-1252’, …

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.ENCODING)

    def get_compression(self):
        """
        The compression field is representative of the compression method that was used to compress the binary data.
        E.g. one of ‘raw’, ‘gzip’, …

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.COMPRESSION)

    def get_data_UUID(self):
        """
        128-bit Integer displayed as a hexadecimal string in 5 groups separated by hyphens, in the form 8-4-4-4-12 for
        a total of 36 characters. The UUID is randomly generated using the UUID Version 4 standard.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.UUID)

    def get_data_type(self):
        """
        The data type field represents the datatype of the binary data. This field is given in the C++ data type naming
        convention. E.g. ‘short’, ‘unsigned short’, ‘int’, ‘unsigned int’, ‘long’, ‘unsigned long’, ‘long long’,
        ‘float’, ‘double’, ‘long double’.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.DATA_TYPE)

    def get_dimensionality(self):
        """
        The dimensionality field represents the acquisition format of the binary data and specifies the number of
        spatiotemporal dimensions of the data that is comprised of one or more frames. E.g. ‘1D’, ‘2D’, ‘3D’, ‘1D+t’,
        2D+t’, ‘3D+t’. In this notion, the time series sampling of one transducer would count as a “spatial” dimension.
        These are defined as 1D = [𝝉], 2D = [x1, 𝝉], 3D = [x1, 𝝉, x2]. The “+t” will then add a time dimension for
        multiple of these frames.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.DIMENSIONALITY)

    def get_sizes(self):
        """
        The sizes field quantifies the number of data points in each of the dimensions specified in the dimensionality
        field. e.g. [128, 2560, 26] with a “2D+t” dimensionality.

        Return
        ------
        np.ndarray
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.SIZES)

    def get_photoacoustic_imaging_device_reference(self):
        """
        A string referencing the UUID of the PA imaging device description as defined in the Device Metadata.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.PHOTOACOUSTIC_IMAGING_DEVICE_REFERENCE)

    def get_pulse_energy(self):
        """
        A value specifying the pulse energy used to generate the photoacoustic signal.
        If the pulse energies are averaged over many pulses, the average value must be specified.

        Return
        ------
        np.ndarray
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.PULSE_ENERGY)

    def get_measurement_time_stamps(self):
        """
        An array specifying the time at which a measurement was recorded.

        Return
        ------
        np.ndarray
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.MEASUREMENT_TIMESTAMPS)

    def get_acquisition_wavelengths(self):
        """
        A 1D array that contains all wavelengths used for the image acquisition.

        Return
        ------
        np.ndarray
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.ACQUISITION_WAVELENGTHS)

    def get_time_gain_compensation(self):
        """
        An array containing relative
        factors that have been used to correct the time series data for
        the effect of acoustic attenuation.

        Return
        ------
        np.ndarray
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.TIME_GAIN_COMPENSATION)

    def get_overall_gain(self):
        """
        A single value describing a factor used to
        modify the amplitude of the raw time series data.

        Return
        ------
        float
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.OVERALL_GAIN)

    def get_element_dependent_gain(self):
        """
        An array that contains the relative factors used for apodisation or detection element-wise
        sensitivity corrections.

        Return
        ------
        np.ndarray
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.ELEMENT_DEPENDENT_GAIN)

    def get_temperature(self):
        """
        An array describing the temperature of the imaged space (covering both the imaged medium and
        the coupling agent) for each measurement.

        Return
        ------
        np.ndarray
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.TEMPERATURE_CONTROL)

    def get_acoustic_coupling_agent(self):
        """
        A string representing the acoustic coupling agent that is used.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.ACOUSTIC_COUPLING_AGENT)

    def get_speed_of_sound(self):
        """
        Either a single value representing the mean
        global speed of sound in the entire imaged medium or a 3D
        array representing a heterogeneous speed of sound map in
        the device coordinate system. This definition covers both the
        imaged medium and the coupling agent.

        Return
        ------
        np.ndarray
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.SPEED_OF_SOUND)

    def get_scanning_method(self):
        """
        A string representing the scanning
        method that is used. The following descriptions can be used:
        (“composite_scan”, “full_scan”). This flag determines the
        way the metadatum “measurement” is defined.

        Return
        ------
        str
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.SCANNING_METHOD)

    def get_sampling_rate(self):
        """
        A single value referring to the rate at which samples of the analogue signal are taken to be
        converted into digital form.

        Return
        ------
        float
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.AD_SAMPLING_RATE)

    def get_frequency_domain_filter(self):
        """
        The frequency threshold levels that have been applied to filter the raw time series data.

        Return
        ------
        np.ndarray
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.FREQUENCY_DOMAIN_FILTER)

    def get_measurement_spatial_pose(self):
        """
        Coordinates describing the position and orientation changes of the acquisition system
        relative to the measurement of reference (first measurement).

        Return
        ------
        np.ndarray
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.MEASUREMENT_SPATIAL_POSES)

    def get_measurements_per_image(self):
        """
        A single value describing
        the number of measurements that constitute the dataset
        corresponding to one image.

        Return
        ------
        int
            return value can be None, of the key was not found in the meta data dictionary.
        """
        return self.get_acquisition_meta_datum(MetadataAcquisitionTags.MEASUREMENTS_PER_IMAGE)
