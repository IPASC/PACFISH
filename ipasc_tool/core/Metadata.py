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
import numbers
from abc import ABC, abstractmethod


DIMENSIONALITY_STRINGS = ['1D', '2D', '3D', '1D+t', '2D+t', '3D+t']


class Units:
    NO_UNIT = "N/A"
    DIMENSIONLESS_UNIT = "one"
    METERS = "m"
    RADIANS = "rad"
    JOULES = "J"
    SECONDS = "s"
    KELVIN = "K"
    HERTZ = "Hz"


class MetaDatum(ABC):
    """
    This class represents a meta datum.
    A meta datum contains all necessary information to fully characterize the meta information
    represented by an instance of this class.
    """

    def __init__(self, tag: str, mandatory: bool, dtype: type, unit: str = Units.NO_UNIT):
        """

        :param tag:
        :param mandatory:
        :param dtype:
        :param unit:
        :raises TypeError if one of the parameters is not of correct type.
        """

        if tag is not None and isinstance(tag, str):
            self.tag = tag
        else:
            raise TypeError("tag parameter was not of type 'string'")

        if mandatory is not None and isinstance(mandatory, bool):
            self.mandatory = mandatory
        else:
            raise TypeError("mandatory parameter was not of type 'bool'")

        if unit is not None and isinstance(unit, str):
            self.unit = unit
        else:
            raise TypeError("unit parameter was not of type 'string'")

        self.dtype = dtype

    @abstractmethod
    def evaluate_value_range(self, value) -> bool:
        pass


class UnconstrainedMetaDatum(MetaDatum):
    def __init__(self, tag, mandatory, dtype, unit=Units.NO_UNIT):
        super().__init__(tag, mandatory, dtype, unit)

    def evaluate_value_range(self, value) -> bool:
        if value is None:
            return False

        if not isinstance(value, self.dtype):
            raise TypeError("The given value of", self.tag, "was not of the expected data type. Expected ",
                            self.dtype, "but was",
                            type(value).__name__)
        return True


class NonNegativeWholeNumber(MetaDatum):
    def __init__(self, tag, mandatory, dtype, unit=Units.NO_UNIT):
        super().__init__(tag, mandatory, dtype, unit)

    def evaluate_value_range(self, value) -> bool:
        if value is None:
            return False

        if not isinstance(value, self.dtype):
            raise TypeError("The given value of", self.tag, "was not of the expected data type. Expected ",
                            self.dtype, "but was",
                            type(value).__name__)
        if not isinstance(value, int):
            raise TypeError("Whole numbers must be of type int, but was", type(value).__name__)
        return value >= 0


class NonNegativeNumbersInArray(MetaDatum):
    def __init__(self, tag, mandatory, dtype, unit=Units.NO_UNIT):
        super().__init__(tag, mandatory, dtype, unit)

    def evaluate_value_range(self, value) -> bool:
        if value is None:
            return False

        if not isinstance(value, self.dtype):
            raise TypeError("The given value of", self.tag, "was not of the expected data type. Expected ",
                            self.dtype, "but was",
                            type(value).__name__)
        if not isinstance(value, np.ndarray):
            raise TypeError("A sequence of numbers must be of type numpy.ndarray, but was", type(value).__name__)

        for number in np.reshape(value, (-1, )):
            if number < 0:
                return False
        return True


class NumberWithUpperAndLowerLimit(MetaDatum):
    def __init__(self, tag, mandatory, dtype, unit=Units.NO_UNIT, lower_limit=-np.inf, upper_limit=np.inf):
        super().__init__(tag, mandatory, dtype, unit)
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit

    def evaluate_value_range(self, value) -> bool:
        if value is None:
            return False

        if not isinstance(value, self.dtype):
            raise TypeError("The given value of", self.tag, "was not of the expected data type. Expected ",
                            self.dtype, "but was",
                            type(value).__name__)
        if isinstance(value, np.ndarray):
            for item in np.reshape(value, (-1, )):
                if not self.lower_limit <= item <= self.upper_limit:
                    return False
            return True

        if not isinstance(value, numbers.Number):
            raise TypeError("Expected value of", self.tag, "to be a number, but was", type(value).__name__)

        return self.lower_limit <= value <= self.upper_limit


class NDimensionalNumpyArray(MetaDatum):
    def __init__(self, tag, mandatory, dtype, unit=Units.NO_UNIT, expected_array_dimension=1):
        super().__init__(tag, mandatory, dtype, unit)
        self.expected_array_dimension = expected_array_dimension

    def evaluate_value_range(self, value) -> bool:
        if value is None:
            return False

        if not isinstance(value, self.dtype):
            raise TypeError("The given value of", self.tag, "was not of the expected data type. Expected ", self.dtype, "but was",
                            type(value).__name__)
        if not isinstance(value, np.ndarray):
            raise TypeError("A N-Dimensional array must be of type numpy.ndarray, but was", type(value).__name__)

        return len(np.shape(value)) == self.expected_array_dimension


class NonNegativeNumber(MetaDatum):
    def __init__(self, tag, mandatory, dtype, unit=Units.NO_UNIT):
        super().__init__(tag, mandatory, dtype, unit)

    def evaluate_value_range(self, value) -> bool:
        if value is None:
            return False

        if not isinstance(value, self.dtype):
            raise TypeError("The given value of", self.tag, "was not of the expected data type. Expected ", self.dtype, "but was",
                            type(value).__name__)
        if not isinstance(value, numbers.Number):
            raise TypeError("Expected value of", self.tag, "to be a number, but was", type(value).__name__)

        return value >= 0.0


class EnumeratedString(MetaDatum):
    def __init__(self, tag, mandatory, dtype, unit=Units.NO_UNIT, permissible_strings=None):
        super().__init__(tag, mandatory, dtype, unit)
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
    This class defines the naming conventions of the
    """
    # General purpose fields
    UUID = UnconstrainedMetaDatum("uuid", True, str)
    GENERAL = UnconstrainedMetaDatum("general", True, dict)
    ILLUMINATORS = UnconstrainedMetaDatum("illuminators", True, dict)
    DETECTORS = UnconstrainedMetaDatum("detectors", True, dict)
    FIELD_OF_VIEW = UnconstrainedMetaDatum("field_of_view", False, np.ndarray, Units.METERS)
    NUMBER_OF_ILLUMINATORS = NonNegativeWholeNumber("num_illuminators", False, int, Units.DIMENSIONLESS_UNIT)
    NUMBER_OF_DETECTORS = NonNegativeWholeNumber("num_detectors", False, int, Units.DIMENSIONLESS_UNIT)

    # Illumination geometry-specific fields
    ILLUMINATION_ELEMENT = UnconstrainedMetaDatum("illumination_element", False, str)
    ILLUMINATOR_POSITION = UnconstrainedMetaDatum("illuminator_position", False, np.ndarray, Units.METERS)
    ILLUMINATOR_ORIENTATION = NumberWithUpperAndLowerLimit("illuminator_orientation", False, np.ndarray, Units.RADIANS,
                                                           lower_limit=-2*np.pi, upper_limit=2*np.pi)
    ILLUMINATOR_SHAPE = UnconstrainedMetaDatum("illuminator_shape", False, np.ndarray, Units.METERS)  # FIXME: Consistent behavior with detectors
    WAVELENGTH_RANGE = UnconstrainedMetaDatum("wavelength_range", False, np.ndarray, Units.METERS)
    LASER_ENERGY_PROFILE = NDimensionalNumpyArray("laser_energy_profile", False, np.ndarray, Units.JOULES,
                                                  expected_array_dimension=2)
    LASER_STABILITY_PROFILE = NDimensionalNumpyArray("laser_stability_profile", False, np.ndarray, Units.JOULES,
                                                     expected_array_dimension=2)
    PULSE_WIDTH = NonNegativeNumber("pulse_width", False, float, Units.SECONDS)
    BEAM_INTENSITY_PROFILE = NonNegativeNumbersInArray("beam_intensity_profile", False, np.ndarray,
                                                       Units.DIMENSIONLESS_UNIT)
    BEAM_DIVERGENCE_ANGLES = NumberWithUpperAndLowerLimit("beam_divergence_angles", False, float, Units.RADIANS,
                                                          lower_limit=0, upper_limit=2*np.pi)

    # Detection geometry-specific fields
    DETECTION_ELEMENT = UnconstrainedMetaDatum("detection_element", True, str)
    DETECTOR_POSITION = UnconstrainedMetaDatum("detector_position", True, np.ndarray, Units.METERS)
    DETECTOR_ORIENTATION = NumberWithUpperAndLowerLimit("detector_orientation", False, np.ndarray, Units.RADIANS,
                                                        lower_limit=-2*np.pi, upper_limit=2*np.pi)
    DETECTOR_SIZE = UnconstrainedMetaDatum("detector_size", False, np.ndarray, Units.METERS)  # FIXME: Consistent behavior with illuminators
    FREQUENCY_RESPONSE = NDimensionalNumpyArray("frequency_response", False, np.ndarray, Units.DIMENSIONLESS_UNIT,
                                                expected_array_dimension=2)
    ANGULAR_RESPONSE = NDimensionalNumpyArray("angular_response", False, np.ndarray, Units.DIMENSIONLESS_UNIT,
                                              expected_array_dimension=2)

    TAGS_GENERAL = [GENERAL, UUID, ILLUMINATORS, DETECTORS, FIELD_OF_VIEW, NUMBER_OF_ILLUMINATORS, NUMBER_OF_DETECTORS]
    TAGS_ILLUMONATORS = [ILLUMINATION_ELEMENT, ILLUMINATOR_POSITION, ILLUMINATOR_ORIENTATION, ILLUMINATOR_SHAPE,
                         WAVELENGTH_RANGE, LASER_ENERGY_PROFILE, LASER_STABILITY_PROFILE, PULSE_WIDTH,
                         BEAM_INTENSITY_PROFILE, BEAM_DIVERGENCE_ANGLES]
    TAGS_DETECTORS = [DETECTION_ELEMENT, DETECTOR_POSITION, DETECTOR_ORIENTATION, DETECTOR_SIZE, FREQUENCY_RESPONSE,
                      ANGULAR_RESPONSE]
    TAGS = TAGS_GENERAL + TAGS_DETECTORS + TAGS_ILLUMONATORS


class MetadataAcquisitionTags:
    """
    Binary time series data meta data tags
    """

    UUID = UnconstrainedMetaDatum("uuid", True, str)
    ENCODING = UnconstrainedMetaDatum("encoding", True, str)
    COMPRESSION = UnconstrainedMetaDatum("compression", True, str)
    PHOTOACOUSTIC_IMAGING_DEVICE = UnconstrainedMetaDatum("photoacoustic_imaging_device", False, str)
    DATA_TYPE = UnconstrainedMetaDatum("data_type", True, str)
    DIMENSIONALITY = EnumeratedString("dimensionality", True, str, permissible_strings=DIMENSIONALITY_STRINGS)
    SIZES = NonNegativeNumbersInArray("sizes", True, np.ndarray, Units.DIMENSIONLESS_UNIT)
    PULSE_LASER_ENERGY = NonNegativeNumbersInArray("pulse_laser_energy", False, np.ndarray, Units.JOULES)
    FRAME_ACQUISITION_TIMESTAMPS = NonNegativeNumbersInArray("frame_acquisition_timestamps", False, np.ndarray, Units.SECONDS)
    ACQUISITION_OPTICAL_WAVELENGTHS = NonNegativeNumbersInArray("acquisition_optical_wavelengths", False, np.ndarray, Units.METERS)
    TIME_GAIN_COMPENSATION = NonNegativeNumbersInArray("time_gain_compensation", False, np.ndarray, Units.DIMENSIONLESS_UNIT)
    OVERALL_GAIN = NonNegativeNumber("overall_gain", False, float, Units.DIMENSIONLESS_UNIT)
    ELEMENT_DEPENDENT_GAIN = NonNegativeNumbersInArray("element_dependent_gain", False, np.ndarray, Units.DIMENSIONLESS_UNIT)
    TEMPERATURE_CONTROL = NonNegativeNumbersInArray("temperature_control", False, np.ndarray, Units.KELVIN)
    ACOUSTIC_COUPLING_AGENT = UnconstrainedMetaDatum("acoustic_coupling_agent", False, str)
    SCANNING_METHOD = UnconstrainedMetaDatum("scanning_method", False, str)
    AD_SAMPLING_RATE = NonNegativeNumber("ad_sampling_rate", True, float, Units.HERTZ)
    FREQUENCY_DOMAIN_FILTER = UnconstrainedMetaDatum("frequency_domain_filter", False, np.ndarray)

    TAGS_BINARY = [DATA_TYPE, DIMENSIONALITY, SIZES]
    TAGS_CONTAINER = [UUID, ENCODING, COMPRESSION]
    TAGS_ACQUISITION = [PHOTOACOUSTIC_IMAGING_DEVICE, PULSE_LASER_ENERGY, ACQUISITION_OPTICAL_WAVELENGTHS,
                        TIME_GAIN_COMPENSATION, OVERALL_GAIN, ELEMENT_DEPENDENT_GAIN, TEMPERATURE_CONTROL,
                        ACOUSTIC_COUPLING_AGENT, SCANNING_METHOD, AD_SAMPLING_RATE, FREQUENCY_DOMAIN_FILTER]
    TAGS = TAGS_BINARY + TAGS_ACQUISITION + TAGS_CONTAINER
