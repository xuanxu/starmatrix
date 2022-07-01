---
title: 'Starmatrix: Modelling nucleosynthesis of galactic chemical elements'
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
 - name: Departamento de Investigación Básica, CIEMAT, Avda. Complutense 40, E-28040, Madrid, Spain
   index: 1
date: 18 May 2022
bibliography: paper.bib
---

# Summary

`Starmatrix` is a Python package for computing the chemical contribution to the interstellar medium ejected by simple stellar populations (SSPs).

One of the key ingredients of galactic chemical evolution (GCE) models is the nucleosynthetic contribution returned to the interstellar medium by the evolving stellar populations and supernovae. This yields vary depending on the age and metallicity of the stars and are combined following the mass distribution of stars to represent a simple stellar population. Repeating this process adjusting for the the star formation at each time step is one of the main mechanisms of GCE models.

`Starmatrix` reads a single configuration file and calculates the combined contributions of chemical elements ejected to the interstellar medium during the lifetime of stars in the provided mass range. For each mass step an ejections matrix is computed for these fifteen elements: $H$, $D$, $^{3}He$, $^{4}He$, $^{12}C$, $^{16}O$, $^{14}N$, $^{13}C$, $^{20}Ne$, $^{24}Mg$, $^{28}Si$, $^{32}S$, $^{40}Ca$, $^{56}Fe$, and also all neutron-rich CNO isotopes as only one group.

Using explicit (and configurable) values for *solar abundances*, *metallicity (z)*, *ejection rates* and *Initial Mass Function (IMF)*, `Starmatrix` calculates matrices $Q_{ij}$ of masses of elements `i` ejected to the galactic medium as element `j`, integrating for a given range of stellar masses, and accounting for Supernovae (SNe) of types *I* and *II*. Based on the *Matrices Q formalism* [@ferrini1992;@portinari1998], an output file is generated containing matrices linking any ejected species to all its different nucleosynthetic sources.

# Statement of need

Calculating the contributions of chemical elements from different stars in several mass ranges is a necessary step for galactic chemical evolution models [@molla2017]. Usually this is done internally and the chemical yields are convoluted with a star formation history (SFH) inside the model, making it difficult to find reusable opensourced code for calculating the yield for a simple stellar population. The central module in Chempy [@rybizki2017] and the SYGMA module from the NUPYCEE framework [@sygma2018] are exceptions, but being part of bigger codebases they are not available as standalone libraries, not listed in the official Python Package Index and learning how to install and use them is not simple.

`Starmatrix` isolates the SSP yield calculation step as a open source permissively licensed Python implementation, in a modular an flexible way that can be used to provide detailed datasets to be used as input for galactic chemical evolution models, to compare the validity of different yield sets from the literature or to assess different nucleosynthesis modeling assumptions [@bazan2003].

# Features

In order to calculate $Q$ matrices for the whole range of selected stellar masses, the code estimates the stellar lifetime for the minimum and maximum masses and obtains a time interval that is then divided into a fixed number of steps to integrate in. The total time steps can be configured but also the integration step can be forced via settings to be constant in $t$ or in $log(t)$. For each time interval of the integration, the supernova rates are obtained using the corresponding IMF for core-collapse supernovae and a configurable delay time distribution for type Ia supernovae.
Then, the time step is converted back into stellar mass intervals and a $Q$ matrix is calculated for that mass interval weighing it by the selected IMF to create the final output data.

All quantities in the $Q$ matrix are calculated on the base of the ejected mass from stars, using for it the dataset of yields per stellar mass that is entered as input for the code. The code is prepared to include any sets of stellar yields from the literature but if none is declared a default dataset for solar metallicity and with low and intermediate mass star yields from [@gavilan2006] and yields of massive stars from [@chieffi2004] will be used.

![A sample plot using the output data from several `Starmatrix` runs. Lines show true yields `p` of Oxigen using different datasets for low and intermediate mass yields (columns) and for massive stars yields (rows), for a range of metallicity values (bottom horizontal axis) and different IMFs available as Starmatix' settings.\label{fig:oxigen}](sample_plot.png)

Configurable parameters include metallicity, mass range for $Q$ matrices, fraction of binary systems, lower and upper mass limits for the IMF, total time steps for integration and yield correction factors. The code also includes a variety of options for `IMFs`, `solar abundances` data, Supernovae `yields` and `Delay Time Distributions` from the literature to choose from. A complete list of available options can be found in the documentation. To make the code more reusable and to allow it to be integrated in or called by other codebases, Starmatrix defines a base class for each of these parameters to be subclassed if needed so custom options can be easily added programmatically. The code also includes extensive test coverage.

`Starmatrix` depends on `numpy` [@harris2020array] and `scipy` [@scipy2020]. It is released with an open source licence (MIT), available as a public git repository, distributed through the Python Package Index and is easily installable using the standard `pip` package manager.

# References
