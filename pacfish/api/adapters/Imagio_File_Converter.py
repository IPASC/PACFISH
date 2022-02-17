import numpy as np

from pacfish import BaseAdapter, MetaDatum
from pacfish import MetadataAcquisitionTags
from pacfish import DeviceMetaDataCreator, DetectionElementCreator, IlluminationElementCreator

class NrrdFileConverter(BaseAdapter):
    """
    For the Seno Imagio system.
    """

    def __init__(self):
        pass

    def generate_binary_data(self) -> np.ndarray:
        pass

    def generate_device_meta_data(self) -> dict:
        pass

    def set_metadata_value(self, metadatum: MetaDatum) -> object:
        pass

