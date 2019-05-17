=============
Intergalactic
=============

**Modelling nucleosynthesis of galactic chemical elements**


.. image:: _static/header.jpg
   :width: 690px
   :align: center

Intergalactic is a Q-Matrix generator.

Based on explicit values for *solar abundances*, *z* and *IMF*, Intergalactic calculates matrices ``Q(i,j)`` of masses of elements ``i`` ejected to the galactic medium as element ``j``, for a complete range of stellar masses, accounting for supernovas of types *I* and *II*.

Intergalactic computes the contribution matrix of 15 elements:

+-+-+---+---+-+---+-+-+--+--+--+-+--+--+
|H|D|He3|He4|C|C13|N|O|Ne|Mg|Si|S|Ca|Fe|
+-+-+---+---+-+---+-+-+--+--+--+-+--+--+

and rich neutron isotopes (referred as ``n.r.`` in the code).

.. toctree::
   :maxdepth: 2
   :caption: User guide:

   installation
   usage
   input_params
   testing_edge
   credits
