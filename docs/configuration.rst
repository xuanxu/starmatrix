Configuration
=============

Starmatrix reads a configuration file where several input parameters (all of them optional) can be set in yaml format::

        z                 # Metallicity. Default value: 0.02
        sol_ab            # Solar abundances data. Default value: as09
        imf               # Initial Mass function to use. Default value: kroupa
        imf_alpha         # If IMF is salpeter/starburst, this extra param is needed. Defaults to 2.35
        imf_m_low         # Lower limit (in solar masses) for the IMF. Default value: 0.15
        imf_m_up          # Upper limit (in solar masses) for the IMF. Default value: 100
        m_min             # Minimum mass (in solar masses) for the resulting Q-Matrices. Default: 0.98
        m_max             # Maximum mass (in solar masses) for the resulting Q-Matrices. Default: 40.0
        total_time_steps  # Total time steps for integration. Default value: 300
        binary_fraction   # Fraction of binary systems. Default value: 0.15
        dtd_sn            # Delay time distribution to use for Supernovae. Default value: rpl
        sn_yields         # Dataset for Supernovae yields. Default value: iwa1998
        output_dir        # Name of the directory where results are written. Defaults to "results"
        matrix_headers    # Flag to include headers in the qm-matrices file. Default value: yes
        return_fractions  # Flag to calculate R: fraction of mass restored to the ISM. Default: False
        integration_step  # The integration step can be constant in t or in log(t). Default: "logt"
        dtd_correction_factor # Correction for the uncertainty in the DTD integral. Default: 1.0
        deprecation_warnings  # If False Starmatrix won't show deprecation warnings. Default: True
        expelled_elements_filename  # Filename of ejected data. Defaults to an internal file with
                                    # data for z=0.02 from Gavilan et al, 2006, A&A, 450, 509
                                    # and Chieffi & Limongi, 2004, ApJ, 608, 405
        yield_corrections # A map of individual correction factors for items in the ejected data file

Starmatrix will use its internal default values for all params for which no values are provided.

If you want to use an existent configuration file as template for your own, you can run::

    $ starmatrix --generate-config

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

.. _`IMF class`: https://github.com/xuanxu/starmatrix/blob/main/src/starmatrix/imfs.py#L20-L40

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
:lo19: Lodders et al. 2019

The default value is ``as09``. If you want to use your own abundances data you can do so subclassing the `Abundances class`_.

.. _`Abundances class`: https://github.com/xuanxu/starmatrix/blob/main/src/starmatrix/abundances.py#L18-L47

Delay Time Distributions
------------------------

The ``dtd_sn`` param in the config file can be set to use any of the available Delay Time Distributions for supernova rates from different papers/authors:

:rlp: Supernova rates from Ruiz-Lapuente et al. 2000
:maoz: The DTD of Type Ia supernovae from Maoz & Graur (2017)
:castrillo: DTD of Type Ia supernovae from Castrillo et al. (2020)
:greggio: DTD of Type Ia supernovae from Greggio, L. (2005)

Supernovae yields
-----------------

The ``sn_yields`` param in the config file can be set to use any of the available supernova yields datasets from different papers/authors:

:iwa1998: Supernova data from Iwamoto, K. et al., 1999, ApJ 125, 439
:sei2013: Supernova data from Seitenzahl et al. 2013, MNRAS 429, 2, 1156–1172

Integration step
----------------

By default integration steps are constant in `log(t)` but this behavior can be changed via the `integration_step` setting, that can take these values:

:logt: Integration step is constant in `log(t)`, so it is smaller for short-lived stars and gradually increases when time increases (stellar mass decreases).  The total number of steps should be set using the `total_time_steps` setting
:t:    Integration step is constant in `t`. Less efficient than log(t) but can be used to study specific intervals. Should be tuned with the `total_time_steps` setting
:two_steps_t: The integration will use two time steps: [half the lifetime of a 100 solar masses star for the given metallicity] as time step for stars bigger than 4 solar masses, and 100 times that for less massive stars. If this option is selected the `total_time_steps` setting is ignored
:fixed_n_steps: The integration will take exactly the number of time steps specified in the next two settings (`integration_steps_stars_smaller_than_4Msun` and `integration_steps_stars_bigger_than_4Msun`)
:integration_steps_stars_bigger_than_4Msun: integer number of integration time steps for m = 4Msun to m_max. This option is ignored unless `integration_step` value is `fixed_n_steps`
:integration_steps_stars_smaller_than_4Msun: integer number of integration time steps for m = m_min to 4Msun. This option is ignored unless `integration_step` value is `fixed_n_steps`


Ejected data file
-----------------

The ``expelled_elements_filename`` setting should be a valid path of a text file containing data for expelled elements per stellar mass.

**Format:**

The file should include a row of data for each stellar mass.
Structure of each row should be:

* First column: **stellar mass**
* 2nd to 19th columns: expelled mass of element i where i is in the following ordered list

    **H, D, He3, He4, C12, C13, N14primary, n.r., O16, Ne, Mg, Si, S, Ca, Fe, remnants, C13secondary, N14secondary**

This data will be used internally to interpolate/extrapolate values for all the mass range of the model.

Yield corrections
-----------------

Using the ``yield_corrections`` setting you can specify correction factors for the yields contained in the ejected data file.
This setting is a map of **key: value** pairs.
The allowed keys correspond to the elements included in the ejected data file:

**H**, **D**, **He3**, **He4**, **C12**, **C13**, **N14p**, **n.r.**, **O16**, **Ne**, **Mg**, **Si**, **S**, **Ca**, **Fe**, **remnants**, **C13s** and **N14s**

**Example:**

If you want to multiply all magnesium data by 2, and all Sulfur data by 0.87 your settings file should include:

.. code:: yaml

    yield_corrections:
        mg: 2
        s: 0.87

