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

Intergalactic is a Python package for calculating the contributions of chemical elements ejected during the lifetime of stars. Intergalactic generates matrices of elements and its output is based on the *Matrices Q formalism* [@ferrini1992].

Using explicit (and configurable) values for *solar abundances*, *metallicity (z)*, *ejection rates* and *Initial Mass Function (IMF)*, the code calculates matrices `Q(i,j)` of masses of elements `i` ejected to the galactic medium as element `j`, for a complete range of stellar masses, accounting for SuperNovas of types *I* and *II*.

For each mass step Intergalactic computes the contribution matrix of 15 elements:

| H | D | He3 | He4 | C | C13 | N | O | Ne | Mg | Si | S | Ca | Fe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

and rich neutron isotopes.

Calculating the contributions of chemical elements from different stars in several mass ranges is a necessary step for galactic chemical evolution models [@molla2017]. Intergalactic provides detailed datasets to use as input or internal method by these models.

# References
