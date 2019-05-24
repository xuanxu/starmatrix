---
title: 'Intergalactic: Modelling nucleosynthesis of galactic chemical elements'
tags:
  - Astrophysics
  - Galaxies
  - Modelling
  - Python
authors:
 - name: Juanjo Bazán
   orcid: 0000-0001-7699-3983
   affiliation: 1
 - name: Mercedes Mollá
   orcid: 0000-0003-0817-581X
   affiliation: 1
affiliations:
 - name: Departamento de Investigación Básica, CIEMAT, Madrid, Spain
   index: 1
date: 24 May 2019
bibliography: paper.bib
---

# Summary

Intergalactic is a Python package for calculating the combined contributions of chemical elements ejected during the lifetime of stars present in a galaxy.

Using explicit (and configurable) values for *solar abundances*, *metallicity (z)*, *ejection rates* and *Initial Mass Function (IMF)*, the code calculates matrices `Q(i,j)` of masses of elements `i` ejected to the galactic medium as element `j`, integrating for a complete range of stellar masses, and accounting for SuperNovas of types *I* and *II*. So Intergalactic generates matrices of elements: this output is based on the *Matrices Q formalism* [@ferrini1992]. These matrices link any ejected species to all its different nucleosynthetic sources.

For each mass step Intergalactic computes the contribution matrix of 15 elements:

| H | D | He3 | He4 | C | C13 | N | O | Ne | Mg | Si | S | Ca | Fe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

and rich neutron isotopes.

Calculating the contributions of chemical elements from different stars in several mass ranges is a necessary step for galactic chemical evolution models [@molla2017]. Intergalactic provides detailed datasets to use as input or by internal methods in these kind of models.

Intergalactic includes a variety of options for `IMFs`, `solar abundances` data and `Delay Time Distributions` to choose from, but custom options can be easily added programmatically because a base Python Class is included for each of this parameters to be subclassed if needed.



# References
