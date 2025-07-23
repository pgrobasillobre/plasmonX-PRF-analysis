
from functions import output, tools

# -------------------------------------------------------------------------------------
def read_absorption(inp):
    """
    Reads isotropic absorption data from specified plasmonX output files.
    """

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

        print(f"For file {file}, natoms = {natoms}, max_abs = {max_abs}, max_freq = {max_freq}")




