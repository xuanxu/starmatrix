import numpy as np
from intergalactic.dtds import select_dtd
from intergalactic.dtds import dtd_ruiz_lapuente
from intergalactic.dtds import dtd_mannucci_della_valle_panagia
from intergalactic.dtds import dtd_sloan_ii_maoz_mannucci_brandt

def test_select_dtd():
    strings = ["rlp", "mdvp", "sloan_ii"]
    dtds = [dtd_ruiz_lapuente, dtd_mannucci_della_valle_panagia, dtd_sloan_ii_maoz_mannucci_brandt]

    for i in range(len(strings)):
        times = [0.001, 9.] + list(np.random.rand(5)) + list(np.random.rand(5) * 9)
        for time in times:
            assert select_dtd(strings[i])(time) == dtds[i](time)

def test_no_negative_time_values():
    t = -1
    assert dtd_ruiz_lapuente(t) == 0.0
    assert dtd_mannucci_della_valle_panagia(t) == 0.0
    assert dtd_sloan_ii_maoz_mannucci_brandt(t) == 0.0
