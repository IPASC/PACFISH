import nrrd
import numpy as np


def create_nrrd_file(output_path_and_filename):
    data = np.random.random((128, 4096, 13))
    meta = dict([('type', 'double'),
                 ('dimension', 3),
                 ('space', 'left-posterior-superior'),
                 ('sizes', np.array([128, 4096, 13])),
                 ('space directions', np.array([[0.3, 0., 0.],
                                             [0., 0.0125, 0.],
                                             [0., 0., 1.]])),
                 ('kinds', ['domain', 'domain', 'domain']),
                 ('endian', 'little'),
                 ('encoding', 'gzip'),
                 ('space origin', np.array([0., 0., 0.]))])
    nrrd.write(output_path_and_filename, data=data, header=meta)
