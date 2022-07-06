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


Module List
^^^^^^^^^^^

This is the list of all Starmatrix modules::

    starmatrix.abundances
    starmatrix.constants
    starmatrix.dtds
    starmatrix.elements
    starmatrix.supernovae
    starmatrix.functions
    starmatrix.imfs
    starmatrix.matrix
    starmatrix.model
    starmatrix.settings

starmatrix.abundances
"""""""""""""""""""""

This modules include chemical abundances data: solar abundances from different papers/authors and the Abundances class, that can be subclassed to define new abundances datasets.

`starmatrix.abundances code at GitHub`_

.. _`starmatrix.abundances code at GitHub`: https://github.com/xuanxu/starmatrix/blob/main/src/starmatrix/abundances.py

starmatrix.constants
""""""""""""""""""""

This modules defines constants to use internally or as default parameters if left empty by the user.

`starmatrix.constants code at GitHub`_

.. _`starmatrix.constants code at GitHub`: https://github.com/xuanxu/starmatrix/blob/main/src/starmatrix/constants.py

starmatrix.dtds
"""""""""""""""

The dtds module contains some predefined Delay Time Distributions from different papers/authors.

`starmatrix.dtds code at GitHub`_

.. _`starmatrix.dtds code at GitHub`: https://github.com/xuanxu/starmatrix/blob/main/src/starmatrix/dtds.py


starmatrix.elements
"""""""""""""""""""

This module includes the Expelled class, used to read the file containing ejected elements data and use it to interpolate for any given mass.

`starmatrix.elements code at GitHub`_

.. _`starmatrix.elements code at GitHub`: https://github.com/xuanxu/starmatrix/blob/main/src/starmatrix/elements.py

starmatrix.supernovae
"""""""""""""""""""""

The supernovae module contains several datasets of Supernova ejections for different metallicities.

`starmatrix.supernovae code at GitHub`_

.. _`starmatrix.supernovae code at GitHub`: https://github.com/xuanxu/starmatrix/blob/main/src/starmatrix/supernovae.py


starmatrix.functions
""""""""""""""""""""

A module grouping utility methods used all around by Starmatrix modules like functions for converting between stellar mass and stellar lifetimes or to integrate initial mass functions.

`starmatrix.functions code at GitHub`_

.. _`starmatrix.functions code at GitHub`: https://github.com/xuanxu/starmatrix/blob/main/src/starmatrix/functions.py


starmatrix.imfs
"""""""""""""""

This module contains some predefined Initial Mass Functions from different papers/authors and the IMF class, that can be subclassed to define new initial mass functions.

`starmatrix.imfs code at GitHub`_

.. _`starmatrix.imfs code at GitHub`: https://github.com/xuanxu/starmatrix/blob/main/src/starmatrix/imfs.py

starmatrix.matrix
"""""""""""""""""

This module contains functions to compute Q-matrices of elements for a given mass, and Q-matrices of elements coming from Supernova events.

`starmatrix.matrix code at GitHub`_

.. _`starmatrix.matrix code at GitHub`: https://github.com/xuanxu/starmatrix/blob/main/src/starmatrix/matrix.py

starmatrix.model
""""""""""""""""

The Model class is the one actually running the explosive nucleosynthesis for the configured stellar mass range and writing the Q-matrices and the other output files.

`starmatrix.model code at GitHub`_

.. _`starmatrix.model code at GitHub`: https://github.com/xuanxu/starmatrix/blob/main/src/starmatrix/model.py

starmatrix.settings
"""""""""""""""""""

This module groups the functions in charge of defining default settings and checking all values in a set of parameters are valid. Deprecation warnings are also defined in the settings module.

`starmatrix.settings code at GitHub`_

.. _`starmatrix.settings code at GitHub`: https://github.com/xuanxu/starmatrix/blob/main/src/starmatrix/settings.py


Examples
^^^^^^^^

Run a model with your own custom parameters (in this example custom_params is a dict object modifying any of the available :doc:`configuration parameters <configuration>`) from inside your programs::

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
