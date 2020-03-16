# DataConversionTool

Dear photoacoustic community,

in this github repository we are currently starting to develop a tool that enables the conversion of vendor-specific
proprietary data formats into a standard format that has a defined structure for the meta data that are given with
the binary data.
A list of meta data information was suggested by the International Photoacoustic Standardisation Consortium (IPASC) 
in early 2020. You can find this list using the following link:

https://www.ipasc.science/documents/20200121_Metadata_list.pdf

Please help IPASC by reporting any missing parameters.

Many thanks,

The IPASC members

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

        def generate_meta_data_device(self) -> dict:
            # IMPLEMENTATION HERE
            pass

        def set_metadata_value(self, metadata_tag: MetaDatum) -> object:
            # IMPLEMENTATION HERE
            pass
