"""
SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
SPDX-License-Identifier: BSD 3-Clause License
"""

from pacfish import PAData
from pacfish.qualitycontrol.CompletenessChecker import CompletenessChecker
from pacfish.qualitycontrol.ConsistencyChecker import ConsistencyChecker
from pacfish.qualitycontrol.PADataIntegrityCheck import perform_pa_data_integrity_check


def quality_check_pa_data(pa_data: PAData, verbose: bool = False, log_file_path: str = None) -> bool:
    completeness = CompletenessChecker(verbose=verbose, log_file_path=log_file_path)
    consistency = ConsistencyChecker(verbose=verbose, log_file_path=log_file_path)

    b1 = completeness.check_meta_data(pa_data.meta_data_acquisition)
    b2 = consistency.check_meta_data(pa_data.meta_data_acquisition)

    b3 = completeness.check_meta_data_device(pa_data.meta_data_device)
    b4 = consistency.check_meta_data_device(pa_data.meta_data_device)

    b5 = consistency.check_binary(pa_data.binary_time_series_data)

    return b1 and b2 and b3 and b4 and b5
