import sys

# -------------------------------------------------------------------------------------
def error(error_message):
   """
   Prints an error message and terminates execution.

   Args:
       error_message (str): The error message to be displayed.

   Returns:
       None: The function exits the program.
   """

   print("")
   print("")
   print("   ERROR: " + error_message)
   print("")
   print("")
   sys.exit()
# -------------------------------------------------------------------------------------
def display_message(message):
   """
   Prints a formated message to the user.

   Args:
       message (str): The message to be displayed.

   Returns:
       None: The function displays a message
   """

   print("")
   print("")
   print("   " + message)
   print("")
   print("")
   sys.exit()

# -------------------------------------------------------------------------------------
def save_natoms_abs_freq(natoms_abs_freq):
    """
    Saves number of atoms, maximum absorption, and associated frequency 
    extracted from plasmonX output files into a CSV file.

    Removes exact duplicates (same number of atoms, same float values).

    Args:
        natoms_abs_freq: A list of [natoms, max_abs, max_freq] entries retrieved from each file.

    Returns:
        None: The function creates 'natoms_abs_freq.csv' with the data.
    """
    output_file = "natoms_abs_freq.csv"

    # Deduplicate using a set of exact (natoms, max_abs, max_freq) tuples
    unique_entries = list({tuple(entry) for entry in natoms_abs_freq})

    with open(output_file, 'w') as f:
        f.write("# nAtoms Max_abs Associated_freq\n")
        for natoms, max_abs, max_freq in unique_entries:
            f.write(f"{natoms} {max_abs:.10f} {max_freq:.10f}\n")

    display_message('File "natoms_abs_freq.csv" created.')
# -------------------------------------------------------------------------------------


    