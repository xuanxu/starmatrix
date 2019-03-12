.. intergalactic

.. |travis-badge| image:: https://travis-ci.org/xuanxu/intergalactic.svg?branch=master
   :target: https://travis-ci.org/xuanxu/intergalactic
   :alt: Build status
.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: License
   :alt: MIT License
.. |status| image:: https://img.shields.io/badge/status-alpha-orange.svg
   :alt: Project status: alpha


=============
Intergalactic
=============

|travis-badge| |license| |status|

Intergalactic is a Q-Matrix generator.

Based on explicit values for *solar abundances*, *z* and *IMF*, Intergalactic calculates matrices ``Q(i,j)`` of masses of elements *i* ejected to the galactic medium as element *j*, for a complete range of stellar masses, accounting for supernovas of types *Ia* and *Ib*.

Intergalactic computes the contribution matrix of 15 elements:

= = === === = === = = ==== == == == = == ==
H D He3 He4 C C13 N O n.r. Ne Mg Si S Ca Fe
= = === === = === = = ==== == == == = == ==

Installation
============

The easiest way to install it is using pip::

    $ pip install intergalactic

This will also install some dependencies: *numpy* and *yaml*

Input params
============

Intergalactic reads a config file where several options can be set in yaml format::

    input_params:
        z: 0.0200               # metallicity
        sol_ab: ag89            # solar abundances
        imf: kroupa             # initial mass function
        m_max: 40               # max value for stellar mass
        binary_fraction: 0.05   # rate of binary stars
        sn_ia_selection: rpl    # supernova imf

If no values are provided Intergalactic will use its internal default values for all params.

Usage
=====

Use intergalactic running::

    $ intergalactic --config FILENAME

where *FILENAME* is the path to the config yaml file.

Running intergalactic will produce a directory with three output files:

    * mass_intervals : all the mass intervals used to integrate for all the mass range
    * imf_supernova_rates : the initial mass functions for the supernova rates for each mass interval
    * qm-matrices : the Q(m) matrices for every mass interval defined in the *mass_intervals* file


License
=======

*Copyright* © 2019 Juanjo Bazán, released under the `MIT license`_.

.. _`MIT license`: LICENSE
