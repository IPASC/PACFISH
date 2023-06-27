# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-FileCopyrightText: 2021 Janek Gröhl
# SPDX-FileCopyrightText: 2021 Lina Hacker
# SPDX-License-Identifier: BSD 3-Clause License

import numpy as np
import numbers
from abc import ABC, abstractmethod


DIMENSIONALITY_STRINGS = ['time', 'space', 'time and space']
"""
The Dimenstionality_STRINGS define what the value space of the metadatum DIMENSIONALITY is.
"""


class Units:
    """
    A list of the SI and compound units that are used in the IPASC format.
    """
    NO_UNIT = "N/A"
    DIMENSIONLESS_UNIT = "one"
    METERS = "m"
    RADIANS = "rad"
    JOULES = "J"
    SECONDS = "s"
    KELVIN = "K"
    HERTZ = "Hz"
    METERS_PER_SECOND = "m/s"


class MetaDatum(ABC):
    """
    This class represents a meta datum.
    A meta datum contains all necessary information to fully characterize the meta information
    represented by an instance of this class.
    """

    def __init__(self, tag: str, minimal: bool, dtype: (type, tuple), unit: str = Units.NO_UNIT):
        """
        Instantiates a MetaDatum and sets all relevant values.

        Parameters
        ----------
        tag: str
            The tag that corresponds to this meta datum.

        minimal: bool
            Defines if the metadatum is `minimal` (i.e. if is MUST be reported). Without the
            minimal parameters, the time series data cannot be reconstructed into an image.
            All parameters that are not minimal are interpreted as "report if present".
        dtype: type, tuple
            The data type of the meta datum. Can either be a single type or a tuple of possible types.
        unit: str
            The unit associated with this metadatum. Must be one of the strings defined in pacfish.Units.

        Raises
        ------
        TypeError:
            if one of the parameters is not of the correct type.
        """

        if tag is not None and isinstance(tag, str):
            self.tag = tag
        else:
            raise TypeError("tag parameter was not of type 'string'")

        if minimal is not None and isinstance(minimal, bool):
            self.mandatory = minimal
        else:
            raise TypeError("mandatory parameter was not of type 'bool'")

        if unit is not None and isinstance(unit, str):
            self.unit = unit
        else:
            raise TypeError("unit parameter was not of type 'string'")

        self.dtype = dtype

    @abstractmethod
    def evaluate_value_range(self, value) -> bool:
        """
        Evaluates if a given value fits to the acceptable value range of the MetaDatum.

        Parameters
        ----------
        value: object
            value to evaluate

        Return
        ------
        bool
            True if the given value is acceptable for the respective MetaDatum
        """
        pass


class UnconstrainedMetaDatum(MetaDatum):
    """
    This MetaDatum has no limitations on the values associated with it.
    """

    def __init__(self, tag, minimal, dtype, unit=Units.NO_UNIT):
        super().__init__(tag, minimal, dtype, unit)

    def evaluate_value_range(self, value) -> bool:
        if value is None:
            return False

        if not isinstance(value, self.dtype):
            raise TypeError("The given value of", self.tag, "was not of the expected data type. Expected ",
                            self.dtype, "but was",
                            type(value).__name__)
        return True


class NonNegativeWholeNumber(MetaDatum):
    """
    This MetaDatum is defined to be a non-negative whole number.
    """
    def __init__(self, tag, minimal, dtype, unit=Units.NO_UNIT):
        super().__init__(tag, minimal, dtype, unit)

    def evaluate_value_range(self, value) -> bool:
        if value is None:
            return False

        if not isinstance(value, int):
            if not (isinstance(value, np.ndarray) and len(np.shape(value)) == 0):
                raise TypeError("The given value of", self.tag, "was not of the expected data type. Expected ",
                                "int but was", type(value).__name__)
        return value >= 0


class NonNegativeNumbersInArray(MetaDatum):
    """
    This MetaDatum is defined to be an array containing non-negative whole numbers.
    """
    def __init__(self, tag, minimal, dtype, unit=Units.NO_UNIT):
        super().__init__(tag, minimal, dtype, unit)

    def evaluate_value_range(self, value) -> bool:
        if value is None:
            return False

        if not isinstance(value, np.ndarray):
            raise TypeError("The given value of", self.tag, "was not of the expected data type. Expected ",
                            "np.ndarray but was", type(value).__name__)

        for number in np.reshape(value, (-1, )):
            if number < 0:
                return False
        return True


class NumberWithUpperAndLowerLimit(MetaDatum):
    """
    This MetaDatum is defined to be a whole number in between a lower and an upper bound (inclusive).
    """
    def __init__(self, tag, minimal, dtype, unit=Units.NO_UNIT, lower_limit=-np.inf, upper_limit=np.inf):
        super().__init__(tag, minimal, dtype, unit)
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit

    def evaluate_value_range(self, value) -> bool:
        if value is None:
            return False

        if isinstance(value, np.ndarray):
            for item in np.reshape(value, (-1, )):
                if not self.lower_limit <= item <= self.upper_limit:
                    return False
            return True
        if not isinstance(value, numbers.Number):
            raise TypeError("The given value of", self.tag, "was not of the expected data type. Expected ",
                            "a number or numpy array but was", type(value).__name__)

        return self.lower_limit <= value <= self.upper_limit


class NDimensionalNumpyArray(MetaDatum):
    """
    This MetaDatum is defined to be an array of unconstrained numbers.
    """
    def __init__(self, tag, minimal, dtype, unit=Units.NO_UNIT, expected_array_dimension=1):
        super().__init__(tag, minimal, dtype, unit)
        self.expected_array_dimension = expected_array_dimension

    def evaluate_value_range(self, value) -> bool:
        if value is None:
            return False

        if not isinstance(value, np.ndarray):
            raise TypeError("A N-Dimensional array must be of type numpy.ndarray, but was", type(value).__name__)

        if len(np.shape(np.atleast_1d(value))) != self.expected_array_dimension:
            return False

        return True


class NDimensionalNumpyArrayWithMElements(MetaDatum):
    """
    This MetaDatum is defined to be an array with a specific dimensionality.
    """
    def __init__(self, tag, minimal, dtype, unit=Units.NO_UNIT, expected_array_dimension=1,
                 elements_per_dimension=None):
        super().__init__(tag, minimal, dtype, unit)
        self.expected_array_dimension = expected_array_dimension
        self.elements_per_dimension = elements_per_dimension

    def evaluate_value_range(self, value) -> bool:
        if value is None:
            return False

        if not isinstance(value, np.ndarray):
            raise TypeError("A N-Dimensional array must be of type numpy.ndarray, but was", type(value).__name__)

        num_dimensions_correct = len(np.shape(value)) == self.expected_array_dimension
        dimension_elements_correct = True
        if self.elements_per_dimension is not None:
            if len(np.shape(value)) != len(self.elements_per_dimension):
                dimension_elements_correct = False
            else:
                dimension_elements_correct = False not in [val == self.elements_per_dimension[idx] for idx, val in
                                                           enumerate(np.shape(value))]

        return num_dimensions_correct and dimension_elements_correct


class NonNegativeNumber(MetaDatum):
    """
    This MetaDatum is defined to be a non-negative number.
    """
    def __init__(self, tag, minimal, dtype, unit=Units.NO_UNIT):
        super().__init__(tag, minimal, dtype, unit)

    def evaluate_value_range(self, value) -> bool:
        if value is None:
            return False

        if not isinstance(value, self.dtype):
            if not (isinstance(value, np.ndarray) and len(np.shape(value))==0):
                raise TypeError("The given value of", self.tag, "was not of the expected data type. Expected ", self.dtype,
                                "but was",
                                type(value).__name__)

        return value >= 0.0


class EnumeratedString(MetaDatum):
    """
    This MetaDatum is defined to be a string that must be from a defined list of strings.
    """
    def __init__(self, tag, minimal, dtype, unit=Units.NO_UNIT, permissible_strings=None):
        super().__init__(tag, minimal, dtype, unit)
        self.permissible_strings = permissible_strings

    def evaluate_value_range(self, value) -> bool:
        if value is None:
            return False

        if not isinstance(value, self.dtype):
            raise TypeError("The given value of", self.tag, "was not of the expected data type. Expected ", self.dtype, "but was",
                            type(value).__name__)

        if self.permissible_strings is None:
            return False

        return value in self.permissible_strings


class MetadataDeviceTags:
    """
    This class defines the MetaData that compose all information needed to describe a
    digital twin of a photoacoustic device.

    It also specifies the naming conventions of the underlying HDF5 data fields.
    Furthermore, it is specified if a certain meta datum is minimal or not, the data type
    is defined and the units of the metadatum are given.
    """
    # General purpose fields
    UNIQUE_IDENTIFIER = UnconstrainedMetaDatum("unique_identifier", True, str)
    GENERAL = UnconstrainedMetaDatum("general", True, dict)
    ILLUMINATORS = UnconstrainedMetaDatum("illuminators", False, dict)
    DETECTORS = UnconstrainedMetaDatum("detectors", True, dict)
    FIELD_OF_VIEW = NDimensionalNumpyArrayWithMElements("field_of_view", True, np.ndarray, Units.METERS,
                                                        expected_array_dimension=1, elements_per_dimension=[6])
    NUMBER_OF_ILLUMINATION_ELEMENTS = NonNegativeWholeNumber("num_illuminators", False, int, Units.DIMENSIONLESS_UNIT)
    NUMBER_OF_DETECTION_ELEMENTS = NonNegativeWholeNumber("num_detectors", False, int, Units.DIMENSIONLESS_UNIT)

    # Illumination geometry-specific fields
    ILLUMINATION_ELEMENT = UnconstrainedMetaDatum("illumination_element", False, str)
    ILLUMINATOR_POSITION = NDimensionalNumpyArray("illuminator_position", False, np.ndarray, Units.METERS,
                                                  expected_array_dimension=1)
    ILLUMINATOR_ORIENTATION = NDimensionalNumpyArray("illuminator_orientation", False, np.ndarray, Units.METERS,
                                                     expected_array_dimension=1)
    ILLUMINATOR_GEOMETRY = UnconstrainedMetaDatum("illuminator_geometry", False, (float, np.ndarray, str),
                                                  Units.METERS)
    ILLUMINATOR_GEOMETRY_TYPE = UnconstrainedMetaDatum("illuminator_geometry_type", False, str, Units.METERS)
    WAVELENGTH_RANGE = NDimensionalNumpyArray("wavelength_range", False, np.ndarray, Units.METERS,
                                              expected_array_dimension=1)
    BEAM_ENERGY_PROFILE = NDimensionalNumpyArray("beam_energy_profile", False, np.ndarray, Units.JOULES,
                                                 expected_array_dimension=2)
    BEAM_STABILITY_PROFILE = NDimensionalNumpyArray("beam_stability_profile", False, np.ndarray, Units.JOULES,
                                                    expected_array_dimension=2)
    PULSE_WIDTH = NonNegativeNumber("pulse_width", False, float, Units.SECONDS)
    BEAM_INTENSITY_PROFILE = NDimensionalNumpyArray("beam_intensity_profile", False, np.ndarray,
                                                    Units.DIMENSIONLESS_UNIT,
                                                    expected_array_dimension=2)
    INTENSITY_PROFILE_DISTANCE = NonNegativeNumber("intensity_profile_distance", False, float, Units.METERS)
    BEAM_DIVERGENCE_ANGLES = NumberWithUpperAndLowerLimit("beam_divergence_angles", False, float, Units.RADIANS,
                                                          lower_limit=0, upper_limit=2*np.pi)

    # Detection geometry-specific fields
    DETECTION_ELEMENT = UnconstrainedMetaDatum("detection_element", True, str)
    DETECTOR_POSITION = NDimensionalNumpyArray("detector_position", True, np.ndarray, Units.METERS,
                                               expected_array_dimension=1)
    DETECTOR_ORIENTATION = NDimensionalNumpyArray("detector_orientation", False, np.ndarray, Units.METERS,
                                                  expected_array_dimension=1)
    DETECTOR_GEOMETRY = UnconstrainedMetaDatum("detector_geometry", False, (float, np.ndarray, str),
                                               Units.METERS)

    DETECTOR_GEOMETRY_TYPE = UnconstrainedMetaDatum("detector_geometry_type", False, str, Units.METERS)

    FREQUENCY_RESPONSE = NonNegativeNumbersInArray("frequency_response", False, np.ndarray,
                                                Units.HERTZ + " / " + Units.DIMENSIONLESS_UNIT)
    ANGULAR_RESPONSE = NDimensionalNumpyArray("angular_response", False, np.ndarray,
                                              Units.RADIANS + " / " + Units.DIMENSIONLESS_UNIT,
                                              expected_array_dimension=2)

    TAGS_GENERAL = [GENERAL, UNIQUE_IDENTIFIER, ILLUMINATORS, DETECTORS, FIELD_OF_VIEW, NUMBER_OF_ILLUMINATION_ELEMENTS,
                    NUMBER_OF_DETECTION_ELEMENTS]
    TAGS_ILLUMINATORS = [ILLUMINATION_ELEMENT, ILLUMINATOR_POSITION, ILLUMINATOR_ORIENTATION, ILLUMINATOR_GEOMETRY,
                         ILLUMINATOR_GEOMETRY_TYPE,
                         WAVELENGTH_RANGE, BEAM_ENERGY_PROFILE, BEAM_STABILITY_PROFILE, PULSE_WIDTH,
                         BEAM_INTENSITY_PROFILE, INTENSITY_PROFILE_DISTANCE, BEAM_DIVERGENCE_ANGLES]
    TAGS_DETECTORS = [DETECTION_ELEMENT, DETECTOR_POSITION, DETECTOR_ORIENTATION, DETECTOR_GEOMETRY, FREQUENCY_RESPONSE,
                      ANGULAR_RESPONSE, DETECTOR_GEOMETRY_TYPE]
    TAGS = TAGS_GENERAL + TAGS_DETECTORS + TAGS_ILLUMINATORS


class MetadataAcquisitionTags:
    """
    This class defines the MetaData that compose all information needed to describe the
    measurement circumstances for a given measurement of photoacoustic time series data.

    It also specifies the naming conventions of the underlying HDF5 data fields.
    Furthermore, it is specified if a certain meta datum is minimal or not, the data type
    is defined and the units of the metadatum are given.
    """

    UUID = UnconstrainedMetaDatum("uuid", True, str)
    ENCODING = UnconstrainedMetaDatum("encoding", True, str)
    COMPRESSION = UnconstrainedMetaDatum("compression", True, str)
    VERSION = UnconstrainedMetaDatum("version", True, str)

    DATA_TYPE = UnconstrainedMetaDatum("data_type", True, str)
    DIMENSIONALITY = EnumeratedString("dimensionality", True, str, permissible_strings=DIMENSIONALITY_STRINGS)
    SIZES = NonNegativeNumbersInArray("sizes", True, np.ndarray, Units.DIMENSIONLESS_UNIT)

    REGIONS_OF_INTEREST = UnconstrainedMetaDatum("regions_of_interest", False, dict, Units.METERS)
    PHOTOACOUSTIC_IMAGING_DEVICE_REFERENCE = UnconstrainedMetaDatum("photoacoustic_imaging_device_reference", False, str)
    PULSE_ENERGY = NonNegativeNumbersInArray("pulse_energy", False, np.ndarray, Units.JOULES)
    MEASUREMENT_TIMESTAMPS = NonNegativeNumbersInArray("measurement_timestamps", False,
                                                       np.ndarray, Units.SECONDS)
    MEASUREMENT_SPATIAL_POSES = NDimensionalNumpyArray("measurement_spatial_poses", False,
                                                       np.ndarray, Units.SECONDS,
                                                       expected_array_dimension=2)
    ACQUISITION_WAVELENGTHS = NDimensionalNumpyArray("acquisition_wavelengths", False,
                                                     np.ndarray, Units.METERS, expected_array_dimension=1)
    TIME_GAIN_COMPENSATION = NonNegativeNumbersInArray("time_gain_compensation", False, np.ndarray,
                                                       Units.DIMENSIONLESS_UNIT)
    OVERALL_GAIN = NonNegativeNumber("overall_gain", False, float, Units.DIMENSIONLESS_UNIT)
    ELEMENT_DEPENDENT_GAIN = NonNegativeNumbersInArray("element_dependent_gain", False, np.ndarray,
                                                       Units.DIMENSIONLESS_UNIT)
    TEMPERATURE_CONTROL = NonNegativeNumbersInArray("temperature_control", False, np.ndarray, Units.KELVIN)
    ACOUSTIC_COUPLING_AGENT = UnconstrainedMetaDatum("acoustic_coupling_agent", False, str)
    SCANNING_METHOD = UnconstrainedMetaDatum("scanning_method", False, str)
    SPEED_OF_SOUND = UnconstrainedMetaDatum("speed_of_sound", False, (np.ndarray, float), Units.METERS_PER_SECOND)
    AD_SAMPLING_RATE = NonNegativeNumber("ad_sampling_rate", True, float, Units.HERTZ)
    FREQUENCY_DOMAIN_FILTER = UnconstrainedMetaDatum("frequency_domain_filter", False, np.ndarray)
    MEASUREMENTS_PER_IMAGE = NonNegativeWholeNumber("measurements_per_image", False, int)
    ULTRASOUND_IMAGE_DATA = UnconstrainedMetaDatum("ultrasound_image_data", False, np.ndarray)
    ULTRASOUND_IMAGE_TIMESTAMPS = UnconstrainedMetaDatum("ultrasound_image_timestamps", False, np.ndarray)

    TAGS_BINARY = [DATA_TYPE, DIMENSIONALITY, SIZES, VERSION]
    TAGS_CONTAINER = [UUID, ENCODING, COMPRESSION]
    TAGS_ACQUISITION = [PHOTOACOUSTIC_IMAGING_DEVICE_REFERENCE, PULSE_ENERGY, ACQUISITION_WAVELENGTHS,
                        TIME_GAIN_COMPENSATION, OVERALL_GAIN, ELEMENT_DEPENDENT_GAIN, TEMPERATURE_CONTROL,
                        ACOUSTIC_COUPLING_AGENT, SCANNING_METHOD, AD_SAMPLING_RATE, FREQUENCY_DOMAIN_FILTER,
                        SPEED_OF_SOUND, MEASUREMENTS_PER_IMAGE, REGIONS_OF_INTEREST, MEASUREMENT_TIMESTAMPS,
                        MEASUREMENT_SPATIAL_POSES, ULTRASOUND_IMAGE_DATA, ULTRASOUND_IMAGE_TIMESTAMPS]
    TAGS = TAGS_BINARY + TAGS_ACQUISITION + TAGS_CONTAINER
