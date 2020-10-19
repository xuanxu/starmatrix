import pytest
import numpy as np
import intergalactic.settings as settings
from intergalactic.dtds import select_dtd
from intergalactic.dtds import dtd_correction
from intergalactic.dtds import dtd_ruiz_lapuente
from intergalactic.dtds import dtd_maoz_graur
from intergalactic.dtds import dtd_castrillo
from intergalactic.dtds import dtd_greggio


@pytest.fixture
def available_dtds():
    """
    Fixture returning the names of all available DTDs defined in settings
    """
    return settings.valid_values["dtd_sn"]


def test_dtds_presence(available_dtds):
    for dtd in available_dtds:
        assert select_dtd(dtd) is not None


def test_select_dtd(available_dtds):
    dtds = [dtd_ruiz_lapuente, dtd_maoz_graur, dtd_castrillo, dtd_greggio]

    for i in range(len(available_dtds)):
        times = [0.001, 9.] + list(np.random.rand(5)) + list(np.random.rand(5) * 9)
        for time in times:
            assert select_dtd(available_dtds[i])(time) == dtds[i](time)


def test_no_negative_time_values():
    t = -1
    assert dtd_ruiz_lapuente(t) == 0.0
    assert dtd_maoz_graur(t) == 0.0


def test_dtd_correction_factor():
    assert dtd_correction({}) == 1.0
    assert dtd_correction({'dtd_correction_factor': 3.0}) == 3.0
