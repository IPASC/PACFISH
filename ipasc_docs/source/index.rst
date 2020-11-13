.. IPASC Data Conversion Tool documentation master file, created by
   sphinx-quickstart on Sun Aug 30 15:41:38 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. include:: _documentation/welcome.rst

Build the documentation
=======================

Run `sphinx-build -b pdf docs/source docs` in the top level folder to build the pdf documentation.
The latest documentation will then be available under docs/ipasc_tool_documentation.pdf

.. include:: _static/coordinate_system.png

Class references
================

Module: api
-------------

.. automodule:: ipasc_tool.api
    :members:
.. automodule:: ipasc_tool.api.BaseAdapter
    :members:
.. automodule:: ipasc_tool.api.adapters
    :members:
.. automodule:: ipasc_tool.api.adapters.DKFZ_CAMI_Experimental_System_Nrrd_File_Converter
    :members:

Module: core
-------------

.. automodule:: ipasc_tool.core
    :members:
.. automodule:: ipasc_tool.core.DeviceMetaDataCreator
    :members:
.. automodule:: ipasc_tool.core.Metadata
    :members:
.. automodule:: ipasc_tool.core.PAData
    :members:

Module: iohandler
-------------

.. automodule:: ipasc_tool.iohandler
    :members:
.. automodule:: ipasc_tool.iohandler.file_reader
    :members:
.. automodule:: ipasc_tool.iohandler.file_writer
    :members:

Module: qualitycontrol
-------------

.. automodule:: ipasc_tool.qualitycontrol
    :members:
.. automodule:: ipasc_tool.qualitycontrol.CompletenessChecker
    :members:
.. automodule:: ipasc_tool.qualitycontrol.ConsistencyChecker
    :members:
.. automodule:: ipasc_tool.qualitycontrol.PADataIntegrityChecker
    :members:
