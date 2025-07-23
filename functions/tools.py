from classes import parameters

param = parameters.parameters()

def read_natoms(file):
    """
    Reads the number of atoms from a plasmonX output file by grabbing
    the first column of the last atomic line between the header markers.
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