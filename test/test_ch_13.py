import sun
import gematria
from angle import angle
from hdate import HDate
import pytest
import molad


def test_halacha_4():
    assert (sun.Sun.rambam_correction(angle(10)) == angle(0, 20))
    assert (sun.Sun.rambam_correction(angle(90)) == angle(1, 59))
    assert (sun.Sun.rambam_correction(angle(100)) == angle(1, 58))


def test_halacha_5():
    assert (sun.Sun.rambam_correction(angle(200)) == angle(0, 42))


def test_halacha_7():
    assert (sun.Sun.rambam_correction(angle(65)) == angle(1, 46))


def test_halacha_8():
    assert (sun.Sun.rambam_correction(angle(67)) == angle(1, 48))


def test_halacha_9_10():

    assert (sun.Sun.rambam_correction(angle(19)) == angle(0, 38))
    wanted_date = HDate("יד", "תמוז", 4938)

    mean_location = sun.Sun.mean_location(wanted_date)
    assert (mean_location == angle("קה", "לז", "כה"))

    aphelion = sun.Sun.aphelion(wanted_date)
    assert (aphelion == angle("פו", "מה", "כג"))

    location = sun.Sun.location(wanted_date)
    assert (sun.Sun.rambam_correction(angle(19)) == angle(0, 38))
    assert (location == angle("קד", "נט", "כה"))
    mazal, angle_in_mazal = location.to_mazal()
    assert (mazal == "סרטן")
    assert (angle_in_mazal == (angle("טו") - angle(0, 0, "לה")))
