import numpy as np
import pacfish as pf
from testing.unit_tests.utils import create_complete_device_metadata_dictionary, \
    create_complete_acquisition_meta_data_dictionary, assert_equal_dicts

device_dict = create_complete_device_metadata_dictionary()
acquisition_dict = create_complete_acquisition_meta_data_dictionary()

pa_data = pf.PAData(binary_time_series_data=np.random.random([4, 100, 2]),
                    meta_data_acquisition=acquisition_dict,
                    meta_data_device=device_dict)

pf.write_data("ipasc_compatible_V1.hdf5", pa_data)
