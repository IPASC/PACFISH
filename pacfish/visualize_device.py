# SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
# SPDX-FileCopyrightText: 2021 Janek Gröhl
# SPDX-License-Identifier: BSD 3-Clause License

import matplotlib.pylab as plt
from matplotlib.patches import Rectangle, Circle, Polygon
import numpy as np
from pacfish import MetadataDeviceTags


def visualize_device(device_dictionary: dict, save_path: str = None, title: str = None):
    """
    Visualises a given device from the device_dictionary.

    Parameters
    ----------
    device_dictionary: dict
        The dictionary containing the device description.
    save_path: str
        Optional save_path to save a PNG file of the visualisation to.
    title: str
        Optional custom title for the plot.
    """

    def define_boundary_values(_device_dictionary: dict):
        mins = np.ones(3) * 100000
        maxs = np.ones(3) * -100000

        if "illuminators" in _device_dictionary:
            for illuminator in _device_dictionary["illuminators"]:
                position = _device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_POSITION.tag]
                for i in range(3):
                    if position[i] < mins[i]:
                        mins[i] = position[i]
                    if position[i] > maxs[i]:
                        maxs[i] = position[i]

        for detector in _device_dictionary["detectors"]:
            position = _device_dictionary["detectors"][detector][MetadataDeviceTags.DETECTOR_POSITION.tag]
            for i in range(3):
                if position[i] < mins[i]:
                    mins[i] = position[i]
                if position[i] > maxs[i]:
                    maxs[i] = position[i]

        fov = _device_dictionary["general"][MetadataDeviceTags.FIELD_OF_VIEW.tag]
        for i in range(3):
            if fov[2 * i] < mins[i]:
                mins[i] = fov[2 * i]
            if fov[2 * i + 1] < mins[i]:
                mins[i] = fov[2 * i + 1]
            if fov[2 * i] > maxs[i]:
                maxs[i] = fov[2 * i]
            if fov[2 * i + 1] > maxs[i]:
                maxs[i] = fov[2 * i + 1]

        MARGIN = 0.001
        maxs += MARGIN
        mins -= MARGIN
        return mins, maxs

    def add_arbitrary_plane(_device_dictionary: dict, _mins, _maxs, _axes, _draw_axis):
        _draw_axis.set_xlim(_mins[_axes[0]], _maxs[_axes[0]])
        _draw_axis.set_ylim(_maxs[_axes[1]], _mins[_axes[1]])
        _draw_axis.set_title(f"axes {_axes[0]}/{_axes[1]} projection view")
        _draw_axis.set_xlabel(f"{_axes[0]}-axis [m]")
        _draw_axis.set_ylabel(f"{_axes[1]}-axis [m]")

        fov = _device_dictionary["general"][MetadataDeviceTags.FIELD_OF_VIEW.tag]

        for detector in _device_dictionary["detectors"]:
            if not (MetadataDeviceTags.DETECTOR_POSITION.tag in _device_dictionary["detectors"][detector] and
                    MetadataDeviceTags.DETECTOR_GEOMETRY.tag in _device_dictionary["detectors"][detector]):
                return
            detector_geometry_type = _device_dictionary["detectors"][detector][
                MetadataDeviceTags.DETECTOR_GEOMETRY_TYPE.tag]
            detector_position = _device_dictionary["detectors"][detector][MetadataDeviceTags.DETECTOR_POSITION.tag]
            detector_geometry = np.asarray(
                _device_dictionary["detectors"][detector][MetadataDeviceTags.DETECTOR_GEOMETRY.tag])

            if detector_geometry_type == "CUBOID":
                if detector_geometry[_axes[0]] == 0:
                    detector_geometry[_axes[0]] = 0.0001
                if detector_geometry[_axes[1]] == 0:
                    detector_geometry[_axes[1]] = 0.0001
                _draw_axis.add_patch(Rectangle((detector_position[_axes[0]] - detector_geometry[_axes[0]] / 2,
                                                detector_position[_axes[1]] - detector_geometry[_axes[1]] / 2),
                                               detector_geometry[_axes[0]], detector_geometry[_axes[1]], color="blue"))
            elif detector_geometry_type == "SPHERE" or detector_geometry_type == "CIRCLE":
                _draw_axis.add_patch(Circle((detector_position[_axes[0]], detector_position[_axes[1]]), detector_geometry,
                                            color="blue"))
            else:
                print("UNSUPPORTED GEOMETRY TYPE FOR VISUALISATION. WILL DEFAULT TO 'x' visualisation.")
                _draw_axis.plot(detector_position[_axes[0]], detector_position[_axes[1]], "x", color="blue")

        if "illuminators" in _device_dictionary:
            for illuminator in _device_dictionary["illuminators"]:
                if not (MetadataDeviceTags.ILLUMINATOR_POSITION.tag in _device_dictionary["illuminators"][illuminator] and
                        MetadataDeviceTags.ILLUMINATOR_GEOMETRY.tag in _device_dictionary["illuminators"][illuminator]):
                    return
                illuminator_position = _device_dictionary["illuminators"][illuminator][
                    MetadataDeviceTags.ILLUMINATOR_POSITION.tag]
                illuminator_orientation = np.asarray(
                    _device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_ORIENTATION.tag])
                illuminator_divergence = _device_dictionary["illuminators"][illuminator][
                    MetadataDeviceTags.BEAM_DIVERGENCE_ANGLES.tag]
                illuminator_geometry = np.asarray(
                    _device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_GEOMETRY.tag])
                diameter = np.sqrt(np.sum(np.asarray([a ** 2 for a in illuminator_geometry]))) / 2
                illuminator_geometry_type = _device_dictionary["illuminators"][illuminator][
                    MetadataDeviceTags.ILLUMINATOR_GEOMETRY_TYPE.tag]

                _draw_axis.scatter(illuminator_position[_axes[0]], illuminator_position[_axes[1]],
                                   marker="+", color="red")
                x = [illuminator_position[_axes[0]],
                     illuminator_position[_axes[0]] +
                     illuminator_orientation[_axes[0]] / 25]
                y = [illuminator_position[_axes[1]],
                     illuminator_position[_axes[1]] +
                     illuminator_orientation[_axes[1]] / 25]
                plt.plot(x, y, color="yellow", alpha=1, linewidth=25, zorder=-10)

        start_indexes = np.asarray(_axes) * 2
        end_indexes = start_indexes + 1

        _draw_axis.add_patch(
            Rectangle((fov[start_indexes[0]], fov[start_indexes[1]]),
                      -fov[start_indexes[0]] + fov[end_indexes[0]],
                      -fov[start_indexes[1]] + fov[end_indexes[1]],
                      color="green", fill=False, label="Field of View"))

    if title is None:
        title = "Device Visualisation based on IPASC data format specifications"
    mins, maxs = define_boundary_values(device_dictionary)

    plt.figure(figsize=(10, 4))
    plt.suptitle(title)
    ax = plt.subplot(1, 3, 1)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    add_arbitrary_plane(device_dictionary, mins, maxs, _axes=(0, 2), _draw_axis=ax)
    ax = plt.subplot(1, 3, 2)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    add_arbitrary_plane(device_dictionary, mins, maxs, _axes=(0, 1), _draw_axis=ax)
    ax = plt.subplot(1, 3, 3)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    add_arbitrary_plane(device_dictionary, mins, maxs, _axes=(1, 2), _draw_axis=ax)

    plt.scatter(None, None, color="blue", marker="o", label="Detector Element")
    plt.scatter(None, None, color="red", marker="+", label="Illumination Element")
    plt.scatter(None, None, color="green", marker="s", label="Field of View")
    plt.scatter(None, None, color="Yellow", marker="s", label="Illumination Profile")
    plt.legend(loc="lower left")
    plt.tight_layout()
    if save_path is None:
        plt.show()
    else:
        plt.savefig(save_path + "figure.png", dpi=300)
