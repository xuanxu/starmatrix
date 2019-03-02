# Intergalactic

Intergalactic is a Q-Matrix generator.

Based on explicit values for solar abundances, z and IMF, Intergalactic calculates matrices Q(i,j) of masses of elements i ejected to the galactic medium as element j, for a complete range of stellar masses, accounting for supernovas of types Ia and Ib.

_Current status of the project: alpha_

It computes the contribution matrix of 15 elements:

* H
* D
* He3
* He4
* C
* C13
* N
* O
* n.r.
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
  z: 0.0200               # metallicity
  sol_ab: ag89            # solar abundances
  imf: kroupa             # initial mass function
  m_max: 40               # max value for stellar mass
  binary_fraction: 0.05   # rate of binary stars
  sn_ia_selection: rpl    # supernova imf
```

## Credits

Intergalactic is built upon a long list of previous works from different authors/papers, some of those are:

__Evolution models:__

Ferrini,1992,ApJ,387,138

Portinari,1998,AA,334,505

Renzini (1980)

Mercedes Mollá

Marta Gavilán


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


__Supernovae contributions__

Iwamoto, K. et al. 1999 ApJ 125, 439

Ferrini, F., Poggianti, B. 1993 ApJ 410, 44

Matteucci

Tornambe

Ruiz-Lapuente

Kobayashi 09


## License

Copyright © 2019 Juanjo Bazán, released under the [MIT license](MIT-LICENSE.txt)
