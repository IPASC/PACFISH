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

from pacfish import DeviceMetaDataCreator
from pacfish import DetectionElementCreator
from pacfish import IlluminationElementCreator
from pacfish import CompletenessChecker


device_metadata_creator = DeviceMetaDataCreator()

illumination_element_creator = IlluminationElementCreator()
illumination_element_creator.set_pulse_width(12.5)
illumination_element_creator.set_beam_divergence_angles(0.5)
illuminator = illumination_element_creator.get_dictionary()

device_metadata_creator.add_illumination_element(illuminator)


detection_element_creator = DetectionElementCreator()
detection_element_creator.set_detector_position(np.asarray([0.3, 0.5, 0.2]))
detection_element_creator.set_detector_orientation(np.asarray([0.1, 0.1, 0.1]))
detector = detection_element_creator.get_dictionary()

device_metadata_creator.add_detection_element(detector)

result_dictionary = device_metadata_creator.finalize_device_meta_data()

completeness_checker = CompletenessChecker(verbose=True)

completeness_checker.check_meta_data_device(result_dictionary)
