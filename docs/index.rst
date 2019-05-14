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

and rich neutrons isotopes (referred as ``n.r.`` in the code).

.. toctree::
   :maxdepth: 2
   :caption: User guide:

   installation
   usage
   input_params
   testing_edge
   credits


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
* *Mannucci, Della Valle, Panagia*, 2006, MNRAS, 370, 773M


