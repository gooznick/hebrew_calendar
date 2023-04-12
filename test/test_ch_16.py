from angle import angle
from hdate import HDate
import pytest
import moon
import sun
import molad
import math
import datetime
import ecliptic_lat
import ephem


def test_halacha_2():
    v = ecliptic_lat.moon_plane_coefs["v"]  # מהלך הראש האמצעי ביום אחד
    assert (v.copy().round_seconds() == angle(0, "ג", "יא"))
    assert ((v*100).copy().round_seconds() == angle("ה", "יז", "מג"))
    assert ((v*1000).copy().round_seconds() == angle("נב", "נז", "י"))
    assert ((v*10000).copy().round_seconds().remove_circles()
            == angle("קסט", "לא", "מ"))


@pytest.mark.xfail
def test_halacha_2a():
    v = ecliptic_lat.moon_plane_coefs["v"]  # מהלך הראש האמצעי ביום אחד
    assert ((v*10).copy().round_seconds() == angle(0, "לא", "מז"))
    assert ((v*29).copy().round_seconds() == angle(1, "לב", "ט"))
    assert ((v*354).copy().round_seconds() == angle("יח", "מד", "מב"))


@pytest.mark.xfail
def test_halacha_4():
    the_day = HDate("ב", "אייר", "ד-תתקלח")

    head_location = ecliptic_lat.EclipticLatitude.compute_head_location(
        the_day)
    head_location.round_seconds()
    assert head_location == angle("קעז", "ל", "כג")


def test_halacha_19():
    the_day = HDate("ב", "אייר", "ד-תתקלח")

    is_south, lat = ecliptic_lat.EclipticLatitude.compute(
        the_day)
    assert is_south
    assert lat == angle(3, "נג")


def calc_moon_latitude_ephem(date: HDate):
    gdate = molad.to_georgian(date)
    gdate = datetime.datetime(
        year=gdate.year, month=gdate.month, day=gdate.day-1, hour=18)
    emoon = ephem.Moon()
    emoon.compute(gdate)
    return math.degrees(ephem.Ecliptic(emoon).lat)


def calc_moon_latitude(date: HDate):
    is_south, lat = ecliptic_lat.EclipticLatitude.compute(
        date)
    return lat.as_degrees_fraction() * (-1 if is_south else 1)


def test_sun_moon_velocity():
    t0 = ecliptic_lat.HazonShamaimBeginningDay
    ecliptic_lat.set_hazon_shamaim()

    for x in range(40):
        d0 = molad.Months.date_add_days(t0, x * 10)
        lat0 = calc_moon_latitude(d0)
        lat1 = calc_moon_latitude_ephem(d0)
        assert abs(lat0 - lat1) < .5
