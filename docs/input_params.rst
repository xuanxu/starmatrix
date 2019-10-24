
Input params
============

Intergalactic reads a config file where several options can be set in yaml format::

        z: 0.0200               # metallicity
        sol_ab: ag89            # solar abundances
        imf: kroupa             # initial mass function (IMF)
        imf_m_low: 0.15         # lower mass limit for the IMF
        imf_m_up: 100           # upper mass limit for the IMF
        total_time_steps: 300   # number of time steps (will result in a Q Matrix per step)
        m_min: 0.98             # min value for stellar mass
        m_max: 40               # max value for stellar mass
        binary_fraction: 0.15   # rate of binary stars
        dtd_sn: rlp             # delay time distribution for supernovas

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

.. _`IMF class`: https://github.com/xuanxu/intergalactic/blob/master/src/intergalactic/imfs.py#L20-L40

The IMF will be normalized integrating in the ``[imf_m_low, imf_m_up]`` mass interval
(default: ``[0.15, 100]``, except ``Starburst``: ``[1, 120]``).

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

:rlp: Supernova rates from Ruiz-Lapuente et al. 2000
:maoz: The DTD of Type Ia supernovae from Maoz & Graur (2017)
:mdvp: DTD from Mannucci, Della Valle, Panagia 2006
