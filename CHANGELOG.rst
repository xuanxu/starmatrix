.. starmatrix changelog

=========
Changelog
=========

1.4.0 (2021-03-18)
==================
- New supernovae module to add SN yields datasets
- Added ``sn_yields`` setting
- Added SN yields dataset from *Seitenzahl et al. 2013*

1.3.0 (2020-12-09)
==================

- SuperNova rates are now computed accounting for the total number of stars created per unit of stellar mass
- Added new DTD option: Greggio, L. 2005
- Added dataset of solar abundances from Lodders et al. 2019
- Added ``two_steps_t`` option for ``integration_step`` setting: The integration will use two time steps: [half the lifetime of a 100 solar masses star for the given metallicity] as time step for stars bigger than 4 solar masses, and 100 times that for less massive stars. If this option is selected the `total_time_steps` setting is ignored
- Added ``fixed_n_steps`` option for ``integration_step`` setting: The integration will take exactly the number of time steps specified in the next two settings (``integration_steps_stars_smaller_than_4Msun`` and ``integration_steps_stars_bigger_than_4Msun``)
- Removed DTD from *Mannucci, Della Valle, Panagia (2006)* (was deprecated in v1.2.0)
- Deprecation warnings can be silenced setting ``deprecation_warnings`` to False (it is True by default)
- Added correction of abundances data for CRI-LIM yields set
- Element production refactored: removed special case for massive stars
- Updated CNO cycle calculations
- Added ``yield_corrections`` setting to allow custom corrections for the ejections data
- Project renamed to Starmatrix

1.2.0 (2020-03-12)
==================

- Added Supernovae II data to the ``imf_supernova_rates`` file
- Tweak SN total energy function to make it continous
- Better docs
- Added DTD from Maoz & Graur (2017)
- The DTD from Mannucci, Della Valle & Panagia is deprecated
- Added ``matrix_headers`` setting to optionally remove headers from `qm-matrices` file
- The default value for binary systems fraction is now 0.15
- Added ``integration_step`` setting to set the integration step as constant in *log(t)* or in *t*
- Kroupa, Chabrier and Miller-Scalo IMFs have been slightly corrected
- Added ``returned_fractions`` setting to generate a file with the masses restored to the ISM
- Fixed: Maoz & Graur DTD rate corrected by mass
- Added new DTD: Castrillo et al. 2020

1.1.0 (2019-04-22)
==================

New normalization of IMFs
-------------------------

- Added settings to configure IMF's mass limits: ``[imf_m_low, imf_m_up]``
- IMFs are normalized calculating the definite integral in ``[m_low, m_up]``

Minor changes
-------------

- Better ``config-example.yml`` file
- ``Starburst`` IMF, is internally a shortcut for a Salpeter IMF with mass limits in [1, 120]
- Test coverage increased

`All v1.1.0 commits`_

.. _`All v1.1.0 commits`: https://github.com/xuanxu/starmatrix/compare/v1.0.0...v1.1.0

1.0.0 Mercedes Mollá Release - (2019-04-05)
===========================================

New nucleosynthesis method
--------------------------

- Time step is now constant on ``log(t)``
- New settings to add limits on stellar mass: ``[m_min, m_max]``
- Added setting for number of time steps:  ``[total_time_steps]``
- New stellar lifetime method from *Raiteri C.M., Villata M. & Navarro J.F., 1996, A&A 315, 105-115*

New Delay Time Distribution setting
-----------------------------------

- Added setting ``dtd_sn`` to select Delay Time Distribution tu use with supernova rates
- Added DTD from *Mannucci, Della Valle, Panagia (2006)*

Q-Matrix changes
----------------

- Q Matrix values are calculated now without adding a 10e6 factor
- Accuracy increased to ``15.10f``
- Supernova rates are 0.0 for masses > 8 solar masses

New unified integration method
------------------------------

- Supernova rates, IMFs and Q integrals are now resolved with Newton-Cotes degree 6

Bug fixes
---------

- Fixed out-of-limits error ocurring when interpolating to 100 stellar masses
- Fixed over-adding supernova rates to Q matrix in each integration step
- Fixed matrix size when mass was invalid

`All v1.0.0 commits`_

.. _`All v1.0.0 commits`: https://github.com/xuanxu/starmatrix/compare/v0.1.0...v1.0.0

0.1.0 Beatrice Tinsley Release - (2019-03-21)
=============================================

**First beta release**

Q-Matrix generation complete for 15 elements:
---------------------------------------------

H | D | He3 | He4 | C | C13 | N | O | n.r. | Ne | Mg | Si | S | Ca | Fe
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---


**Initial mass functions** included:

keyword | IMF
--- | ---
salpeter | Salpeter 1955
starburst | Starburst 1999
miller_scalo | Miller & Scalo 1979
ferrini | Ferrini, Palla & Penco 1998
kroupa | Kroupa 2002
chabrier | Chabrier 2003
maschberger | Maschberger 2012

**Solar abundances** included:

keyword | Abundances dataset
--- | ---
ag89 | Anders & Grevesse 1989
gs98 | Grevesse & Sauval 1998
as05 | Asplund et al. 2005
as09 | Asplund et al. 2009
he10 | Heger 2010

**Supernova rates** calculation methods included:

keyword | Abundances dataset
--- | ---
matteucci | SN Ia Matteucci
tornambe | SN Ia/Ib Tornambe
rlp | SN Ia Ruiz-Lapuente

