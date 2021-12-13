import matplotlib.pylab as plt
from matplotlib.patches import Rectangle, Circle, Polygon
import numpy as np
from ipasc_tool import MetadataDeviceTags


def define_boundary_values(device_dictionary: dict):
    mins = np.zeros(3)
    maxs = np.ones(3) * -1000

    for illuminator in device_dictionary["illuminators"]:
        position = device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_POSITION.tag]
        for i in range(3):
            if position[i] < mins[i]:
                mins[i] = position[i]
            if position[i] > maxs[i]:
                maxs[i] = position[i]

    for detector in device_dictionary["detectors"]:
        position = device_dictionary["detectors"][detector][MetadataDeviceTags.DETECTOR_POSITION.tag]
        for i in range(3):
            if position[i] < mins[i]:
                mins[i] = position[i]
            if position[i] > maxs[i]:
                maxs[i] = position[i]

    fov = device_dictionary["general"][MetadataDeviceTags.FIELD_OF_VIEW.tag]
    for i in range(3):
        if fov[2*i] < mins[i]:
            mins[i] = fov[2*i]
        if fov[2*i+1] < mins[i]:
            mins[i] = fov[2*i+1]
        if fov[2*i] > maxs[i]:
            maxs[i] = fov[2*i]
        if fov[2*i+1] > maxs[i]:
            maxs[i] = fov[2*i+1]

    MARGIN = 0.001
    maxs += MARGIN
    mins -= MARGIN
    return mins, maxs


def add_arbitrary_plane(device_dictionary: dict, mins, maxs, axes, draw_axis):
    print("AXES:", axes)
    draw_axis.set_xlim(mins[axes[0]], maxs[axes[0]])
    draw_axis.set_ylim(maxs[axes[1]], mins[axes[1]])
    draw_axis.set_title(f"axes {axes[0]}/{axes[1]} projection view")
    draw_axis.set_xlabel(f"{axes[0]}-axis [m]")
    draw_axis.set_ylabel(f"{axes[1]}-axis [m]")

    fov = device_dictionary["general"][MetadataDeviceTags.FIELD_OF_VIEW.tag]

    for detector in device_dictionary["detectors"]:
        if not (MetadataDeviceTags.DETECTOR_POSITION.tag in device_dictionary["detectors"][detector] and
                MetadataDeviceTags.DETECTOR_GEOMETRY.tag in device_dictionary["detectors"][detector]):
            return
        detector_geometry_type = device_dictionary["detectors"][detector][MetadataDeviceTags.DETECTOR_GEOMETRY_TYPE.tag]
        detector_position = device_dictionary["detectors"][detector][MetadataDeviceTags.DETECTOR_POSITION.tag]
        detector_geometry = np.asarray(device_dictionary["detectors"][detector][MetadataDeviceTags.DETECTOR_GEOMETRY.tag])

        if detector_geometry_type == "CUBOID":
            if detector_geometry[axes[0]] == 0:
                detector_geometry[axes[0]] = 0.0001
            if detector_geometry[axes[1]] == 0:
                detector_geometry[axes[1]] = 0.0001
            draw_axis.add_patch(Rectangle((detector_position[axes[0]] - detector_geometry[axes[0]]/2,
                                           detector_position[axes[1]] - detector_geometry[axes[1]]/2),
                                          detector_geometry[axes[0]], detector_geometry[axes[1]], color="blue"))
        elif detector_geometry_type == "SHPERE" or detector_geometry_type == "CIRCLE":
            draw_axis.add_patch(Circle((detector_position[axes[0]], detector_position[axes[1]]), detector_geometry,
                                       color="blue"))
        else:
            print("UNSUPPORTED GEOMETRY TYPE FOR VISUALISATION. WILL DEFAULT TO 'x' visualisation.")
            draw_axis.plot(detector_position[axes[0]], detector_position[axes[1]], "x", color="blue")

    for illuminator in device_dictionary["illuminators"]:
        if not (MetadataDeviceTags.ILLUMINATOR_POSITION.tag in device_dictionary["illuminators"][illuminator] and
                MetadataDeviceTags.ILLUMINATOR_GEOMETRY.tag in device_dictionary["illuminators"][illuminator]):
            return
        illuminator_position = device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_POSITION.tag]
        illuminator_orientation = np.asarray(device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_ORIENTATION.tag])
        illuminator_divergence = device_dictionary["illuminators"][illuminator][MetadataDeviceTags.BEAM_DIVERGENCE_ANGLES.tag]
        illuminator_geometry = np.asarray(device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_GEOMETRY.tag])
        diameter = np.sqrt(np.sum(np.asarray([a**2 for a in illuminator_geometry]))) / 2
        illuminator_geometry_type = device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_GEOMETRY_TYPE.tag]

        draw_axis.scatter(illuminator_position[axes[0]], illuminator_position[axes[1]],
                                   marker="+", color="red")
        x = [illuminator_position[axes[0]],
             illuminator_position[axes[0]] +
             illuminator_orientation[axes[0]]/25]
        y = [illuminator_position[axes[1]],
             illuminator_position[axes[1]] +
             illuminator_orientation[axes[1]]/25]
        plt.plot(x, y, color="yellow", alpha=1, linewidth=25, zorder=-10)

    start_indexes = np.asarray(axes) * 2
    end_indexes = start_indexes + 1

    draw_axis.add_patch(
        Rectangle((fov[start_indexes[0]], fov[start_indexes[1]]),
                  -fov[start_indexes[0]] + fov[end_indexes[0]],
                  -fov[start_indexes[1]] + fov[end_indexes[1]],
                  color="green", fill=False, label="Field of View"))


def visualize_device(device_dictionary: dict, save_path: str = None, title: str=None):

    if title is None:
        title = "Device Visualisation based on IPASC data format specifications"
    mins, maxs = define_boundary_values(device_dictionary)

    plt.figure(figsize=(10, 4))
    plt.suptitle(title)
    ax = plt.subplot(1, 3, 1)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    add_arbitrary_plane(device_dictionary, mins, maxs, axes=(0, 2), draw_axis=ax)
    ax = plt.subplot(1, 3, 2)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    add_arbitrary_plane(device_dictionary, mins, maxs, axes=(0, 1), draw_axis=ax)
    ax = plt.subplot(1, 3, 3)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    add_arbitrary_plane(device_dictionary, mins, maxs, axes=(1, 2), draw_axis=ax)

    # plt.subplot(1, 4, 4)
    #
    #
    plt.scatter(None, None, color="blue", marker="o", label="Detector Element")
    plt.scatter(None, None, color="red", marker="+", label="Illumination Element")
    plt.scatter(None, None, color="green", marker="s", label="Field of View")
    plt.scatter(None, None, color="Yellow", marker="s", label="Illumination Profile")
    plt.legend(loc="lower left")
    plt.tight_layout()
    if save_path is None:
        plt.show()
    else:
        plt.savefig(save_path + "figure.png", "png")
