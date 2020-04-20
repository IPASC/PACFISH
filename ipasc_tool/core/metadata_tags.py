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


class Units:
    NO_UNIT = "N/A"
    DIMENSIONLESS_UNIT = "one"
    METERS = "m"
    RADIANS = "rad"
    JOULES = "J"
    SECONDS = "s"
    KELVIN = "K"
    HERTZ = "Hz"


class MetaDatum:
    """
    This class represents a meta datum.
    A meta datum contains all necessary information to fully characterize the meta information
    represented by an instance of this class.
    """

    def __init__(self, tag, mandatory, dtype, unit=Units.NO_UNIT):
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


class MetadataDeviceTags(Enum):
    """
    This class defines the naming conventions of the
    """

    def __init__(self, metadatum: MetaDatum):
        self.info = metadatum

    # General purpose fields
    UUID = MetaDatum("uuid", True, str)
    GENERAL = MetaDatum("general", True, dict)
    ILLUMINATORS = MetaDatum("illuminators", True, dict)
    DETECTORS = MetaDatum("detectors", True, dict)
    FIELD_OF_VIEW = MetaDatum("field_of_view", False, np.ndarray, Units.METERS)
    NUMBER_OF_ILLUMINATORS = MetaDatum("num_illuminators", False, int, Units.DIMENSIONLESS_UNIT)
    NUMBER_OF_DETECTORS = MetaDatum("num_detectors", False, int, Units.DIMENSIONLESS_UNIT)

    # Illumination geometry-specific fields
    ILLUMINATION_ELEMENT = MetaDatum("illumination_element", False, str)
    ILLUMINATOR_POSITION = MetaDatum("illuminator_position", False, np.ndarray, Units.METERS)
    ILLUMINATOR_ORIENTATION = MetaDatum("illuminator_orientation", False, np.ndarray, Units.RADIANS)
    ILLUMINATOR_SHAPE = MetaDatum("illuminator_shape", False, np.ndarray, Units.METERS)
    WAVELENGTH_RANGE = MetaDatum("wavelength_range", False, np.ndarray, Units.METERS)
    LASER_ENERGY_PROFILE = MetaDatum("laser_energy_profile", False, np.ndarray, Units.JOULES)
    LASER_STABILITY_PROFILE = MetaDatum("laser_stability_profile", False, np.ndarray, Units.JOULES)
    PULSE_WIDTH = MetaDatum("pulse_width", False, float, Units.SECONDS)
    BEAM_INTENSITY_PROFILE = MetaDatum("beam_intensity_profile", False, np.ndarray, Units.DIMENSIONLESS_UNIT)
    BEAM_DIVERGENCE_ANGLES = MetaDatum("beam_divergence_angles", False, float, Units.RADIANS)

    # Detection geometry-specific fields
    DETECTION_ELEMENT = MetaDatum("detection_element", True, str)
    DETECTOR_POSITION = MetaDatum("detector_position", True, np.ndarray, Units.METERS)
    DETECTOR_ORIENTATION = MetaDatum("detector_orientation", False, np.ndarray, Units.RADIANS)
    DETECTOR_SIZE = MetaDatum("detector_size", False, np.ndarray, Units.METERS)
    FREQUENCY_RESPONSE = MetaDatum("frequency_response", False, np.ndarray, Units.DIMENSIONLESS_UNIT)
    ANGULAR_RESPONSE = MetaDatum("angular_response", False, np.ndarray, Units.DIMENSIONLESS_UNIT)


class MetadataTags(Enum):
    """
    Binary time series data meta data tags
    """

    def __init__(self, metadatum: MetaDatum):
        self.info = metadatum

    UUID = MetaDatum("uuid", True, str)
    ENCODING = MetaDatum("encoding", True, str)
    COMPRESSION = MetaDatum("compression", True, str)
    PHOTOACOUSTIC_IMAGING_DEVICE = MetaDatum("photoacoustic_imaging_device", False, str)
    DATA_TYPE = MetaDatum("data_type", True, str)
    DIMENSIONALITY = MetaDatum("dimensionality", True, str)
    SIZES = MetaDatum("sizes", True, np.ndarray, Units.DIMENSIONLESS_UNIT)
    PULSE_LASER_ENERGY = MetaDatum("pulse_laser_energy", False, np.ndarray, Units.JOULES)
    FRAME_ACQUISITION_TIMESTAMPS = MetaDatum("frame_acquisition_timestamps", False, np.ndarray, Units.SECONDS)
    ACQUISITION_OPTICAL_WAVELENGTHS = MetaDatum("acquisition_optical_wavelengths", False, np.ndarray, Units.METERS)
    TIME_GAIN_COMPNSATION = MetaDatum("time_gain_compensation", False, np.ndarray, Units.DIMENSIONLESS_UNIT)
    OVERALL_GAIN = MetaDatum("overall_gain", False, float, Units.DIMENSIONLESS_UNIT)
    ELEMENT_DEPENDENT_GAIN = MetaDatum("element_dependent_gain", False, np.ndarray, Units.DIMENSIONLESS_UNIT)
    TEMPERATURE_CONTROL = MetaDatum("temperature_control", False, np.ndarray, Units.KELVIN)
    ACOUSTIC_COUPLING_AGENT = MetaDatum("acoustic_cupling_agent", False, str)
    SCANNING_METHOD = MetaDatum("scanning_method", False, str)
    AD_SAMPLING_RATE = MetaDatum("ad_sampling_rate", True, np.ndarray, Units.HERTZ)
    FREQUENCY_DOMAIN_FILTER = MetaDatum("frequency_domain_filter", False, str)
    FILTER_THRESHOLD = MetaDatum("filter_threshold", False, np.ndarray, Units.HERTZ)