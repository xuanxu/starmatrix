# Intergalactic

Intergalactic is a model for chemical evolution of galaxies. 
It computes the contribution matrix of 15 elements:

* H
* D
* He3
* He4
* C
* C13
* N
* O
* Ne
* Mg
* Si
* S
* Ca
* Fe

## Input params:

Intergalactic reads an initial params file where several options must be set:

```yaml
input_params: 
  z: 0.0200
  lim_yields: GAV
  massive_yields: CLI
  sol_ab: ag89
  fe_coef: 1
  imf: 2002
  imf_m_up: 40
  alpha_bin_stars: 0.05
  sn_ia_selection: 3
``` 

## Credits

Intergalactic is built upon a long list of previous works from different authors/papers, some of those are:

__Evolution models:__
Ferrini,1992,ApJ,387,138
Portinari,1998,AA,334,505
Renzini (1980)
Mercedes mollá 
Marta gavilán 

__Initial mass functions__
Salpeter, 1955 
Miller, 1979
Ferrini, 1998
Starburst, 1999
Kroupa, 2002
Chabrier, 2003
Maschberger, 2012

__Solar abundances__
Anders & Grevesse 1989,
Grevesse & Sauval 1998,
Asplund et al. 2005,
Asplund et al. 2009,
Heger 2010

__Supernovas Ia contributions__
Matteucci
Tornambe
Ruiz-Lapuente
Kobayashi 09
