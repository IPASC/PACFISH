from pacfish import load_data
from pacfish.qualitycontrol.PADataIntegrityCheck import quality_check_pa_data
from pacfish.visualize_device import visualize_device
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Display all data available in the IPASC format")
    parser.add_argument("input", metavar="i", type=str, help="input path to the IPASC-formatted HDF5 file.")
    args = parser.parse_args()

    pa_data = load_data(args.input)
    quality_check_pa_data(pa_data, verbose=True)
    visualize_device(pa_data.meta_data_device)
    print("")
    print("=====================================================================")
    print("              PRINTING ALL DATA AVAILABLE IN HDF5")
    print("=====================================================================")
    print(pa_data.__dict__)