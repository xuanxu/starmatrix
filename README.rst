.. starmatrix

.. |ci-badge| image:: https://github.com/xuanxu/starmatrix/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/xuanxu/starmatrix/actions/workflows/tests.yml
   :alt: Build status
.. |docs-badge| image:: https://readthedocs.org/projects/starmatrix/badge/?version=latest
   :target: https://starmatrix.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. |codecov-badge| image:: https://codecov.io/gh/xuanxu/starmatrix/branch/main/graph/badge.svg?token=JRNGFn3SjA
   :target: https://codecov.io/gh/xuanxu/starmatrix
   :alt: Coverage status
.. |license| image:: https://img.shields.io/github/license/xuanxu/starmatrix?color=brightgreen
   :target: https://github.com/xuanxu/starmatrix/blob/main/LICENSE
   :alt: MIT License
.. |version| image:: https://img.shields.io/pypi/v/starmatrix.svg?color=brightgreen
   :target: https://pypi.org/project/starmatrix/
   :alt: starmatrix in PyPi
.. |paper-link| image:: https://joss.theoj.org/papers/10.21105/joss.04461/status.svg
   :target: https://doi.org/10.21105/joss.04461
   :alt: Paper
   
============
✨Starmatrix
============

|ci-badge| |docs-badge| |codecov-badge| |license| |version| |paper-link| 

Starmatrix is a Q-Matrices generator.

Based on explicit values for *solar abundances*, *Z* and *IMF*, Starmatrix calculates matrices ``Q(i,j)`` of masses of elements ``i`` ejected to the galactic medium as element ``j``, for a complete range of stellar masses, accounting for supernovae of types ``Ia`` and ``II``. You can read more about the ``Matrices Q formalism`` in ``Ferrini et al. 1992``.

Starmatrix computes the contribution matrix of 15 elements:

= = === === = === = = ==== == == == = == ==
H D He3 He4 C C13 N O n.r. Ne Mg Si S Ca Fe
= = === === = === = = ==== == == == = == ==

Starmatrix is a tool for astronomers working with galactic chemical evolution models needing detailed datasets to use as input, wanting to compare the validity of different yield sets or assessing different nucleosynthesis modeling assumptions.

Installation
============

The easiest way to install the package is using pip::

    $ pip install starmatrix

This will install the most recent release version and also some dependencies if they are not found in the system: *numpy*, *scipy* and *pyyaml*

A previous installation can be upgraded to the latest version with::

    $ pip install --upgrade starmatrix

Edge
----

If you want to play with the latest code present in this repository even if it has not been released yet, you can do it by cloning the repo locally and instructing pip to install it::

    $ git clone https://github.com/xuanxu/starmatrix.git
    $ cd starmatrix
    $ pip install -e .

Python >= 3.7 is required.

Test installation
-----------------

To test installation worked you can just run Starmatrix with default values running::

    $ starmatrix --generate-config
    $ starmatrix --config config-example.yml

The first command will generate a basic configuration file (named ``config-example.yml``) and the second command will run Starmatrix using that configuration. A folder named ``results`` should be created with the output files.

Test suite
==========

Starmatrix includes a test suite located in the ``/src/starmatrix/tests`` directory. The current state of the build is `publicly tracked by GitHub CI`_. You can run the latest tests locally and get information on code coverage if you clone the code to your local machine, install its development dependencies and use ``pytest``::

    $ git clone https://github.com/xuanxu/starmatrix.git
    $ cd starmatrix
    $ pip install -e ".[dev]"
    $ pytest

.. _`publicly tracked by GitHub CI`: https://github.com/xuanxu/starmatrix/actions/workflows/tests.yml

Usage
=====

Use starmatrix running::

    $ starmatrix --config FILENAME

where *FILENAME* is the path to the config yaml file.

Running starmatrix will produce a directory with three output files:

* **mass_intervals**: all the mass intervals used to integrate for all the mass range
* **imf_supernova_rates**: the initial mass functions for the supernova rates for each mass interval
* **qm-matrices**: the Q(m) matrices for every mass interval defined in the *mass_intervals* file, expressed as stellar mass fractions.

You can find the complete documentation at `ReadTheDocs' Starmatrix page`_.

.. _`ReadTheDocs' Starmatrix page`: https://starmatrix.readthedocs.io/

Input params
============

Starmatrix reads a config file where several options can be set in yaml format::

        z: 0.0200               # metallicity
        sol_ab: as09            # solar abundances
        imf: kroupa2002         # initial mass function (IMF)
        imf_m_low: 0.15         # lower mass limit for the IMF
        imf_m_up: 100           # upper mass limit for the IMF
        total_time_steps: 300   # number of time steps (will result in a Q Matrix per step)
        m_min: 0.98             # min value for stellar mass
        m_max: 40               # max value for stellar mass
        binary_fraction: 0.15   # rate of binary stars
        snia_m_max              # Upper mass limit for binaries with SN Ia. Default value: 16 Msun
        dtd_sn: rlp             # delay time distribution for supernovae
        sn_yields: iwa1998      # Dataset for Supernovae yields
        output_dir: results     # Name of the directory where results are written.
        integration_step: logt  # The integration step can be constant in t, constant in log(t), or custom.
        expelled_elements_filename: ejecta.txt  # Filename of ejected data.

Starmatrix will use its internal `default values`_ for all params for which no values are provided.

If you want to use an existent configuration file as template for your own, you can run::

    $ starmatrix --generate-config

That command will create a ``config-example.yml`` file in the current dir containing the default values.

.. _`default values`: https://starmatrix.readthedocs.io/en/latest/configuration.html#default-values

Starmatrix uses solar mass (M*) as the reference unit for all quantities, so internally the upper and lower limits for IMF are expressed in solar masses, Delay Time Distributions are expressed as [Supernovae per Year per M*] and the expelled elements file is expected to express data as expelled mass per solar mass, same as the supernova yields.

Initial mass function
---------------------

The ``imf`` param in the config file can be set to use any of the predefined IMFs from different papers/authors:

:salpeter: Salpeter 1955
:starburst: Starburst 1999 (a Salpeter with mass limits in [1, 120])
:miller_scalo: Miller & Scalo 1979
:ferrini: Ferrini, Palla & Penco 1998
:kroupa2001: Kroupa 2001
:kroupa2002: Kroupa 2002
:chabrier: Chabrier 2003
:maschberger: Maschberger 2012

The default value is ``kroupa2002``. If you want to use your own IMF you can do so subclassing the `IMF class`_.

.. _`IMF class`: https://github.com/xuanxu/starmatrix/blob/main/src/starmatrix/imfs.py#L35-L68

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

.. _`Abundances class`: https://github.com/xuanxu/starmatrix/blob/main/src/starmatrix/abundances.py#L30-L59

Delay Time Distributions
------------------------

The ``dtd_sn`` param in the config file can be set to use any of the available Delay Time Distributions for supernova rates from different papers/authors:

:rlp: Supernova rates from Ruiz-Lapuente et al. (2000)
:maoz: DTD of Type Ia supernovae from Maoz & Graur (2017)
:castrillo: DTD of Type Ia supernovae from Castrillo et al. (2021)
:greggio: DTD of Type Ia supernovae from Greggio, L. (2005)
:chen: DTD of Type Ia supernovae from Chen et al. (2021)
:greggio-CDD04: DTD from model Close DD 0.4 Gyrs from Greggio, L. (2005)
:greggio-CDD1: DTD from model Close DD 1 Gyr from Greggio, L. (2005)
:greggio-WDD04: DTD from model Wide DD 0.4 Gyrs from Greggio, L. (2005)
:greggio-WDD1: DTD from model Wide DD 1 Gyr from Greggio, L. (2005)
:greggio-SDCH: DTD from model SD Chandra from Greggio, L. (2005)
:greggio-SDSCH: DTD from model SD sub-Chandra from Greggio, L. (2005)
:strolger-fit1: Phi function from Strolger et al. (2020) with (ξ, ω, 𝛼) = (10, 600, 220)
:strolger-fit2: Phi function from Strolger et al. (2020) with (ξ, ω, 𝛼) = (110, 1000, 2)
:strolger-fit3: Phi function from Strolger et al. (2020) with (ξ, ω, 𝛼) = (350, 1200, 20)
:strolger-fit4: Phi function from Strolger et al. (2020) with (ξ, ω, 𝛼) = (6000, 6000, -2)
:strolger-fit5: Phi function from Strolger et al. (2020) with (ξ, ω, 𝛼) = (-650, 2200, 1100)
:strolger-optimized: Phi function from Strolger et al. (2020) with (ξ, ω, 𝛼) = (-1518, 51, 50)

Supernovae yields
-----------------

The ``sn_yields`` param in the config file can be set to use any of the available supernova yields datasets from different papers/authors:

:iwa1998: Data from Iwamoto, K. et al., 1999
:sei2013: Data from Seitenzahl et al. 2013
:ln2018-1: Data from Leung & Nomoto 2018, Tables 6/7
:ln2018-2: Data from Leung & Nomoto 2018, Tables 8/9
:ln2018-3: Data from Leung & Nomoto 2018, Tables 10/11
:ln2020: Data from Leung & Nomoto 2020
:br2019-1: Data from Bravo, E. et al., Table 3
:br2019-2: Data from Bravo, E. et al., Table 4
:gro2021-1: Data from Gronow, S. et al., Tables 3/A10 He+Core detonations
:gro2021-2: Data from Gronow, S. et al., Tables 4/A8 He+Core detonations
:mor2018-1: Data from Mori, K. et al., W7
:mor2018-2: Data from Mori, K. et al., WDD2

Contributions
=============

If you find a bug or have a question, please [open an issue in the project's repo](https://github.com/xuanxu/starmatrix/issues).

Contributions are welcome, please read our `contributing guidelines`_.

.. _`contributing guidelines`: https://github.com/xuanxu/starmatrix/blob/main/CONTRIBUTING.md


Citation
========

If you find Starmatrix helpful, please consider citing:

::

   @article{Bazan2022,
      doi = {10.21105/joss.04461},
      url = {https://doi.org/10.21105/joss.04461},
      year = {2022},
      publisher = {The Open Journal},
      volume = {7},
      number = {75},
      pages = {4461},
      author = {Juanjo Bazán and Mercedes Mollá},
      title = {Starmatrix: Modelling nucleosynthesis of galactic chemical elements},
      journal = {Journal of Open Source Software}
   }

License
=======

*Copyright* © Juanjo Bazán, released under the `MIT license`_.

.. _`MIT license`: https://github.com/xuanxu/starmatrix/blob/main/LICENSE

Credits
=======

Starmatrix is built upon a long list of previous works from different authors/papers:

* *Ferrini et al.*, 1992, ApJ, 387, 138
* *Ferrini & Poggiantti*, 1993, ApJ, 410, 44F
* *Portinari, Chiosi & Bressan*, 1998,AA,334,505P
* *Talbot & Arnett*, 1973, ApJ, 186, 51-67
* *Galli et al.*, 1995, ApJ, 443, 536G
* *Mollá et al.*, 2015, MNRAS, 451, 3693-3708
* *Iwamoto et al.*, 1999, ApJS, 125, 439
* *Seitenzahl et al.*, 2013, MNRAS, Volume 429, Issue 2, 1156–1172
* *Matteucci & Greggio*, 1986, A&A, 154, 279M
* *Mollá et al.*, 2017, MNRAS, 468, 305-318
* *Gavilan, Mollá & Buell*, 2006, A&A, 450, 509
* *Raiteri C.M., Villata M. & Navarro J.F.*, 1996, A&A 315, 105-115
* *Ruiz-Lapuente, P., Canal, R.*, 2000, astro.ph..9312R
* *Maoz, D. & Graur, O.*, 2017, ApJ, 848, 25M
* *Castrillo, A. et al.*, 2021, MNRAS  V501, 3, 3122–3136
* *Greggio, L.*, 2005, A&A 441, 1055–1078
* *Leung & Nomoto*, 2018, ApJ, Vol 861, Issue 2, Id 143
* *Leung & Nomoto*, 2020, ApJ, Vol 888, Issue 2, Id 80
* *Bravo, E. et al.*, 2019, MNRAS, 482, Issue 4, 4346–4363
* *Gronow, S. et al.*, 2021, A&A 656, A94
* *Mori, K. et al.*, 2018, ApJ, 863:176
* *Chen, X., Hu, L. & Wang, L.*, 2021, ApJ, 922, 15
* *Strolger et al*, 2020, ApJ, Vol 890, 2. doi: 10.3847/1538-4357/ab6a97
