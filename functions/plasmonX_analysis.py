import sys

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
    found_values, max_abs, max_freq= tools.read_max_absorption(inp.files[0])

    # Skip this loop cycle if not absorption was found
    if not found_values:
        print(f"Skipping {inp.files[0]}: absorption data not found.")
        sys.exit()

    # Append result as [file, max_freq, max_abs]
    results = [inp.files[0], max_freq, max_abs]

    output.save_file_abs_freq(results)
# -------------------------------------------------------------------------------------
