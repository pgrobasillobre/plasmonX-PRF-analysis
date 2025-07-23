import argparse

class input_class:
    """
    Manages XXXXXX

    """

    def __init__(self):
        """
        Initializes input parameters.
  
         """

        self.read_max_absorption = False
        self.plot_max_absorption = False
        self.file_patterns = []



    def read_command_line(self, args):
        """
        Parses command-line arguments and validates combinations.
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
        self.file_patterns = options.files or []

