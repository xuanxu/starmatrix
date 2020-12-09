==========
Starmatrix
==========

**Modelling nucleosynthesis of galactic chemical elements**


.. image:: _static/header.jpg
   :width: 690px
   :align: center

Starmatrix is a Q-Matrix generator.

Based on explicit values for *solar abundances*, *z* and *IMF*, Starmatrix calculates matrices ``Q(i,j)`` of masses of elements ``i`` ejected to the galactic medium as element ``j``, for a complete range of stellar masses, accounting for supernovas of types *I* and *II*.

Starmatrix computes the contribution matrix of 15 elements:

+-+-+---+---+-+---+-+-+--+--+--+-+--+--+
|H|D|He3|He4|C|C13|N|O|Ne|Mg|Si|S|Ca|Fe|
+-+-+---+---+-+---+-+-+--+--+--+-+--+--+

and rich neutron isotopes (referred as ``n.r.`` in the code).


**Codebase**

The code for *Starmatrix* is hosted at `GitHub`_ under a MIT license.

.. _`GitHub`: https://github.com/xuanxu/starmatrix

.. toctree::
   :maxdepth: 2
   :caption: User guide:

   installation
   usage
   configuration
   testing_edge
   credits
