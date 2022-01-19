"""
SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
SPDX-License-Identifier: CC0
"""

import numpy as np
import pacfish as pf

device_metadata_creator = pf.DeviceMetaDataCreator()

illumination_element_creator = pf.IlluminationElementCreator()
illumination_element_creator.set_pulse_width(12.5)
illumination_element_creator.set_beam_divergence_angles(0.5)
illuminator = illumination_element_creator.get_dictionary()

device_metadata_creator.add_illumination_element(illuminator)


detection_element_creator = pf.DetectionElementCreator()
detection_element_creator.set_detector_position(np.asarray([0.3, 0.5, 0.2]))
detection_element_creator.set_detector_orientation(np.asarray([0.1, 0.1, 0.1]))
detector = detection_element_creator.get_dictionary()

device_metadata_creator.add_detection_element(detector)

result_dictionary = device_metadata_creator.finalize_device_meta_data()

completeness_checker = pf.CompletenessChecker(verbose=True)

completeness_checker.check_device_meta_data(result_dictionary)
