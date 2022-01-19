# Possible Metadata Attributes

Each metadatum is characterised by a series of attributes to describe and define its use and boundary conditions.  
If necessary, further specifications by nested attributes can be given. All units of the metadata are stated in the {International System of Units} (SI units) unless otherwise specified.

## Condition
Constraints of an attribute that limit its value range  (e.g. the acquisition wavelengths must the of the same size as the acquired measurements)
## Description
A short description of the attribute.
## dtype
Data type of the attribute.
## Measurement Device Attribute
A specific type of nested attribute that describes measurement device details if required. Measurement device attributes are always optional. They include:
### Calibration Date
A timestamp referring to the date when the measurement device was last calibrated. Timestamps are given in seconds with the elapsed time since epoch (Jan 1st 1970, 00:00).
### Measurement Device Manufacturer
A string literal describing the manufacturer of the measurement device, e.g. ‘Thorlabs’.
### Measurement Device Serial Number
A string literal comprising the serial number of the measurement device.
### Measurement Device Type
A string literal describing the measurement device for this attribute, e.g. ‘pyroelectric sensor’ or ‘wavemeter’.
## Method Name
The name of the function/method that can be called in any programming language to obtain information on a specific attribute.
## Necessity
 ‘Minimal’ or ‘Report if present’ condition for the metadatum. Minimal parameters are all parameters that are required to reconstruct an image from the raw time series data. Any additional information should be reported in the metadata if available.
## Nested Attribute
A sub-attribute that further describes an attribute.
## Units
SI units of the attribute if applicable.

---

# Binary Data Metadata

The binary data are formatted as: [detectors, samples, wavelengths, measurements]. Depending on the binary data metadata, the size of these arrays varies.  The interpretation of the measurement field depends on the dimensionality field.

## Data Type

The Data Type field represents the datatype of the binary data. This field is given in the C++ data type naming convention, e.g. ‘short’, ‘unsigned short’, ‘int’, ‘unsigned int’, ‘long’, ‘unsigned long’, ‘long long’, ‘float’, ‘double’, ‘long double’.

|   |   |
|---|---|
|__Necessity__| Minimal |
|__dtype__| String |
|__Method Name__| get_data_type() |

## Dimensionality

The Dimensionality field represents the definition of the ‘measurement’ field and can be either [‘time’, ‘space’, or ‘time and space’]. 

|   |   |
|---|---|
|__Necessity__| Minimal |
|__dtype__| String |
|__Method Name__| get_dimensionality() |

## Sizes

The Sizes field quantifies the number of data points in each of the dimensions specified in the dimensionality field. As such, it defines the respective sizes of each element of the binary data which are: [detectors, samples, wavelengths, measurements].

|   |   |
|---|---|
|__Necessity__| Minimal |
|__dtype__| Integer array |
|__Units__| Dimensionless Quantity (the units can be inferred in combination with Dimensionality and the detection and illumination geometry).
|__Method Name__| get_sizes() |

---

# File Container Format
The container format metadata refer to the inherent features of the file format which specify the organisation ofhow the different elements of metadata are combined in a computer file.

## Encoding

The Encoding field defines the character set that was used to encode the binary data and the metadata, e.g. one of ‘UTF-8’, ‘ASCII’, ‘CP-1252’ etc.

|   |   |
|---|---|
|__Necessity__| Minimal |
|__dtype__| String |
|__Method Name__| get_encoding() |

## Compression

The Compression field defines the compression method that was used to compress the binary data, e.g. one of ‘raw’, ‘gzip etc.

|   |   |
|---|---|
|__Necessity__| Minimal |
|__dtype__| String |
|__Method Name__| get_compression() |

## Universally Unique Identifier

The Universally Unique Identifier (UUID) field is a unique identifier of the data that can be referenced.

|   |   |
|---|---|
|__Necessity__| Minimal |
|__dtype__| String |
|__Condition__| 128-bit Integer displayed as a hexadecimal string in 5 groups separated by hyphens, in the form 8-4-4-4-12 for a total of 36 characters. The UUID is randomly generated using the UUID version 4 standard. |
|__Method Name__| get_data_UUID() |

---

# Acquisition Metadata

## A/D (Analog/Digital) Sampling Rate

The A/D Sampling Rate field refers to the rate at which samples of the analogue signal are taken to be converted into digital form.

|   |   |
|---|---|
|__Necessity__| Minimal |
|__dtype__| Double |
|__Units__| Hertz [Hz] (samples / second) |
|__Method Name__| get_sampling_rate() |

## Acoustic Coupling Agent

The Acoustic Coupling Agent field is a string representation of the acoustic coupling agent that is used, e.g.  D2O, H2O, gel, etc.

|   |   |
|---|---|
|__Necessity__| Report if present |
|__dtype__| String |
|__Method Name__| get_coupling_agent() |

## Acquisition Optical Wavelengths

The Acquisition Optical Wavelengths field is an array of all wavelengths used for image acquisition.

|   |   |
|---|---|
|__Necessity__| Minimal |
|__dtype__| Array |
|__Units__| Meters [m] |
|__Method Name__| get_wavelengths() |

## Element-dependent Gain 

The Element-dependent Gain field is a 2D array that contains the relative factors which are used for apodization or detection element-wise sensitivity corrections.

|   |   |
|---|---|
|__Necessity__| Report if present |
|__dtype__| Double array [num_detectors] |
|__Units__| Dimensionless unit |
|__Condition__| The element-dependent gain is a double array that has the same dimension as the number of detectors. |
|__Method Name__| get_element_dependent_gain() |

## Frequency Domain Filter

The Frequency Domain Filter field specifies an array defining the frequency threshold levels that are applied to filter the raw time series data, containing [lower, higher] -3 dB points of the filter in Hertz. [lower, -1] denotes a high-pass filter and [-1, higher] denotes a low-pass filter.

|   |   |
|---|---|
|__Necessity__| Report if present |
|__dtype__| Double array |
|__Units__| Hertz [Hz] (samples / second) |
|__Method Name__| get_frequency_filter() |

## Measurements Per Image

The Measurements Per Image field specifies a single value describing the number of measurements that constitute the dataset corresponding to one image

|   |   |
|---|---|
|__Necessity__| Report if present |
|__dtype__| Integer |
|__Units__| Dimensionless unit|
|__Method Name__| get_measurements_per_image() |

## Measurement Spatial Pose

The Measurement Spatial Pose field specifies coordinates describing the position and orientation changes of the acquisition system relative to the measurement of reference (first measurement). The entire coordinate system is moved based on the spatial positions. If the frame stays constant, N equals 0.

|   |   |
|---|---|
|__Necessity__| Report if present |
|__dtype__| 2D double array of 6D coordinates (N, 6) |
|__Units__| Meters [m] |
|__Condition__| Array size must be the same as the size of ‘measurements’ specified in the sizes field. | 
|__Method Name__| get_measurement_spatial_pose() |

## Measurement Timestamps

The Measurement Timestamps field specifies the time at which a measurement was recorded.

|   |   |
|---|---|
|__Necessity__| Report if present |
|__dtype__| Double array |
|__Units__| Seconds [s] |
|__Condition__| Array size must be the same as the size of ‘measurements’ specified in the sizes field. Timestamps are given in seconds with the elapsed time since epoch (Jan 1st 1970, 00:00). | 
|__Method Name__| get_time_stamps() |

## Overall Gain 

The Overall Gain field is a single value describing a factor used to modify the amplitude of the raw time series data.

|   |   |
|---|---|
|__Necessity__| Report if present |
|__dtype__| Double |
|__Units__| Dimensionless unit |
|__Method Name__| get_overall_gain() |

## Photoacoustic Imaging Device Reference

The Photoacoustic Imaging Device Reference field specifies a reference to the UUID of the PA imaging device description as defined in part 1. This field will be used for future versions of the data format, where the device metadata may not be stored within the file but will be accessible via a web service.

|   |   |
|---|---|
|__Necessity__| Report if present |
|__dtype__| String |
|__Method Name__| get_device_reference() |

## Pulse Laser Energy

The Pulse Laser Energy field specifies the pulse energy used to generate the PA signal. If the pulse energies are averaged over many pulses, the average value must be specified. If the pulse laser energy has already been accounted for, the array must read [0].

|   |   |
|---|---|
|__Necessity__| Report if present |
|__dtype__| Double array |
|__Units__| Joule [J] |
|__Condition__| Array size must be the same as the size of ‘measurements’’ specified in the sizes field, except for the case of [0]. It can also be of shape [detection_elements, measurements] in case that laser pulses are fired individually for each detection element. 
|__Method Name__| get_pulse_laser_energy() |

## Regions of Interest

The Regions of Interest field specifies a list of named regions within the underlying 3D Cartesian coordinate system (cf. Device Metadata). Strings containing the region names are mapped to arrays that define either an approximate cuboid area (cf. Field of View) or a list of coordinates describing a set of 3D Cartesian coordinates surrounding the named region. This field aims to facilitate the delineation of, e.g. distinct tissue types, potential lesions or phantom components. Regions of Interest are defined independently from the Field of View, and could be also outside the Field of View.

|   |   |
|---|---|
|__Necessity__| Report if present |
|__dtype__| Dictionary [String, 2D double array (6, 3)] where the first number in the array represents the number of coordinates and the second number represents the coordinate values. |
|__Units__| Meter [m] |
|__Method Name__| get_region_of_interest() |

## Scanning Method

The Scanning Method field is a string representation of the scanning method that was used. The following descriptions can be used: (“composite_scan”, “full_scan”). This flag determines the way the metadatum “measurement” is defined. 

|   |   |
|---|---|
|__Necessity__| Report if present |
|__dtype__| String |
|__Method Name__| get_scanning_method() |

## Speed of Sound

The Speed of Sound field specifies either a single value representing the mean global speed of sound in the entire imaged medium or a 3D array representing a heterogeneous speed of sound map in the device coordinate system. This definition covers both the imaged medium and the coupling agent.

|   |   |
|---|---|
|__Necessity__| Report if present |
|__dtype__| Double or double array |
|__Units__| Meters per second [m/s] |
|__Method Name__| get_speed_of_sound() |

## Temperature Control

The Temperature Control field specifies the temperature of the imaged space (covering both the imaged medium and the coupling agent) for each measurement.

|   |   |
|---|---|
|__Necessity__| Report if present |
|__dtype__| Double array |
|__Units__| Kelvin [K] |
|__Condition__| The temperature control array either has the same dimension as the number of ‘measurements’, or is a single value indicating a constant temperature over all measurements. |
|__Method Name__| get_temperature() |

## Time Gain Compensation

The Time Gain Compensation field is a 1D array that contains relative factors which are used to correct the time series data for the effect of acoustic attenuation. 

|   |   |
|---|---|
|__Necessity__| Report if present |
|__dtype__| Double array |
|__Units__| Dimensionless unit |
|__Condition__| The time gain compensation array has the same dimension as the samples dimension [samples].   It can also be of shape [detection_elements, samples] if measurements are acquired individually for each detection element. |
|__Method Name__| get_time_gain_compensation() |

---

# Device Metadata

The device metadata is split into three categories: Some general metadata parameters,
metadata information on the detection geometry, and metadata information on the illumination geometry.

## General Parameters

### Field of View

The Field of View field defines an approximate cuboid (3D) area detectable by the PA imaging device in 3D cartesian coordinates [x1start, x1end, x2start, x2end, x3start, x3end].  A 2D Field of View can be defined by setting the start and end coordinate of the respective dimension to the same value.

|   |   |
|---|---|
|__Necessity__| Minimal |
|__dtype__| 2D double array of length 6 |
|__Units__| Meter [m]|
|__Method Name__| get_field_of_view() |

### Number of Detection Elements

The Number of Detection Elements field quantifies the number of transducer elements used for detection in the PA imaging device. Each of these transducer elements is described by a set of detection geometry parameters.

|   |   |
|---|---|
|__Necessity__| Minimal |
|__dtype__| Integer |
|__Units__| Dimensionless unit |
|__Method Name__| get_number_of_detection_elements() |

### Number of Illumination Elements

The Number of Illumination Elements field quantifies the number of illuminators that are used in the PA imaging device. Each of these illuminators is described by a set of illumination geometry parameters.

|   |   |
|---|---|
|__Necessity__| Report if present  |
|__dtype__| Integer |
|__Units__| Dimensionless unit |
|__Method Name__| get_number_of_illumination_elements() |

### Universally Unique Identifier

The Universally Unique Identifier (UUID) for the device that can be referenced.

|   |   |
|---|---|
|__Necessity__| Minimal  |
|__dtype__| String |
|__Condition__| 128-bit Integer displayed as a hexadecimal string in 5 groups separated by hyphens, in the form 8-4-4-4-12 for a total of 36 characters. The UUID is randomly generated using the UUID version 4 standard. |
|__Method Name__| get_device_uuid() |


## Detection Element

### Detector Geometry

The Detector Geometry field defines the shape of the detector elements. The data type and the contents of the shape field are determined by the Detector Geometry Type field. The given coordinates are interpreted relative to the Detector Position.

|   |   |
|---|---|
|__Necessity__| Report if present  |
|__dtype__| Double, double array, or byte array |
|__Units__| Meter [m] |
|__Method Name__| get_detector_geometry() |

### Detector Geometry Type

The Detector Geometry Type field defines the interpretation of the data in the detector geometry field.
The following geometry types are currently supported:
- “CIRCULAR” - defined by a single value that determines the radius of the circle
- “SPHERE” - defined by a single value that determines the radius of the sphere
- “CUBOID” - defined by three values that determine the extent of the cuboid in x1, x2, and x3 dimensions before the position and orientation transforms.
- “MESH” - defined by an STL-formatted string that determines the positions of points and faces before the position and orientation transforms.

|   |   |
|---|---|
|__Necessity__| Report if present  |
|__dtype__| String |
|__Method Name__| get_detector_geometry_type() |

### Detector Orientation

The Detector Orientation field defines the direction unit vector of the detector in 3D Cartesian coordinates [xd, yd, zd] .

|   |   |
|---|---|
|__Necessity__| Report if present  |
|__dtype__| Double array |
|__Units__| Meter [m] |
|__Method Name__| get_detector_orientation() |

### Detector Position

The DetectorPosition field defines the position of the detection element centroid in 3D Cartesian coordinates [x1, x2, x3] .

|   |   |
|---|---|
|__Necessity__| Minimal  |
|__dtype__| Double array |
|__Units__| Meter [m] |
|__Method Name__| get_detector_position() |


### Detection Element Properties

#### Angular Response

The Angular Response field characterises the angular sensitivity of the detection element to the incident angle (relative to the element’s orientation) of the incoming pressure wave. If only one value (the angle [a]) is given, the value can be interpreted as a=limiting angle (where the response drops to -6 dB).

|   |   |
|---|---|
|__Necessity__| Report if present  |
|__dtype__| Array with two components, where the first component is the incident angle in radians and the second component is the normalised response value. |
|__Units__| Radians [rad], Normalised Units (to the maximum efficiency) |
|__Method Name__| get_angular_response() |

#### Frequency Response

The Frequency Response field describes a function of frequency that characterises the response of the detection element with respect to the frequency of incident pressure waves. If the response is only sparsely defined, the  values can be linearly interpolated between the closest neighbours. If the value is of shape [c, b], it can  be interpreted as c=centre frequency and b=bandwidth (measured at -6 dB).

|   |   |
|---|---|
|__Necessity__| Report if present  |
|__dtype__| Array with two components, where the first component is the frequency (in Hertz [s-1]) and the second component is the response value (in normalised units). |
|__Units__| Hertz [s-1], normalised units (to the maximum intensity) |
|__Method Name__| get_frequency_response() |

## Illumination Element

### Illuminator Geometry

The Illuminator Geometry field defines the numerical geometry of the optical fibre (bundle) output. The data type and content of this metadatum are determined by the illuminator geometry type field. The given coordinates  are interpreted relative to the illuminator position.

|   |   |
|---|---|
|__Necessity__| Report if present  |
|__dtype__| Double, double array, or byte array |
|__Units__| Meter [m] |
|__Method Name__| get_illuminator_geometry() |

### Illuminator Geometry Type

The Illuminator Geometry Type field defines the shape of the optical fibre (bundle) output. It determines the interpretation of the data in the illuminator geometry field. The following geometry types are currently supported:
- “CIRCULAR” - defined by a single value that determines the radius of the circle.
- “SPHERE” - defined by a single value that determines the radius of the sphere.
- “CUBOID” - defined by three values that determine the extent of the cuboid in x1, x2, and x3 dimensions before the position and orientation transforms.
- “MESH” - defined by an STL-formatted string that determines the positions of points and faces before the position and orientation transforms.

|   |   |
|---|---|
|__Necessity__| Report if present  |
|__dtype__| String |
|__Method Name__| get_illuminator_geometry_type() |

### Illuminator Orientation

The Illuminator Orientation field defines the direction unit vector of the illuminator in 3D Cartesian coordinates [x1d, x2d, x3d] . This unit vector is the normal of the planar illuminator surface.

|   |   |
|---|---|
|__Necessity__| Report if present  |
|__dtype__| 1D double array |
|__Units__| Meter [m] |
|__Method Name__| get_illuminator_orientation() |

### Illuminator Position

The Illuminator Position field defines the position of the illuminator centroid in 3D cartesian coordinates [x1, x2, x3] .

|   |   |
|---|---|
|__Necessity__| Report if present  |
|__dtype__| 1D double array |
|__Units__| Meter [m] |
|__Method Name__| get_illuminator_position() |

### Illuminator Properties

#### Beam Divergence Angles

The Beam Divergence Angles field represents the opening angles of the laser beam from the illuminator shape with respect to the orientation vector. This angle is represented by the standard deviation of the beam divergence.

|   |   |
|---|---|
|__Necessity__| Report if present  |
|__dtype__| Double |
|__Units__| Radians [rad] |
|__Method Name__| get_beam_divergence() |

#### Beam Intensity Profile

The Beam Intensity Profile field is a function of a spatial position that specifies the relative laser beam intensity according to the planar emitting surface of the illuminator shape at the distance defined in intensity profile distance. For points between specified positions, it is assumed that the values are linearly interpolated from their closest neighbours. The positions are generally in 2D.

|   |   |
|---|---|
|__Necessity__| Report if present  |
|__dtype__| Array of two double arrays [positions, intensities] with intensities and their corresponding positions. |
|__Units__| Normalised units (to the maximum intensity) |
|__Method Name__| get_beam_profile() |

#### Intensity Profile Distance

The Intensity Profile Distance field describes the distance from the light source for measuring its beam intensity profile. This distance is to be measured from the Illuminator Position along with the Illuminator Orientation. 

|   |   |
|---|---|
|__Necessity__| Report if present  |
|__dtype__| Double |
|__Units__| Meters [m] |
|__Method Name__| get_beam_profile_distance() |

#### Laser Energy Profile

The Laser Energy Profile field is a discretized function of the wavelength (nm)  describing the laser energy of the illuminator. Thereby, systematic differences in multispectral image acquisitions can be accounted for.

|   |   |
|---|---|
|__Necessity__| Report if present  |
|__dtype__| Array of two 1D double arrays [wavelengths, energies], where the first array comprises the wavelengths and the second array comprises the laser energies. |
|__Units__| Joule [J] |
|__Condition__| The laser energy profile function is well defined and non-negative in the wavelength range. |
|__Method Name__| get_energy_profile() |

#### Laser Stability Profile

The Laser Stability Profile field is a function of the wavelength (nm) and represents the standard deviation of the pulse-to-pulse laser energy of the illuminator.

|   |   |
|---|---|
|__Necessity__| Report if present  |
|__dtype__| Array of two 1D double arrays [wavelengths, energies], where the first array comprises the wavelengths and the second array comprises the laser energies. |
|__Units__| Joule [J] |
|__Condition__| The laser stability profile function is well defined and non-negative in the wavelength range. |
|__Method Name__| get_stability_profile() |

#### Pulse Duration / Width

The Pulse Duration /Width field describes the total length of a laser pulse measured as the time interval between the half-power points on the leading and trailing edges of the pulse.

|   |   |
|---|---|
|__Necessity__| Report if present  |
|__dtype__| Double |
|__Units__| Seconds [s]|
|__Method Name__| get_pulse_width() |

#### Wavelength Range

The Wavelength Range field quantifies the wavelengths  that can be generated by the illuminator. Three values can be reported: the minimum wavelength max, the maximum wavelength  max and a metric for the accuracy accuracy: (min, max, accuracy). These parameters could be for instance (700, 900, 1.2), meaning that this illuminator can be tuned from 700 nm to 900 nm with an accuracy of 1.2 nm. Single-wavelength elements are specified as: (actual, actual, accuracy).

|   |   |
|---|---|
|__Necessity__| Report if present  |
|__dtype__| 1D double array |
|__Units__| Meters [m] |
|__Method Name__| get_wavelength_range() |
