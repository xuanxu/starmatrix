import pytest
import intergalactic.functions as functions
from intergalactic.imfs import Chabrier, Ferrini, Salpeter, Kroupa, MillerScalo, Maschberger, Starburst
from intergalactic.abundances import AndersGrevesse1989, GrevesseSauval1998, Asplund2005, Asplund2009, Heger2010

def test_select_imf():
    strings = ["salpeter", "chabrier", "ferrini", "kroupa", "miller_scalo", "starburst", "maschberger"]
    classes = [Salpeter, Chabrier, Ferrini, Kroupa, MillerScalo, Starburst, Maschberger]

    for i in range(len(strings)):
        imf_instance = functions.select_imf(strings[i])
        assert type(imf_instance) == classes[i]

def test_select_abundances():
    strings = ["ag89", "gs98", "as05", "as09", "he10"]
    classes = [AndersGrevesse1989, GrevesseSauval1998, Asplund2005, Asplund2009, Heger2010]

    for i in range(len(strings)):
        abundance_instance = functions.select_abundances(strings[i], 0.033)
        assert type(abundance_instance) == classes[i]
        assert abundance_instance.z == 0.033
