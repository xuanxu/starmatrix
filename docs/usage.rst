Usage
=====


Basic
-----

Use Intergalactic running::

    $ intergalactic --config FILENAME

where *FILENAME* is the path to the config yaml file.

Running Intergalactic will produce a directory with three output files:

* **mass_intervals**: all the mass intervals used to integrate for all the mass range
* **imf_supernova_rates**: the initial mass functions for the supernova rates for each mass interval
* **qm-matrices**: the Q(m) matrices for every mass interval defined in the *mass_intervals* file


Advanced
--------

If you have Intergalactic installed in your system, you can import its modules, classes and functions to use them in your own code.

This is the list of all Intergalactic modules::

    intergalactic.abundances
    intergalactic.constants
    intergalactic.dtds
    intergalactic.elements
    intergalactic.functions
    intergalactic.imfs
    intergalactic.matrix
    intergalactic.model
    intergalactic.settings

**Examples:**

Run a model with your own custom parameters from inside your programs::

    import intergalactic
    import intergalactic.settings as settings
    from intergalactic.model import Model

    custom_params = { ... }
    context = settings.validate(custom_params)
    Model(context).run()

Call Intergalactic utility functions::

    import intergalactic.functions as functions

    stellar_mass = 4.3
    z = 0.02
    stellar_tau = functions.stellar_lifetime(stellar_mass, z)

Compute the contributions matrix of supernovas for a given mass::

    import intergalactic.matrix as matrix

    stellar_mass = 4.3
    contribution_matrix = matrix.q_sn(stellar_mass)
