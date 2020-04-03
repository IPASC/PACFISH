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

from core import MetadataTags, MetaDatum


class CompletenessChecker:

    def __init__(self):
        self.save_file_name = "logfile.md"

    def check_meta_data(self, meta_data_dictionary: dict, verbose: bool = False,
                        log_file_path: str = None) -> bool:
        """
        This function will evaluate the completeness of the reported metadata.
        It can be used to generate a report to the console by setting `verbose`
        to True. When setting a file path to log_file, it will also save the
        report as a txt file in the designated path.

        :param meta_data_dictionary: A dictionary containing all PA image
        meta data.
        :param verbose: A flag to indicate whether the log should be printed
                        to the console.
        :param log_file_path: If given a string with the path to where the log
                              file should be written to.

        :return: True, if the meta_data_dictionary is complete

        :raises ValueError: if meta_data_dictionary was None
        :raises TypeError: if one of the arguments ws not of the correct type
        """

        # Input data validation
        if meta_data_dictionary is None:
            raise ValueError("the field meta_data_dictionary must not be None!")

        if not isinstance(meta_data_dictionary, dict):
            raise TypeError("The field meta_data_dictionary was not of " +
                            "type dict")

        # Creation of the completenes report
        incompletenes_count = 0

        log_string = "#Completeness Report\n\n"

        log_string += "##Individual fields\n\n"
        for metadatum in MetadataTags:
            meta_data_is_complete = True

            if metadatum not in meta_data_dictionary:
                log_string += "* missing entry \"" + metadatum.info.tag + "\"\n"
                log_string += "  * metadatum not found in dictionary\n\n"
                meta_data_is_complete = False
            elif meta_data_dictionary[metadatum] is None:
                log_string += "* missing entry \"" + metadatum.info.tag + "\"\n"
                log_string += "  * metadatum found in dictionary\n"
                log_string += "  * but the mapped field was None\n\n"
                meta_data_is_complete = False
            elif not isinstance(meta_data_dictionary[metadatum], metadatum.info.dtype):
                log_string += "* corrupt entry \"" + metadatum.info.tag + "\"\n"
                log_string += "  * metadatum found in dictionary\n"
                log_string += "  * and the mapped field was not None\n"
                log_string += ("  * but the mapped field was not of type " +
                               str(metadatum.info.dtype) + "\n\n")
                meta_data_is_complete = False

            if not meta_data_is_complete:
                incompletenes_count += 1

        log_string += "## Result\n\n"

        log_string += (str(incompletenes_count) + " metadata fields were "
                       "found to be incomplete or missing.\n\n")

        if incompletenes_count > 0:
            log_string += "The metadata dictionary is incomplete\n"
        else:
            log_string += "The metadata dictionary is complete\n"

        # Reporting of the results
        if verbose:
            print(log_string)

        if log_file_path is not None:
            with open(log_file_path + self.save_file_name, "w") as log_file_handle:
                log_file_handle.writelines(log_string)

        return incompletenes_count == 0

    def check_meta_data_device(self, device_meta_data: dict):
        # TODO
        pass
