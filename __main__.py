import sys

from functions import output
from classes import input_class 

# ============================================================================================================ #
#                                        Program by Pablo Grobas Illobre                                       #
#                                                                                                              #
#                                       Contact: pgrobasillobre@gmail.com                                      #
# ============================================================================================================ #


def main():
    """
    Main function to XXXXXXXXXXX.

    Returns:
        None: Calls the relevant function based on the user's input.
    """
    try:
        # Parse command-line arguments
        inp = input_class.input_class()
        inp.read_command_line(sys.argv[1:])

        #general.read_command_line(sys.argv, inp)

        # Select and execute the appropriate task
        if inp.read_max_absorption:
            pass

    except Exception as e:
        output.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
