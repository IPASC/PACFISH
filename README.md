# README

[![Pypi Badge](https://img.shields.io/pypi/v/pacfish)](https://pypi.org/project/pacfish/)
[![Pypi Installs](https://img.shields.io/pypi/dw/pacfish?label=pypi%20installs)](https://pypistats.org/packages/pacfish)
[![License: BSD 3-Clause](https://img.shields.io/badge/license-BSD%203--Clause-blue)](https://github.com/IPASC/PACFISH/blob/main/LICENSES/BSD%203-Clause)

[![Documentation Status](https://readthedocs.org/projects/pacfish/badge/?version=latest)](https://pacfish.readthedocs.io/en/latest/)
![Testing Status](https://github.com/IPASC/PACFISH/actions/workflows/continuous-integration-testing.yml/badge.svg)
[![Code Coverage](https://codecov.io/gh/IPASC/PACFISH/branch/main/graph/badge.svg)](https://app.codecov.io/gh/IPASC/PACFISH)

In this repository we develop the photoacoustic converter for information sharing (PACFISH).
It is a tool that enables the conversion of vendor-specific
proprietary data formats into the IPASC data format,
 which is an HDF5 container that has a defined 
structure for the meta data that are given with the binary data.
A list of meta data information was suggested by the International 
Photoacoustic Standardisation Consortium (IPASC) 
in early 2020. You can find this list using the following link:

https://www.ipasc.science/documents/20210916_IPASC_Format_V2.pdf

Please help IPASC by reporting any missing parameters, bugs, or issues.
We are also looking forward to any contributions in form of adapters that 
can convert a priprietary format into the IPASC format.
If you are a member of the research community, a photoacoustic vendor, or
interested to contribute or in the project in general because of any other
reasons, please contact the leadership team of the Data Acquisition and
Management Theme of IPASC. 

These are currently: Janek Gröhl, Lina Hacker, and Ben Cox.

# Examples and use cases

Please look in the `ipasc_examples` folder for
detailed and functional examples how to use the 
PACFISH API.

## Use case: using the tool to read and write HDF5 files

    from IPASC_DataConversionTool import iohandler as io

    # Loading data from the hard drive
    pa_data = io.load_data("path/to/hdf5file.hdf5")
    numpy_array = pa_data.binary_time_series_data

    # Writing of data to hard drive
    io.write_data("path/to/new/file.hdf5", pa_data)

## Use case: Implement a conversion adapter

    from IPASC_DataConversionTool.api import BaseAdapter

    class DeviceSpecificAdapter(BaseAdapter):

        def generate_binary_data(self) -> np.ndarray:
            # IMPLEMENTATION HERE
            pass

        def generate_device_meta_data(self) -> dict:
            # IMPLEMENTATION HERE
            pass

        def set_metadata_value(self, metadata_tag: MetaDatum) -> object:
            # IMPLEMENTATION HERE
            pass
