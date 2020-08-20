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

from ipasc_tool import PAData
from ipasc_tool.qualitycontrol.CompletenessChecker import CompletenessChecker
from ipasc_tool.qualitycontrol.ConsistencyChecker import ConsistencyChecker
from ipasc_tool.qualitycontrol.PADataIntegrityCheck import perform_pa_data_integrity_check


def quality_check_pa_data(pa_data: PAData, verbose: bool = False, log_file_path: str = None) -> bool:
    completeness = CompletenessChecker(verbose=verbose, log_file_path=log_file_path)
    consistency = ConsistencyChecker(verbose=verbose, log_file_path=log_file_path)

    b1 = completeness.check_meta_data(pa_data.meta_data_acquisition)
    b2 = consistency.check_meta_data(pa_data.meta_data_acquisition)

    b3 = completeness.check_meta_data_device(pa_data.meta_data_device)
    b4 = consistency.check_meta_data_device(pa_data.meta_data_device)

    b5 = consistency.check_binary(pa_data.binary_time_series_data)

    return b1 and b2 and b3 and b4 and b5
