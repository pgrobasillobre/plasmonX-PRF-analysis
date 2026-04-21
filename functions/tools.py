import os

from functions import output

from classes import parameters

param = parameters.parameters()

# -------------------------------------------------------------------------------------
def read_natoms(file):
    """
    Reads the number of atoms from a plasmonX output file.

    The function searches for a block in the file delimited by specific headers
    indicating atomic coordinates. It extracts the first column (atom index) of the 
    last line within this block, which corresponds to the total number of atoms.

    Args:
        file (str): Path to the plasmonX output file.

    Returns:
        int: Number of atoms found in the atomic block.

    Raises:
        ValueError: If the atom index cannot be converted to an integer.
    """
    #
    natoms = 0
    found_header = False
    found_sticks_1 = False

    # First find atom header. Then sticks header. Store atom number. Stop when new sticks header is encountered.
    for line in open(file, 'r'):
       s = line.split()
       if not s:           # blank / whitespace-only line
           continue

       if found_sticks_1 and line.startswith(param.header_sticks):
           break

       if found_header and found_sticks_1:
           natoms = int(s[0])   # safe because s is non-empty

       if line.startswith(param.header_atoms):
           found_header = True

       if found_header and line.startswith(param.header_sticks):
           found_sticks_1 = True

    return natoms  # Replace with actual logic to read natoms from the file
# -------------------------------------------------------------------------------------
def read_max_absorption(file):
    """
    Reads the maximum isotropic absorption and its corresponding frequency 
    from a plasmonX output file.

    The function searches for the absorption spectrum section, reads energy and 
    absorption values, and identifies the maximum absorption along with its energy.

    Args:
        file (str): Path to the plasmonX output file.

    Returns:
        tuple:
            - found_values (bool): True if absorption data was found, False otherwise.
            - max_abs (float): Maximum absorption value (in atomic units).
            - max_freq (float): Energy at which maximum absorption occurs (in eV).

    Raises:
        ValueError: If numeric parsing fails for frequency or absorption values.
    """

    freq = []
    absorption  = []
    max_abs = 0
    max_freq = 0
    found_values = False
    found_absorption = False

    # First find maxima analysis header. Then read freqs (eV) and absorption (atomic units). Stop when sticks header is encounterd. Store maximum absorption.
    for line in open(file,'r'): 
        if (found_absorption == True):
            if not line.startswith(param.header_sticks):
                freq.append(float(line.split()[1]))
                absorption.append(float(line.split()[2]))
            elif line.startswith(param.header_sticks):
                break
        if (line.startswith(param.header_maxima_analysis)): found_absorption = True

    # Check if lists are empty and retrieve maximum absorption and associated energy
    if absorption: 
        found_values = True
        max_index = absorption.index(max(absorption))
        max_abs = absorption[max_index]
        max_freq = freq[max_index]

    return found_values, max_abs, max_freq
# -------------------------------------------------------------------------------------
def read_xyz_natoms(file):
    """
    Reads the number of atoms from an XYZ geometry file.

    The XYZ format stores the number of atoms in the first line.

    Args:
        file (str): Path to the XYZ file.

    Returns:
        int: Number of atoms declared in the XYZ file.
    """

    with open(file, 'r') as f:
        first_line = f.readline().strip()

    return int(first_line)
# -------------------------------------------------------------------------------------
def find_matching_csv(xyz_file):
    """
    Finds the CSV file associated with an XYZ file using the same base name.

    Args:
        xyz_file (str): Path to the XYZ file.

    Returns:
        str: Path to the matching CSV file.

    Raises:
        FileNotFoundError: If the matching CSV file does not exist.
    """

    csv_file = os.path.splitext(xyz_file)[0] + ".csv"

    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"Matching CSV file '{csv_file}' does not exist.")

    return csv_file
# -------------------------------------------------------------------------------------
def read_directional_prfs_from_csv(file):
    """
    Reads directional plasmon resonance frequencies from a plasmonX spectrum CSV file.

    The file is whitespace-separated. Columns are interpreted as:
        1  -> frequency in eV
        11 -> absorption along x
        12 -> absorption along y
        13 -> absorption along z

    The PRF for each direction is taken as the frequency at the maximum absorption
    in that direction.

    Args:
        file (str): Path to the CSV file.

    Returns:
        tuple:
            - found_values (bool): True if spectrum data was found.
            - prfs (dict): Directional PRFs with keys x, y, z.
            - intensities (dict): Directional maximum intensities with keys x, y, z.
    """

    rows = []

    for line in open(file, 'r'):
        stripped_line = line.strip()

        if not stripped_line or stripped_line.startswith("#"):
            continue

        parts = stripped_line.replace(",", " ").split()

        if len(parts) < 13:
            continue

        try:
            rows.append({
                "freq": float(parts[0]),
                "x": float(parts[10]),
                "y": float(parts[11]),
                "z": float(parts[12]),
            })
        except ValueError:
            continue

    if not rows:
        return False, {}, {}

    prfs = {}
    intensities = {}

    for direction in ("x", "y", "z"):
        max_row = max(rows, key=lambda row: row[direction])
        prfs[direction] = max_row["freq"]
        intensities[direction] = max_row[direction]

    return True, prfs, intensities
# -------------------------------------------------------------------------------------
