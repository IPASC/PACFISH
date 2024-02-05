"""
This package contains implementations of custom adapters that enable the conversion of
certain commonly used photoacoustic data formats into the IPASC format.

You can use these as a reference when attempting to define your own adapters.
"""

from .Nrrd_File_Converter import NrrdFileConverter
from .Imagio_File_Converter import ImagioFileConverter
