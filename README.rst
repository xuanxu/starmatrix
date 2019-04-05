.. intergalactic

.. |travis-badge| image:: https://travis-ci.org/xuanxu/intergalactic.svg?branch=master
   :target: https://travis-ci.org/xuanxu/intergalactic
   :alt: Build status
.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/xuanxu/intergalactic/blob/master/LICENSE
   :alt: MIT License
.. |version| image:: https://img.shields.io/pypi/v/intergalactic.svg?color=brightgreen
   :target: https://pypi.org/project/intergalactic/
   :alt: Intergalactic in PyPi


=============
Intergalactic
=============

|travis-badge| |license| |version|

Intergalactic is a Q-Matrix generator.

Based on explicit values for *solar abundances*, *z* and *IMF*, Intergalactic calculates matrices ``Q(i,j)`` of masses of elements ``i`` ejected to the galactic medium as element ``j``, for a complete range of stellar masses, accounting for supernovas of types *Ia* and *Ib*.

Intergalactic computes the contribution matrix of 15 elements:

= = === === = === = = ==== == == == = == ==
H D He3 He4 C C13 N O n.r. Ne Mg Si S Ca Fe
= = === === = === = = ==== == == == = == ==

Installation
============

The easiest way to install it is using pip::

    $ pip install intergalactic

This will also install some dependencies: *numpy* and *yaml*

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

    input_params:
        z: 0.0200               # metallicity
        sol_ab: ag89            # solar abundances
        imf: kroupa             # initial mass function
        m_max: 40               # max value for stellar mass
        binary_fraction: 0.05   # rate of binary stars
        dtd_sn: rlp             # delay time distribution for supernovas

If no values are provided Intergalactic will use its internal default values for all params.

If you want to use an existent configuration file as template for your own, you can run::

    $ intergalactic --generate-config

That command will create a ``config-example.yml`` file in the current dir.


Initial mass function
---------------------

The ``imf`` param in the config file can be set to use any of the predefined IMFs from different papers/authors:

:salpeter: Salpeter 1955
:starburst: Starburst 1999
:miller_scalo: Miller & Scalo 1979
:ferrini: Ferrini, Palla & Penco 1998
:kroupa: Kroupa 2002
:chabrier: Chabrier 2003
:maschberger: Maschberger 2012

The default value is ``kroupa``. If you want to use your own IMF you can do so subclassing the `IMF class`_.

.. _`IMF class`: https://github.com/xuanxu/intergalactic/blob/master/src/intergalactic/imfs.py#L20-L40

Solar abundances
----------------

The ``sol_ab`` param in the config file can be set to use any of the available abundances datasets from different papers/authors:

:ag89: Anders & Grevesse 1989
:gs98: Grevesse & Sauval 1998
:as05: Asplund et al. 2005
:as09: Asplund et al. 2009
:he10: Heger 2010

The default value is ``as09``. If you want to use your own abundances data you can do so subclassing the `Abundances class`_.

.. _`Abundances class`: https://github.com/xuanxu/intergalactic/blob/master/src/intergalactic/abundances.py#L18-L47

Delay Time Distributions
------------------------

The ``dtd_sn`` param in the config file can be set to use any of the available Delay Time Distributions for supernova rates from different papers/authors:

:rlp: Supernova rates from Pilar Ruiz-Lapuente
:mdvp: DTD from Mannucci, Della Valle, Panagia 2006

License
=======

*Copyright* © 2019 Juanjo Bazán, released under the `MIT license`_.

.. _`MIT license`: https://github.com/xuanxu/intergalactic/blob/master/LICENSE

Credits
=======

Intergalactic is built upon a long list of previous works from different authors/papers:

* *Ferrini et al.*,1992, ApJ, 387, 138
* *Ferrini & Poggiantti*, 1993, ApJ, 410, 44F
* *Portinari, Chiosi & Bressan.*,1998,AA,334,505P
* *Galli et al.*, 1995, ApJ, 443, 536G
* *Mollá et al*, 2015, MNRAS, 451, 3693-3708
* *Iwamoto et al*, 1999, ApJS, 125, 439
* *Matteucci & Greggio*, 1986, A&A, 154, 279M
* *Mollá et al*, 2017, MNRAS, 468, 305-318
* *Gavilan, Mollá & Buell*, 2006, A&A, 450, 509
* *Raiteri C.M., Villata M. & Navarro J.F.*, 1996, A&A 315, 105-115
* *Mannucci, Della Valle, Panagia* (2006)
