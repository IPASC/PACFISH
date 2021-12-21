# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-FileCopyrightText: 2021 Janek Gröhl
# SPDX-FileCopyrightText: 2021 Lina Hacker
# SPDX-License-Identifier: BSD 3-Clause License

from pacfish import PAData
from pacfish.qualitycontrol import CompletenessChecker, ConsistencyChecker


def quality_check_pa_data(pa_data: PAData, verbose: bool = False, log_file_path: str = None) -> bool:
    """
    This is a convenience method that instantiates both a completeness and a consistency checker
    and evaluates the given PAData instance.

    Parameters
    ----------
    pa_data: PAData
        The PAData instance to check
    verbose: bool
        Specifies if the log report should be printed to the console
    log_file_path: str
        A path to a log file to write to

    Return
    ------
    bool
        True if and only if all completeness and quality checks are passed.
    """
    completeness = CompletenessChecker(verbose=verbose, log_file_path=log_file_path)
    consistency = ConsistencyChecker(verbose=verbose, log_file_path=log_file_path)

    b1 = completeness.check_acquisition_meta_data(pa_data.meta_data_acquisition)
    b2 = consistency.check_acquisition_meta_data(pa_data.meta_data_acquisition)

    b3 = completeness.check_device_meta_data(pa_data.meta_data_device)
    b4 = consistency.check_device_meta_data(pa_data.meta_data_device)

    b5 = consistency.check_binary_data(pa_data.binary_time_series_data)

    return b1 and b2 and b3 and b4 and b5