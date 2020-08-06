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
from enum import Enum
from abc import ABC, abstractmethod


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
    """
    An unconstrained meta datum
    """

    def __init__(self, tag, mandatory, dtype, unit=Units.NO_UNIT):
        super().__init__(tag, mandatory, dtype, unit)

    def evaluate_value_range(self, value) -> bool:
        if not isinstance(value, self.dtype):
            raise TypeError("The given value was not of the expected data type. Expected ", self.dtype, "but was",
                            type(value).__name__)
        return True


class MetadataDeviceTags(Enum):
    """
    This class defines the naming conventions of the
    """

    def __init__(self, metadatum: MetaDatum):
        self.info = metadatum

    # General purpose fields
    UUID = UnconstrainedMetaDatum("uuid", True, str)
    GENERAL = UnconstrainedMetaDatum("general", True, dict)
    ILLUMINATORS = UnconstrainedMetaDatum("illuminators", True, dict)
    DETECTORS = UnconstrainedMetaDatum("detectors", True, dict)
    FIELD_OF_VIEW = UnconstrainedMetaDatum("field_of_view", False, np.ndarray, Units.METERS)
    NUMBER_OF_ILLUMINATORS = UnconstrainedMetaDatum("num_illuminators", False, int, Units.DIMENSIONLESS_UNIT)
    NUMBER_OF_DETECTORS = UnconstrainedMetaDatum("num_detectors", False, int, Units.DIMENSIONLESS_UNIT)

    # Illumination geometry-specific fields
    ILLUMINATION_ELEMENT = UnconstrainedMetaDatum("illumination_element", False, str)
    ILLUMINATOR_POSITION = UnconstrainedMetaDatum("illuminator_position", False, np.ndarray, Units.METERS)
    ILLUMINATOR_ORIENTATION = UnconstrainedMetaDatum("illuminator_orientation", False, np.ndarray, Units.RADIANS)
    ILLUMINATOR_SHAPE = UnconstrainedMetaDatum("illuminator_shape", False, np.ndarray, Units.METERS)
    WAVELENGTH_RANGE = UnconstrainedMetaDatum("wavelength_range", False, np.ndarray, Units.METERS)
    LASER_ENERGY_PROFILE = UnconstrainedMetaDatum("laser_energy_profile", False, np.ndarray, Units.JOULES)
    LASER_STABILITY_PROFILE = UnconstrainedMetaDatum("laser_stability_profile", False, np.ndarray, Units.JOULES)
    PULSE_WIDTH = UnconstrainedMetaDatum("pulse_width", False, float, Units.SECONDS)
    BEAM_INTENSITY_PROFILE = UnconstrainedMetaDatum("beam_intensity_profile", False, np.ndarray, Units.DIMENSIONLESS_UNIT)
    BEAM_DIVERGENCE_ANGLES = UnconstrainedMetaDatum("beam_divergence_angles", False, float, Units.RADIANS)

    # Detection geometry-specific fields
    DETECTION_ELEMENT = UnconstrainedMetaDatum("detection_element", True, str)
    DETECTOR_POSITION = UnconstrainedMetaDatum("detector_position", True, np.ndarray, Units.METERS)
    DETECTOR_ORIENTATION = UnconstrainedMetaDatum("detector_orientation", False, np.ndarray, Units.RADIANS)
    DETECTOR_SIZE = UnconstrainedMetaDatum("detector_size", False, np.ndarray, Units.METERS)
    FREQUENCY_RESPONSE = UnconstrainedMetaDatum("frequency_response", False, np.ndarray, Units.DIMENSIONLESS_UNIT)
    ANGULAR_RESPONSE = UnconstrainedMetaDatum("angular_response", False, np.ndarray, Units.DIMENSIONLESS_UNIT)


class MetadataTags(Enum):
    """
    Binary time series data meta data tags
    """

    def __init__(self, metadatum: MetaDatum):
        self.info = metadatum

    UUID = UnconstrainedMetaDatum("uuid", True, str)
    ENCODING = UnconstrainedMetaDatum("encoding", True, str)
    COMPRESSION = UnconstrainedMetaDatum("compression", True, str)
    PHOTOACOUSTIC_IMAGING_DEVICE = UnconstrainedMetaDatum("photoacoustic_imaging_device", False, str)
    DATA_TYPE = UnconstrainedMetaDatum("data_type", True, str)
    DIMENSIONALITY = UnconstrainedMetaDatum("dimensionality", True, str)
    SIZES = UnconstrainedMetaDatum("sizes", True, np.ndarray, Units.DIMENSIONLESS_UNIT)
    PULSE_LASER_ENERGY = UnconstrainedMetaDatum("pulse_laser_energy", False, np.ndarray, Units.JOULES)
    FRAME_ACQUISITION_TIMESTAMPS = UnconstrainedMetaDatum("frame_acquisition_timestamps", False, np.ndarray, Units.SECONDS)
    ACQUISITION_OPTICAL_WAVELENGTHS = UnconstrainedMetaDatum("acquisition_optical_wavelengths", False, np.ndarray, Units.METERS)
    TIME_GAIN_COMPNSATION = UnconstrainedMetaDatum("time_gain_compensation", False, np.ndarray, Units.DIMENSIONLESS_UNIT)
    OVERALL_GAIN = UnconstrainedMetaDatum("overall_gain", False, float, Units.DIMENSIONLESS_UNIT)
    ELEMENT_DEPENDENT_GAIN = UnconstrainedMetaDatum("element_dependent_gain", False, np.ndarray, Units.DIMENSIONLESS_UNIT)
    TEMPERATURE_CONTROL = UnconstrainedMetaDatum("temperature_control", False, np.ndarray, Units.KELVIN)
    ACOUSTIC_COUPLING_AGENT = UnconstrainedMetaDatum("acoustic_cupling_agent", False, str)
    SCANNING_METHOD = UnconstrainedMetaDatum("scanning_method", False, str)
    AD_SAMPLING_RATE = UnconstrainedMetaDatum("ad_sampling_rate", True, np.ndarray, Units.HERTZ)
    FREQUENCY_DOMAIN_FILTER = UnconstrainedMetaDatum("frequency_domain_filter", False, str)
    FILTER_THRESHOLD = UnconstrainedMetaDatum("filter_threshold", False, np.ndarray, Units.HERTZ)