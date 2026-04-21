import sys
import os

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
    unique_entries.sort(key=lambda t: t[0]) # sort by atoms

    with open(output_file, 'w') as f:
        f.write("# nAtoms Max_abs Associated_freq\n")
        for natoms, max_abs, max_freq in unique_entries:
            f.write(f"{natoms} {max_abs:.10f} {max_freq:.10f}\n")

    display_message('File "natoms_abs_freq.csv" created.')
# -------------------------------------------------------------------------------------
def read_and_plot(inp):
    """
    Reads isotropic absorption data from multiple CSV files and generates a horizontal subplot
    figure showing Number of Atoms vs. Plasmon Resonance Frequency.

    Each subplot uses a distinct marker and color.

    Args:
        inp: An input_class instance containing a list of CSV file paths.

    Returns:
        None: Saves the plot as 'plot.png'.
    """
    import matplotlib
    import matplotlib.pyplot as plt

    # Set Times New Roman globally
    matplotlib.rcParams['font.family'] = 'Times New Roman'

    labelsize = 20
    ticksize = 20

    # Assume we will have a maximum of 5 plots simultaneously
    markers = ['o', 's', '^', 'D', 'v']
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']

    num_files = len(inp.files)
    fig, axes = plt.subplots(1, num_files, figsize=(6 * num_files, 5), sharey=True)

    if num_files == 1:
        axes = [axes]

    for i, file in enumerate(inp.files):
        x_vals = []
        y_vals = []

        with open(file, 'r') as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                parts = line.strip().split()
                if len(parts) >= 3:
                    x_vals.append(int(parts[0]))            # nAtoms
                    y_vals.append(float(parts[2]))          # Associated_freq (eV)

        ax = axes[i]
        ax.scatter(
            x_vals,
            y_vals,
            marker=markers[i % len(markers)],
            color=colors[i % len(colors)],
            s=80
        )
        ax.tick_params(axis='both', labelsize=ticksize)

        if i == 0:
            ax.set_ylabel("Plasmon Resonance Frequency (eV)", fontsize=labelsize)
        ax.set_xlabel("Number of Atoms", fontsize=labelsize)

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.2)  # or 0.5, 0.6, etc.
    plt.savefig("plot.png", dpi=300)
    #plt.show()
# -------------------------------------------------------------------------------------
def save_file_abs_freq(file_abs_freq):
    """
    Saves file name, maximum absorption, and associated frequency 
    extracted from plasmonX output files into a TXT file.

    Args:
        file_abs_freq: A list of [file_path, max_abs, max_freq] entries retrieved from each file.

    Returns:
        None: The function creates 'file.txt' with the data.
    """
    output_file = os.path.splitext(file_abs_freq[0])[0] + ".txt"

    with open(output_file, 'w') as f:
        f.write(f"{os.path.basename(file_abs_freq[0])} {file_abs_freq[1]:20d}   {file_abs_freq[2]:.10f}    {file_abs_freq[3]:.10f}\n")

    print(f"File {output_file} created.")
# -------------------------------------------------------------------------------------
def save_file_directional_prfs(result):
    """
    Saves directional PRFs and maximum intensities for one CSV/XYZ pair into a TXT file.

    Args:
        result: Dictionary containing filename, natoms, prfs, and intensities.

    Returns:
        None: The function creates a TXT file with the same base name as the CSV file.
    """

    output_file = os.path.splitext(result["csv_file"])[0] + ".txt"

    with open(output_file, 'w') as f:
        f.write(
            f"{os.path.basename(result['csv_file'])} "
            f"{result['natoms']:20d} "
            f"{result['intensities']['x']:.10f} "
            f"{result['intensities']['y']:.10f} "
            f"{result['intensities']['z']:.10f} "
            f"{result['prfs']['x']:.10f} "
            f"{result['prfs']['y']:.10f} "
            f"{result['prfs']['z']:.10f}\n"
        )

    print(f"File {output_file} created.")
# -------------------------------------------------------------------------------------
def save_all_directional_prfs(results):
    """
    Saves directional PRFs and maximum intensities for all CSV/XYZ pairs.

    Args:
        results: List of dictionaries containing filename, natoms, prfs, and intensities.

    Returns:
        None: The function creates 'all_prfs.csv'.
    """

    output_file = "all_prfs.csv"

    sorted_results = sorted(results, key=lambda result: result["natoms"])

    with open(output_file, 'w') as f:
        f.write("# filename.csv natoms PRF-x PRF-y PRF-z Intensity_PRF-X Intensity_PRF-y Intensity_PRF-z\n")
        for result in sorted_results:
            f.write(
                f"{os.path.basename(result['csv_file'])} "
                f"{result['natoms']:20d} "
                f"{result['prfs']['x']:.10f} "
                f"{result['prfs']['y']:.10f} "
                f"{result['prfs']['z']:.10f} "
                f"{result['intensities']['x']:.10f} "
                f"{result['intensities']['y']:.10f} "
                f"{result['intensities']['z']:.10f}\n"
            )

    print(f"File {output_file} created.")
# -------------------------------------------------------------------------------------
def save_skipped_files(skipped_files):
    """
    Saves skipped XYZ/CSV inputs and the reason they were skipped.

    Args:
        skipped_files: List of (file_path, reason) tuples.

    Returns:
        None: The function creates or removes 'skipped.err'.
    """

    output_file = "skipped.err"

    if not skipped_files:
        if os.path.exists(output_file):
            os.remove(output_file)
        return

    with open(output_file, 'w') as f:
        f.write("# file reason\n")
        for skipped_file, reason in skipped_files:
            f.write(f"{skipped_file} {reason}\n")

    print("")
    print("Some XYZ files did not have a matching CSV file, or could not be processed.")
    print(f"The skipped geometries are reported in {output_file}.")
    print(f"File {output_file} created.")
# -------------------------------------------------------------------------------------
