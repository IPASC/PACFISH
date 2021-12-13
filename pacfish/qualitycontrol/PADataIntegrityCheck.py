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
