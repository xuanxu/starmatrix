Usage
=====


Basic
-----

Use Starmatrix running::

    $ starmatrix --config FILENAME

where *FILENAME* is the path to the config yaml file.

Running Starmatrix will produce a directory with three output files:

* **mass_intervals**: all the mass intervals used to integrate for all the mass range
* **imf_supernova_rates**: the initial mass functions for the supernova rates for each mass interval
* **qm-matrices**: the Q(m) matrices for every mass interval defined in the *mass_intervals* file


Advanced
--------

If you have Starmatrix installed in your system, you can import its modules, classes and functions to use them in your own code.

This is the list of all Starmatrix modules::

    starmatrix.abundances
    starmatrix.constants
    starmatrix.dtds
    starmatrix.elements
    starmatrix.functions
    starmatrix.imfs
    starmatrix.matrix
    starmatrix.model
    starmatrix.settings

**Examples:**

Run a model with your own custom parameters from inside your programs::

    import starmatrix
    import starmatrix.settings as settings
    from starmatrix.model import Model

    custom_params = { ... }
    context = settings.validate(custom_params)
    Model(context).run()

Call Starmatrix utility functions::

    import starmatrix.functions as functions

    stellar_mass = 4.3
    z = 0.02
    stellar_tau = functions.stellar_lifetime(stellar_mass, z)

Compute the contributions matrix of supernovae for a given mass::

    import starmatrix.matrix as matrix

    stellar_mass = 4.3
    contribution_matrix = matrix.q_sn(stellar_mass)
