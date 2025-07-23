import sys

from functions import output, plasmonX_analysis
from classes import input_class 

# ============================================================================================================ #
#                                        Program by Pablo Grobas Illobre                                       #
#                                                                                                              #
#                                       Contact: pgrobasillobre@gmail.com                                      #
# ============================================================================================================ #

def main():
    """
    Main function to initialize input parameters and execute the appropriate task based on user input.

    Returns:
        None: Calls the relevant function based on the user's input.
    """
    try:
        # Parse command-line arguments
        inp = input_class.input_class()
        inp.read_command_line(sys.argv[1:])

        # Select and execute the appropriate task
        if inp.read_max_absorption:
            plasmonX_analysis.read_absorption(inp)
        elif inp.plot_max_absorption:
            output.error("Plotting functionality is not implemented yet.")

    except Exception as e:
        output.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
