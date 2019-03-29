.. intergalactic changelog 

=========
Changelog
=========

0.2.0 (unreleased)
==================

New nucleosynthesis method
--------------------------

- Time step is now constant on ``log(t)``
- New settings to add limits on stellar mass: ``[m_min, m_max]``
- Added setting for number of time steps:  ``[total_time_steps]``
- New stellar lifetime method from *Raiteri C.M., Villata M. & Navarro J.F., 1996, A&A 315, 105-115*.

New Delay Time Distribution setting
-----------------------------------

- Added setting ``dtd_sn`` to select Delay Time Distribution tu use with supernova rates
- Added DTD from *Mannucci, Della Valle, Panagia (2006)*

Bug fixes
---------

- Fixed out-of-limits error ocurring when interpolating to 100 stellar masses


0.1.0 Beatrice Tinsley Release - (2019-03-21)
=============================================

First beta release.
^^^^^^^^^^^^^^^^^^^

Q-Matrix generation complete for 15 elements:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

