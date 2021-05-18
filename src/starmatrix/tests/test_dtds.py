import pytest
import numpy as np
import starmatrix.settings as settings
from starmatrix.dtds import select_dtd
from starmatrix.dtds import dtd_correction
from starmatrix.dtds import dtd_ruiz_lapuente
from starmatrix.dtds import dtd_maoz_graur
from starmatrix.dtds import dtd_castrillo
from starmatrix.dtds import dtd_greggio
from starmatrix.dtds import dtd_close_dd_04
from starmatrix.dtds import dtd_close_dd_1
from starmatrix.dtds import dtd_wide_dd_04
from starmatrix.dtds import dtd_wide_dd_1
from starmatrix.dtds import dtd_sd_chandra
from starmatrix.dtds import dtd_sd_subchandra
from starmatrix.dtds import dtd_chen


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
    dtds = [dtd_ruiz_lapuente, dtd_maoz_graur, dtd_castrillo, dtd_greggio, dtd_chen,
            dtd_close_dd_04, dtd_close_dd_1, dtd_wide_dd_04, dtd_wide_dd_1, dtd_sd_chandra, dtd_sd_subchandra]

    for i in range(len(available_dtds)):
        times = [0, 0.001, 0.04, 0.1, 0.4, 2, 9.] + list(np.random.rand(5)) + list(np.random.rand(5) * 9)
        for time in times:
            assert select_dtd(available_dtds[i])(time) == dtds[i](time)


def test_no_negative_time_values():
    t = -1
    assert dtd_ruiz_lapuente(t) == 0.0
    assert dtd_maoz_graur(t) == 0.0
    assert dtd_close_dd_04(t) == 0.0
    assert dtd_close_dd_1(t) == 0.0
    assert dtd_wide_dd_04(t) == 0.0
    assert dtd_wide_dd_1(t) == 0.0
    assert dtd_sd_chandra(t) == 0.0
    assert dtd_sd_subchandra(t) == 0.0


def test_dtd_correction_factor():
    assert dtd_correction({}) == 1.0
    assert dtd_correction({'dtd_correction_factor': 3.0}) == 3.0
