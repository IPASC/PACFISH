# Example IPASC data

This repository contains supplementary data for the paper __"The IPASC data format: A consensus data format for photoacoustic imaging"__ 
which presents a consensus-based data format proposal for photoacoustic imaging.
(Please refer to the __Photoacoustic Data and Device Parameters__ consensus 
document on the [IPASC website](https://www.ipasc.science/publications/) for further details).


Four example time series data sets are given in the IPASC format.
The data was obtained synthetically with [k-Wave](www.k-wave.org) simulations.
The script for generating the simulations of the linear-detection array is 
included in `kwave_2Dsim_linear.m`.
In addition to the metadata derived from the k-Wave simulation,
all remaining metadata fields are filled with mock data, 
giving an overview on parameter structure and naming conventions.
The same initial pressure is assumed for each simulation, 
but the data is measured with different detection geometries containing 
50 detection elements:

- Linear Array [`sample_ipasc_kwave_2Dsim_linear_array.hdf5`]
- Semicircular array (180°) [`sample_ipasc_kwave_2Dsim_semicircular_array.hdf5`]
- Circular array (360°) [`sample_ipasc_kwave_2Dsim_circular_array.hdf5`]
- Random array [`sample_ipasc_kwave_2Dsim_random_array.hdf5`]

The image located in `overview.png` shows visualisations of these detection geometries, 
the simulated time series data, as well as respective reconstructions using back projection.

![Example images](overview.png)

The data is openly available under the CC-BY-4.0 license.