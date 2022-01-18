# Code adapted from the SIMPA repository:
# Original license:
# SPDX-FileCopyrightText: 2021 Computer Assisted Medical Interventions Group, DKFZ
# SPDX-License-Identifier: MIT

import os
import glob

current_dir = os.path.dirname(os.path.realpath(__file__))
if current_dir[-6:] == "source":
    folder_level = "../"
else:
    folder_level = ""
rst_files = glob.glob(os.path.join(current_dir, "pacfish*.rst"))


for rst_file in rst_files:
    new_lines = list()
    file = open(rst_file, "r")
    lines = file.readlines()
    lines_iterator = iter(lines)
    for line in lines_iterator:
        if line == 'Submodules\n':
            next(lines_iterator, None)
            next(lines_iterator, None)
            next(lines_iterator, None)
        elif line == 'Subpackages\n':
            next(lines_iterator, None)
            next(lines_iterator, None)
        elif " package" in line:
            new_line = line.replace(" package", "")
            modules = new_line.split(".")
            new_lines.append(modules[-1])
        else:
            new_lines.append(line)
    file.close()
    file = open(rst_file, "w")
    file.writelines(new_lines)
    file.close()
