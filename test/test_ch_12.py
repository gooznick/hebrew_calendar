import sun
import gematria
from angle import angle
from hdate import HDate
import pytest
import molad


def test_halacha_1():
    assert ((sun.location_coefs["v"] * 10).remove_thirds().remove_circles()
            == angle(9, 51, 23))
    assert ((sun.location_coefs["v"] * 100).remove_thirds().remove_circles()
            == angle(98, 33, 53))
    assert ((sun.location_coefs["v"] * 1000).remove_thirds().remove_circles()
            == angle("רסה", "לח", "נ"))
    assert ((sun.location_coefs["v"] * 10000).remove_thirds().remove_circles()
            == angle("קלו", "כח", "כ"))
    assert ((sun.location_coefs["v"] * 29).remove_thirds().remove_circles()
            == angle("כח", "לה", 1))


def test_halacha_2():
    assert ((sun.aphelion_coefs["v"] * 10).remove_circles()
            == angle(0, 0, 1, "ל"))
    assert ((sun.aphelion_coefs["v"] * 100).remove_circles()
            == angle(0, 0, "טו"))
    assert ((sun.aphelion_coefs["v"] * 1000).remove_circles()
            == angle(0, 2, 30))
    assert ((sun.aphelion_coefs["v"] * 10000).remove_circles()
            == angle(0, 25))
    assert ((sun.aphelion_coefs["v"] * 29).remove_thirds().remove_circles()
            == angle(0, 0, 4))
    assert ((sun.aphelion_coefs["v"] * 354).remove_thirds().remove_circles()
            == angle(0, 0, "נג"))

    assert (molad.Months.weekday(sun.location_coefs["t0"]) == 5)
    beginning_year = sun.location_coefs["t0"]._year
    wanted_date = HDate("יד", "תמוז", beginning_year)

    assert (100 == molad.Months.days_diff(
        sun.location_coefs["t0"], wanted_date))
    location = sun.Sun.mean_location(wanted_date)
    assert (location == angle(105, "לז", "כה"))

    assert (gematria.degree_to_mazal(location.degrees) == "סרטן")


@pytest.mark.xfail
def test_halacha_1_year():
    assert ((sun.location_coefs["v"] * 354).remove_thirds().remove_circles()
            == angle("שמח", "נה", "טו"))
