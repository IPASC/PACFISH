import matplotlib.pylab as plt
from matplotlib.patches import Rectangle
import numpy as np
from ipasc_tool import MetadataDeviceTags
from test.tests.test_meta_data import create_complete_device_metadata_dictionary


def define_boundary_values(device_dictionary : dict):
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
        if fov[i] < mins[i]:
            mins[i] = fov[i]
        if fov[i] > maxs[i]:
            maxs[i] = fov[i]

    MARGIN = 0.001
    maxs += MARGIN
    mins -= MARGIN
    return mins, maxs


def add_xz_plane(device_dictionary: dict, mins, maxs):
    fov = device_dictionary["general"][MetadataDeviceTags.FIELD_OF_VIEW.tag]

    ax1 = plt.subplot(121)
    ax1.set_xlim(mins[0], maxs[0])
    ax1.set_ylim(maxs[2], mins[2])
    ax1.set_title("XZ projection")
    ax1.add_patch(
        Rectangle((mins[0], maxs[2]), np.abs(maxs[0] - mins[0]), -np.abs(maxs[2]), alpha=0.2, color="#FFD5B8",
                  label="Tissue"))
    ax1.add_patch(
        Rectangle((mins[0], 0), np.abs(maxs[0] - mins[0]), -np.abs(mins[2]), alpha=0.2, color="#444444",
                  label="Device"))

    for detector in device_dictionary["detectors"]:
        position = device_dictionary["detectors"][detector][MetadataDeviceTags.DETECTOR_POSITION.tag]
        sizes = device_dictionary["detectors"][detector][MetadataDeviceTags.DETECTOR_SIZE.tag]
        ax1.add_patch(Rectangle((position[0]-sizes[0]/2, position[2]-sizes[2]/2), sizes[0],
                                sizes[2], color="blue", alpha=0.5))

    for illuminator in device_dictionary["illuminators"]:
        position = device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_POSITION.tag]
        orientation = device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_ORIENTATION.tag]
        sizes = device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_SIZE.tag]
        ax1.add_patch(Rectangle((position[0] - sizes[0] / 2, position[2] - sizes[2] / 2), sizes[0],
                                sizes[2], color="red", alpha=0.5))
        #ax1.add_patch(Polygon([[position[0], position[2]], [], []], color="yellow", alpha=0.25))


    ax1.add_patch(
        Rectangle((0, fov[2]), fov[0], -fov[2], color="red", fill=False, label="Field of View"))


def add_xy_plane(device_dictionary: dict, mins, maxs):
    fov = device_dictionary["general"][MetadataDeviceTags.FIELD_OF_VIEW.tag]

    ax1 = plt.subplot(122)
    ax1.set_xlim(mins[0], maxs[0])
    ax1.set_ylim(maxs[1], mins[1])
    ax1.set_title("XY projection")

    for detector in device_dictionary["detectors"]:
        position = device_dictionary["detectors"][detector][MetadataDeviceTags.DETECTOR_POSITION.tag]
        sizes = device_dictionary["detectors"][detector][MetadataDeviceTags.DETECTOR_SIZE.tag]
        ax1.add_patch(Rectangle((position[0] - sizes[0] / 2, position[1] - sizes[1] / 2), sizes[0],
                                sizes[1], color="blue", alpha=0.5))

    for illuminator in device_dictionary["illuminators"]:
        position = device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_POSITION.tag]
        sizes = device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_SIZE.tag]
        ax1.add_patch(Rectangle((position[0] - sizes[0] / 2, position[1] - sizes[1] / 2), sizes[0],
                                sizes[1], color="red", alpha=0.5))

    ax1.scatter(None, None, color="blue", marker="x", label="Detector Element")
    ax1.scatter(None, None, color="red", marker="x", label="Illumination Element")

    ax1.add_patch(
        Rectangle((0, fov[1]), fov[0], -fov[1], color="red", fill=False, label="Field of View"))


def visualize_device(device_dictionary: dict, save_path: str = None):

    mins, maxs = define_boundary_values(device_dictionary)

    fig = plt.figure(figsize=(10, 5))
    add_xz_plane(device_dictionary, mins, maxs)
    add_xy_plane(device_dictionary, mins, maxs)

    plt.legend()
    if save_path is None:
        plt.show()
    else:
        plt.savefig(save_path + "figure.png", "png")


if __name__ == "__main__":

    dictionary = create_complete_device_metadata_dictionary()

    visualize_device(dictionary)
