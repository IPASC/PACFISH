# PACFISH

[![Pypi Badge](https://img.shields.io/pypi/v/pacfish)](https://pypi.org/project/pacfish/)
[![Pypi Installs](https://img.shields.io/pypi/dw/pacfish?label=pypi%20installs)](https://pypistats.org/packages/pacfish)
[![License: BSD 3-Clause](https://img.shields.io/badge/license-BSD%203--Clause-blue)](https://github.com/IPASC/PACFISH/blob/main/LICENSES/BSD%203-Clause)

[![Documentation Status](https://readthedocs.org/projects/pacfish/badge/?version=latest)](https://pacfish.readthedocs.io/en/latest/)
![Testing Status](https://github.com/IPASC/PACFISH/actions/workflows/continuous-integration-testing.yml/badge.svg)
[![Code Coverage](https://codecov.io/gh/IPASC/PACFISH/branch/main/graph/badge.svg)](https://app.codecov.io/gh/IPASC/PACFISH)

<img src="https://github.com/IPASC/PACFISH/raw/main/docs/source/images/pacfish_logo.png" alt="PACFISH LOGO" width="350px">


In this repository we develop the photoacoustic converter for information sharing (PACFISH).
It is a tool that enables the conversion of vendor-specific
proprietary data formats into the IPASC data format,
which is an HDF5 container that has a defined 
structure for the meta data that are given with the binary data.
A list of meta data information was suggested by the International 
Photoacoustic Standardisation Consortium (IPASC) 
in early 2020. You can find this list using the following link:

https://www.ipasc.science/documents/20210916_IPASC_Format_V2.pdf

PACFISH serves three purposes: (1) it helps vendors to integrate the IPASC data format 
export into their standard software; (2) it assists scientists to read and write data in 
the consensus HDF5 format; and (3) it helps the PA community to create custom adapters 
that convert proprietary file formats into the consensus HDF5 format.

![API Workflows](https://github.com/IPASC/PACFISH/raw/main/docs/source/images/api_workflows.png)

Please help IPASC by reporting any missing parameters, bugs, or issues.
We are also looking forward to any contributions in form of adapters that 
can convert a priprietary format into the IPASC format.
If you are a member of the research community, a photoacoustic vendor, or
interested to contribute or in the project in general because of any other
reasons, please contact the leadership team of the Data Acquisition and
Management Theme of IPASC. 

These are currently: Janek Gröhl, Lina Hacker, and Ben Cox.

## Software Architecture

PACFISH is divided into the API, core, quality control, and iohandler modules.
The API package (_pacfish.api_ yellow module) can be used to facilitate the 
integration of conversion adapters to convert from arbitrary file formats 
into the IPASC data format. To create a conversion adapter, 
a Python representation of (1) the binary data, (2) the acquisition metadata 
dictionary, and (3) the device metadata dictionary need to be implemented.

![PACFISH Architecture](https://github.com/IPASC/PACFISH/raw/main/docs/source/images/pacfish_architecture.png)

The core classes (_pacfish.core_ green module) represent the metadata and 
data structure in Python. Each metadatum is described with specific device 
tags defining the name, data type, necessity and SI unit (if applicable), 
and setting a value constraint. Basic metadata constraints have been 
implemented to avoid accidental typos within the values field (e.g. only 
positive numbers larger than zero are applicable for acquisition wavelengths). 
If the value is not within the constraints a _TypeError_ is raised. 
Metadatum-specific functions enable easy addition of the values for the 
specific metadata field.

The quality control functionalities (_pacfish.qualitycontrol_ blue module) ensure 
the correctness of the conversion into the IPASC format: a _completeness checker_
tests that all metadata are being called and a _consistency checker_ ensures 
that all metadata are within their constraints. An automatically-generated 
output report gives a human-readable summary of the quality control checks and 
ensures that the likelihood of conversion mistakes are minimized. For control of 
the _Device Metadata_, the detector and illuminator positions can be represented 
in a 3D coordinate system as visual control.

Finally, the I/O functionality (_pacfish.iohandler_ red module) enables reading 
and writing of IPASC-formatted data files.

# Examples and use cases

Please look in the `examples` folder for
detailed and functional examples how to use the 
PACFISH API. We have examples for both `Python` and `MATLAB`.

## Use case: using the tool to read and write HDF5 files

    import pacfish as pf

    # Loading data from the hard drive
    pa_data = pf.load_data("path/to/hdf5file.hdf5")
    numpy_array = pa_data.binary_time_series_data

    # Writing of data to hard drive
    pf.write_data("path/to/new/file.hdf5", pa_data)

## Use case: Implement a conversion adapter

    impot pacfish as pf

    class DeviceSpecificAdapter(pf.BaseAdapter):

        def generate_binary_data(self) -> np.ndarray:
            # IMPLEMENTATION HERE
            pass

        def generate_device_meta_data(self) -> dict:
            # IMPLEMENTATION HERE
            pass

        def set_metadata_value(self, metadata_tag: MetaDatum) -> object:
            # IMPLEMENTATION HERE
            pass

