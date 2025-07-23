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
        if (found_sticks_1) and (line.startswith(param.header_sticks)): break
        if (found_header == True and found_sticks_1 == True): natoms = int(line.split()[0])
        if line.startswith(param.header_atoms): found_header = True
        if (found_header == True) and (line.startswith(param.header_sticks)): found_sticks_1 = True
        
    
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

