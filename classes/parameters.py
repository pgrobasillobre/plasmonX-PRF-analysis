

class parameters:
    """
    Class to handle input parameters for plasmonX analysis.
    """
    # -------------------------------------------------------------------------------------
    def __init__(self):
        """
        Initialize the parameters.
        """
        # Save options
        self.header_atoms = "             Atom               X                   Y                   Z"
        self.header_sticks = ' --------------------------------------------------------------------------------'
        self.header_maxima_analysis = "          NState      Freq(eV)     Isotr. Abs. Cross. Sec.  (a.u.)"
    # -------------------------------------------------------------------------------------
