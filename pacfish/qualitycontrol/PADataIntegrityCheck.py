# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-FileCopyrightText: 2021 Janek Gröhl
# SPDX-FileCopyrightText: 2021 Lina Hacker
# SPDX-License-Identifier: BSD 3-Clause License

from pacfish import PAData
from pacfish.qualitycontrol import CompletenessChecker, ConsistencyChecker


def perform_pa_data_integrity_check(_pa_data: PAData, _verbose: bool = False) -> bool:
    """
    TODO
    :param _pa_data:
    :param _verbose:
    :return:
    """

    if _pa_data is None:
        raise ValueError("The data file must not be None!")

    if not isinstance(_pa_data, PAData):
        raise ValueError("The given data file must be of type PAData!")

    completeness_checker = CompletenessChecker(verbose=_verbose)
    consistency_checker = ConsistencyChecker(verbose=_verbose)

    is_complete_meta_acquisition = completeness_checker.check_meta_data(_pa_data.meta_data_acquisition)
    is_complete_meta_device = completeness_checker.check_meta_data(_pa_data.meta_data_device)

    is_consistent_binary = consistency_checker.check_binary(_pa_data.binary_time_series_data)
    is_consistent_meta_acquisition = consistency_checker.check_meta_data(_pa_data.meta_data_acquisition)
    is_consistent_meta_device = consistency_checker.check_meta_data(_pa_data.meta_data_device)

    return (is_complete_meta_acquisition and is_complete_meta_device and is_consistent_binary and
            is_consistent_meta_acquisition and is_consistent_meta_device)

def quality_check_pa_data(pa_data: PAData, verbose: bool = False, log_file_path: str = None) -> bool:
    completeness = CompletenessChecker(verbose=verbose, log_file_path=log_file_path)
    consistency = ConsistencyChecker(verbose=verbose, log_file_path=log_file_path)

    b1 = completeness.check_meta_data(pa_data.meta_data_acquisition)
    b2 = consistency.check_meta_data(pa_data.meta_data_acquisition)

    b3 = completeness.check_meta_data_device(pa_data.meta_data_device)
    b4 = consistency.check_meta_data_device(pa_data.meta_data_device)

    b5 = consistency.check_binary(pa_data.binary_time_series_data)

    return b1 and b2 and b3 and b4 and b5