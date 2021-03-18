import pytest
import random
import numpy as np
import starmatrix.supernovae as sn


def test_empty_yields_set_is_all_zeroes():
    empty_set = sn.empty_yields_set()

    assert len(empty_set) > 0
    assert len(empty_set) == len(sn.sn_elements_list)
    for element in sn.sn_elements_list:
        assert element in empty_set.keys()
        assert empty_set[element] == 0


def test_yields_structure():
    dataset = random.sample(["iwa1998", "sei2013"], 1)[0]
    yields = sn.yields(dataset, 0)

    assert len(yields) > 0
    assert len(yields) == len(sn.sn_elements_list)
    for element in sn.sn_elements_list:
        assert element in yields.keys()


def test_yields_from_iwamoto():
    minus1 = sn.yields_from_iwamoto(-1)
    minus0301 = sn.yields_from_iwamoto(-0.301)
    minus001 = sn.yields_from_iwamoto(-0.01)
    plus05 = sn.yields_from_iwamoto(0.5)

    assert minus1 == minus0301
    assert minus0301 != minus001
    assert minus001 == plus05


def test_yields_from_seitenzahl():
    minus2 = sn.yields_from_seitenzahl(-2)
    minus15 = sn.yields_from_seitenzahl(-1.5)
    minus1 = sn.yields_from_seitenzahl(-1)
    minus065 = sn.yields_from_seitenzahl(-0.65)
    minus03 = sn.yields_from_seitenzahl(-0.3)
    minus015 = sn.yields_from_seitenzahl(-0.15)
    minus01 = sn.yields_from_seitenzahl(-0.1)
    plus1 = sn.yields_from_seitenzahl(1)

    assert minus2 == minus15
    assert minus15 != minus1
    assert minus1 == minus065
    assert minus065 != minus03
    assert minus03 == minus015
    assert minus015 != minus01
    assert minus01 == plus1
