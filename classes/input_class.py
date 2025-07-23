import os
import argparse

class input_class:
    """
    Handles command-line argument parsing.

    This class manages user-specified options for reading and plotting
    absorption data and collects input file paths based on glob-style patterns.
    """
    # -------------------------------------------------------------------------------------
    def __init__(self):
        """
        Initializes the input_class instance with default flags and file list.
        """

        self.read_max_absorption = False
        self.plot_max_absorption = False

        self.files = []
    # -------------------------------------------------------------------------------------
    def read_command_line(self, args):
        """
        Parses and validates command-line arguments.

        Args:
            args (list): List of command-line arguments (e.g., sys.argv[1:]).

        Raises:
            argparse.ArgumentError: If --read or --plot are given without --files.
            FileNotFoundError: If any provided file pattern does not exist.

        Side Effects:
            Sets internal flags (read_max_absorption, plot_max_absorption)
            and resolves the list of file patterns into actual paths.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('--read', action='store_true', help='Read absorption data')
        parser.add_argument('--plot', action='store_true', help='Plot absorption spectra')
        parser.add_argument('--files', nargs='+', help='List of file patterns to process')

        options = parser.parse_args(args)

        # Validate that --files is only used with --read or --plot
        if (options.read and not options.files) or (options.plot and not options.files):
            parser.error("--read or --plot + --files must be specified together.")

        # Save options
        self.read_max_absorption = options.read
        self.plot_max_absorption = options.plot
        self.files = options.files or []

        # Check files existence, otherwise raise an error
        for pattern in self.files:
            if not os.path.exists(pattern):
                raise FileNotFoundError(f"File pattern '{pattern}' does not exist.")
    # -------------------------------------------------------------------------------------

        
