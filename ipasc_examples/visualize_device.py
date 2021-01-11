import matplotlib.pylab as plt
from matplotlib.patches import Rectangle, Polygon
import numpy as np
from ipasc_tool import MetadataDeviceTags
from ipasc_test.tests.test_meta_data import create_complete_device_metadata_dictionary


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


def add_xz_plane(device_dictionary: dict, mins, maxs):
    fov = device_dictionary["general"][MetadataDeviceTags.FIELD_OF_VIEW.tag]

    ax1 = plt.subplot(131)
    ax1.set_xlim(mins[0], maxs[0])
    ax1.set_ylim(maxs[2], mins[2])
    ax1.set_title("XZ projection (side view)")

    for detector in device_dictionary["detectors"]:
        position = device_dictionary["detectors"][detector][MetadataDeviceTags.DETECTOR_POSITION.tag]
        shape = np.asarray(device_dictionary["detectors"][detector][MetadataDeviceTags.DETECTOR_SHAPE.tag])
        ax1.add_patch(Rectangle((position[0]-shape[0]/2, position[2]-shape[0]/2), shape[0],
                                shape[0], color="blue", alpha=0.5))

    for illuminator in device_dictionary["illuminators"]:
        position = device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_POSITION.tag]
        orientation = device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_ORIENTATION.tag]
        divergence = device_dictionary["illuminators"][illuminator][MetadataDeviceTags.BEAM_DIVERGENCE_ANGLES.tag]
        shape = np.asarray(device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_SHAPE.tag])
        ax1.add_patch(Rectangle((position[0] - shape[0] / 2, position[2] - shape[0] / 2), shape[0],
                                shape[0], color="red", alpha=0.5))
        # length = 0.01
        # x_middle = position[0] + length * np.sin(orientation[1])
        # z_middle = position[2] + length * np.cos(orientation[1])
        # x_middle_1 = position[0] + length * np.sin(orientation[1] + divergence)
        # z_middle_1 = position[2] + length * np.cos(orientation[1] + divergence)
        # x_middle_2 = position[0] + length * np.sin(orientation[1] - divergence)
        # z_middle_2 = position[2] + length * np.cos(orientation[1] - divergence)
        # ax1.add_patch(Polygon([[position[0] - sizes[0] / 2, position[2]],
        #                        [position[0] + sizes[0] / 2, position[2]],
        #                        [x_middle_1, z_middle_1],
        #                        [x_middle_2, z_middle_2],
        #                        [position[0], position[2]]], color="yellow", alpha=0.25))
        # ax1.add_patch(Polygon([[position[0] - sizes[0] / 2, position[2]],
        #                        [position[0] + sizes[0] / 2, position[2]],
        #                        [x_middle, z_middle],
        #                        [position[0], position[2]]], color="orange", alpha=0.5))


    ax1.add_patch(
        Rectangle((fov[0], fov[4]), fov[1], fov[5], color="green", fill=False, label="Field of View"))


def add_xy_plane(device_dictionary: dict, mins, maxs):
    fov = device_dictionary["general"][MetadataDeviceTags.FIELD_OF_VIEW.tag]

    ax1 = plt.subplot(132)
    ax1.set_xlim(mins[0], maxs[0])
    ax1.set_ylim(maxs[1], mins[1])
    ax1.set_title("XY projection (top view)")

    for detector in device_dictionary["detectors"]:
        position = device_dictionary["detectors"][detector][MetadataDeviceTags.DETECTOR_POSITION.tag]
        sizes = np.asarray(device_dictionary["detectors"][detector][MetadataDeviceTags.DETECTOR_SHAPE.tag])
        ax1.add_patch(Rectangle((position[0] - sizes[0] / 2, position[1] - sizes[0] / 2), sizes[0],
                                sizes[0], color="blue", alpha=0.5))

    for illuminator in device_dictionary["illuminators"]:
        position = device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_POSITION.tag]
        sizes = np.asarray(device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_SHAPE.tag])
        ax1.add_patch(Rectangle((position[0] - sizes[0] / 2, position[1] - sizes[0] / 2), sizes[0],
                                sizes[0], color="red", alpha=0.5))

    ax1.scatter(None, None, color="blue", marker="x", label="Detector Element")
    ax1.scatter(None, None, color="red", marker="x", label="Illumination Element")

    ax1.add_patch(
        Rectangle((fov[0], fov[2]), fov[1], fov[3], color="green", fill=False, label="Field of View"))


def add_yz_plane(device_dictionary: dict, mins, maxs):
    fov = device_dictionary["general"][MetadataDeviceTags.FIELD_OF_VIEW.tag]

    ax1 = plt.subplot(133)
    ax1.set_xlim(mins[1], maxs[1])
    ax1.set_ylim(maxs[2], mins[2])
    ax1.set_title("YZ projection (imaging plane)")

    for detector in device_dictionary["detectors"]:
        position = device_dictionary["detectors"][detector][MetadataDeviceTags.DETECTOR_POSITION.tag]
        shape = np.asarray(device_dictionary["detectors"][detector][MetadataDeviceTags.DETECTOR_SHAPE.tag])
        ax1.add_patch(Rectangle((position[1] - shape[0] / 2, position[2] - shape[0] / 2), shape[0],
                                shape[0], color="blue", alpha=0.5))

    for illuminator in device_dictionary["illuminators"]:
        position = device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_POSITION.tag]
        shape = np.asarray(device_dictionary["illuminators"][illuminator][MetadataDeviceTags.ILLUMINATOR_SHAPE.tag])
        ax1.add_patch(Rectangle((position[1] - shape[0] / 2, position[2] - shape[0] / 2), shape[0],
                                shape[0], color="red", alpha=0.5))

    ax1.scatter(None, None, color="blue", marker="x", label="Detector Element")
    ax1.scatter(None, None, color="red", marker="x", label="Illumination Element")

    ax1.add_patch(
        Rectangle((fov[2], fov[4]), fov[3], fov[5], color="green", fill=False, label="Field of View"))


def visualize_device(device_dictionary: dict, save_path: str = None):

    mins, maxs = define_boundary_values(device_dictionary)

    fig = plt.figure(figsize=(10, 5))
    add_xz_plane(device_dictionary, mins, maxs)
    add_xy_plane(device_dictionary, mins, maxs)
    add_yz_plane(device_dictionary, mins, maxs)

    plt.legend(loc="best")
    if save_path is None:
        plt.show()
    else:
        plt.savefig(save_path + "figure.png", "png")


if __name__ == "__main__":

    dictionary = create_complete_device_metadata_dictionary()

    visualize_device(dictionary)
