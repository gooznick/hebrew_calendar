from hdate.angle import angle
from hdate.hdate import HDate
import pytest
from hdate import moon
from hdate import sun
from hdate import molad
import math
import datetime
from hdate import view_arc
import ephem


@pytest.mark.xfail
def test_halacha_1():
    the_day = HDate("ב", "אייר", "ד-תתקלח")
    view_arc_val = view_arc.ViewArc.compute(the_day)
    view_arc_val.round_to_parts()
    assert view_arc_val == angle("יא", "יא")


def test_halacha_1_approx():
    the_day = HDate("ב", "אייר", "ד-תתקלח")
    view_arc_val = view_arc.ViewArc.compute(the_day)
    view_arc_val.round_to_parts()
    assert view_arc_val == angle("יא", "י")
