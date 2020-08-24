.. intergalactic

.. |travis-badge| image:: https://travis-ci.org/xuanxu/intergalactic.svg?branch=master
   :target: https://travis-ci.org/xuanxu/intergalactic
   :alt: Build status
.. |docs-badge| image:: https://readthedocs.org/projects/intergalactic/badge/?version=latest
   :target: https://intergalactic.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. |codecov-badge| image:: https://codecov.io/gh/xuanxu/intergalactic/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/xuanxu/intergalactic
   :alt: Coverage status
.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/xuanxu/intergalactic/blob/master/LICENSE
   :alt: MIT License
.. |version| image:: https://img.shields.io/pypi/v/intergalactic.svg?color=brightgreen
   :target: https://pypi.org/project/intergalactic/
   :alt: Intergalactic in PyPi


=============
Intergalactic
=============

|travis-badge| |docs-badge| |codecov-badge| |license| |version|

Intergalactic is a Q-Matrices generator.

Based on explicit values for *solar abundances*, *z* and *IMF*, Intergalactic calculates matrices ``Q(i,j)`` of masses of elements ``i`` ejected to the galactic medium as element ``j``, for a complete range of stellar masses, accounting for supernovas of types ``Ia`` and ``II``. You can read more about the ``Matrices Q formalism`` in ``Ferrini et al. 1992``.

Intergalactic computes the contribution matrix of 15 elements:

= = === === = === = = ==== == == == = == ==
H D He3 He4 C C13 N O n.r. Ne Mg Si S Ca Fe
= = === === = === = = ==== == == == = == ==

Installation
============

The easiest way to install the package is using pip::

    $ pip install intergalactic

This will also install some dependencies if they are not found in the system: *numpy*, *scipy* and *pyyaml*

A previous installation can be upgraded to the latest version with::

    $ pip install --upgrade intergalactic

Usage
=====

Use intergalactic running::

    $ intergalactic --config FILENAME

where *FILENAME* is the path to the config yaml file.

Running intergalactic will produce a directory with three output files:

* **mass_intervals**: all the mass intervals used to integrate for all the mass range
* **imf_supernova_rates**: the initial mass functions for the supernova rates for each mass interval
* **qm-matrices**: the Q(m) matrices for every mass interval defined in the *mass_intervals* file

Input params
============

Intergalactic reads a config file where several options can be set in yaml format::

        z: 0.0200               # metallicity
        sol_ab: as09            # solar abundances
        imf: kroupa             # initial mass function (IMF)
        imf_m_low: 0.15         # lower mass limit for the IMF
        imf_m_up: 100           # upper mass limit for the IMF
        total_time_steps: 300   # number of time steps (will result in a Q Matrix per step)
        m_min: 0.98             # min value for stellar mass
        m_max: 40               # max value for stellar mass
        binary_fraction: 0.15   # rate of binary stars
        dtd_sn: rlp             # delay time distribution for supernovas
        output_dir: results     # Name of the directory where results are written.
        integration_step: logt  # The integration step can be constant in t, constant in log(t), or custom.
        expelled_elements_filename: ejecta.txt  # Filename of ejected data.

Intergalactic will use its internal default values for all params for which no values are provided.

If you want to use an existent configuration file as template for your own, you can run::

    $ intergalactic --generate-config

That command will create a ``config-example.yml`` file in the current dir.


Initial mass function
---------------------

The ``imf`` param in the config file can be set to use any of the predefined IMFs from different papers/authors:

:salpeter: Salpeter 1955
:starburst: Starburst 1999 (a Salpeter with mass limits in [1, 120])
:miller_scalo: Miller & Scalo 1979
:ferrini: Ferrini, Palla & Penco 1998
:kroupa: Kroupa 2002
:chabrier: Chabrier 2003
:maschberger: Maschberger 2012

The default value is ``kroupa``. If you want to use your own IMF you can do so subclassing the `IMF class`_.

.. _`IMF class`: https://github.com/xuanxu/intergalactic/blob/master/src/intergalactic/imfs.py#L35-L68

The IMF will be normalized integrating in the ``[imf_m_low, imf_m_up]`` mass interval (default: ``[0.15, 100]``, except ``Starburst``: ``[1, 120]``).

Solar abundances
----------------

The ``sol_ab`` param in the config file can be set to use any of the available abundances datasets from different papers/authors:

:ag89: Anders & Grevesse 1989
:gs98: Grevesse & Sauval 1998
:as05: Asplund et al. 2005
:as09: Asplund et al. 2009
:he10: Heger 2010
:lo19: Lodders et al. 2019

The default value is ``as09``. If you want to use your own abundances data you can do so subclassing the `Abundances class`_.

.. _`Abundances class`: https://github.com/xuanxu/intergalactic/blob/master/src/intergalactic/abundances.py#L30-L59

Delay Time Distributions
------------------------

The ``dtd_sn`` param in the config file can be set to use any of the available Delay Time Distributions for supernova rates from different papers/authors:

:rlp: Supernova rates from Ruiz-Lapuente et al. 2000
:maoz: DTD of Type Ia supernovae from Maoz & Graur (2017)
:castrillo: DTD of Type Ia supernovae from Castrillo et al. (2020)
:greggio: DTD of Type Ia supernovae from Greggio, L. (2005)

Test suite
==========

Intergalactic includes a test suite located in the ``/src/intergalactic/tests`` directory. The current state of the build is `publicly tracked by Travis CI`_. You can run the latest tests locally and get information on code coverage if you clone the code to your local machine, install its development dependencies and use ``pytest``::

    $ git clone https://github.com/xuanxu/intergalactic.git
    $ cd intergalactic
    $ pip install -e .[dev]
    $ pytest -v --cov=intergalactic

.. _`publicly tracked by Travis CI`: https://travis-ci.org/xuanxu/intergalactic

Edge
====

If you want to play with the latest code present in this repository even if it has not been released yet, you can do it by cloning the repo locally and instructing pip to install it::

    $ git clone https://github.com/xuanxu/intergalactic.git
    $ cd intergalactic
    $ pip install -e .

License
=======

*Copyright* © 2020 Juanjo Bazán, released under the `MIT license`_.

.. _`MIT license`: https://github.com/xuanxu/intergalactic/blob/master/LICENSE

Credits
=======

Intergalactic is built upon a long list of previous works from different authors/papers:

* *Ferrini et al.*,1992, ApJ, 387, 138
* *Ferrini & Poggiantti*, 1993, ApJ, 410, 44F
* *Portinari, Chiosi & Bressan*,1998,AA,334,505P
* *Galli et al.*, 1995, ApJ, 443, 536G
* *Mollá et al.*, 2015, MNRAS, 451, 3693-3708
* *Iwamoto et al.*, 1999, ApJS, 125, 439
* *Matteucci & Greggio*, 1986, A&A, 154, 279M
* *Mollá et al.*, 2017, MNRAS, 468, 305-318
* *Gavilan, Mollá & Buell*, 2006, A&A, 450, 509
* *Raiteri C.M., Villata M. & Navarro J.F.*, 1996, A&A 315, 105-115
* *Ruiz-Lapuente, P., Canal, R.*, 2000, astro.ph..9312R
* *Maoz, D. & Graur, O.* 2017, ApJ, 848, 25M
* *Castrillo, A. et al* 2020, MNRAS (*in preparation*)
* *Greggio, L.* 2005, A&A 441, 1055–1078
