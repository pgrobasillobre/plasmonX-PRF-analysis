import sys
import os

from functions import output, tools

# -------------------------------------------------------------------------------------
def read_atoms_absorption_freq_and_save(inp):
    """
    Reads isotropic absorption data from specified plasmonX output files.

    Args:
        inp: An input_class instance containing a list of files to read.

    Returns:
        list: A list of [natoms, max_freq, max_abs] for each valid file.
    """
    results = []

    for file in inp.files:
        # Initialize variables
        natoms = 0
        max_absorption = 0.0

        # Read the file
        natoms = tools.read_natoms(file)
        found_values, max_abs, max_freq= tools.read_max_absorption(file)

        # Skip this loop cycle if not absorption was found
        if not found_values:
            print(f"Skipping {file}: absorption data not found.")
            continue

        #print(f"For file {file}, natoms = {natoms}, max_abs = {max_abs}, max_freq = {max_freq}")

        # Append result as [natoms, max_freq, max_abs]
        results.append([natoms, max_freq, max_abs])

    output.save_natoms_abs_freq(results)
# -------------------------------------------------------------------------------------
def read_file_absorption_freq_and_save(inp):
    """
    Reads isotropic absorption data from specified plasmonX output files.

    Args:
        inp: An input_class instance containing a list of files to read.

    Returns:
        list: A list of [filename, max_freq, max_abs] for each valid file.
    """

    # Initialize variables
    max_absorption = 0.0

    # Read the file
    natoms = tools.read_natoms(inp.files[0])
    found_values, max_abs, max_freq= tools.read_max_absorption(inp.files[0])

    # Skip this loop cycle if not absorption was found
    if not found_values:
        print(f"Skipping {inp.files[0]}: absorption data not found.")
        sys.exit()

    # Append result as [file, max_freq, max_abs]
    results = [inp.files[0], natoms, max_freq, max_abs]

    output.save_file_abs_freq(results)
# -------------------------------------------------------------------------------------
def read_xyz_csv_directional_prfs_and_save(inp):
    """
    Reads XYZ files, finds their associated CSV spectra, and extracts directional PRFs.

    Args:
        inp: An input_class instance containing a list of XYZ files to read.

    Returns:
        list: A list of result dictionaries for each valid XYZ/CSV pair.
    """

    results = []
    skipped_files = []

    for xyz_file in inp.files:
        if not os.path.exists(xyz_file):
            skipped_files.append((xyz_file, "XYZ file not found"))
            continue

        try:
            csv_file = tools.find_matching_csv(xyz_file)
        except FileNotFoundError:
            skipped_files.append((xyz_file, "matching CSV file not found"))
            continue

        natoms = tools.read_xyz_natoms(xyz_file)
        found_values, prfs, intensities = tools.read_directional_prfs_from_csv(csv_file)

        if not found_values:
            skipped_files.append((csv_file, "directional spectrum data not found"))
            continue

        result = {
            "csv_file": csv_file,
            "natoms": natoms,
            "prfs": prfs,
            "intensities": intensities,
        }

        results.append(result)
        output.save_file_directional_prfs(result)

    if results:
        output.save_all_directional_prfs(results)
    else:
        print("No directional PRF data found.")

    output.save_skipped_files(skipped_files)

    if not results:
        sys.exit()
# -------------------------------------------------------------------------------------
