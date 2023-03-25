import sun
import gematria
from angle import angle
from hdate import HDate
import pytest
import molad


def test_halacha_1():
    assert (sun.location_coefs["v"] * 10).remove_thirds().remove_circles() == angle(
        9, 51, 23
    )
    assert (sun.location_coefs["v"] * 100).remove_thirds().remove_circles() == angle(
        98, 33, 53
    )
    assert (sun.location_coefs["v"] * 1000).remove_thirds().remove_circles() == angle(
        "רסה", "לח", "נ"
    )
    assert (sun.location_coefs["v"] * 10000).remove_thirds().remove_circles() == angle(
        "קלו", "כח", "כ"
    )
    assert (sun.location_coefs["v"] * 29).remove_thirds().remove_circles() == angle(
        "כח", "לה", 1
    )


def test_halacha_2():
    assert (sun.aphelion_coefs["v"] * 10).remove_circles() == angle(0, 0, 1, "ל")
    assert (sun.aphelion_coefs["v"] * 100).remove_circles() == angle(0, 0, "טו")
    assert (sun.aphelion_coefs["v"] * 1000).remove_circles() == angle(0, 2, 30)
    assert (sun.aphelion_coefs["v"] * 10000).remove_circles() == angle(0, 25)
    assert (sun.aphelion_coefs["v"] * 29).remove_thirds().remove_circles() == angle(
        0, 0, 4
    )
    assert (sun.aphelion_coefs["v"] * 354).remove_thirds().remove_circles() == angle(
        0, 0, "נג"
    )

    assert molad.Months.weekday(sun.location_coefs["t0"]) == 5
    beginning_year = sun.location_coefs["t0"]._year
    wanted_date = HDate("יד", "תמוז", beginning_year)

    assert 100 == molad.Months.days_diff(sun.location_coefs["t0"], wanted_date)
    location = sun.Sun.mean_location(wanted_date)
    assert location == angle(105, "לז", "כה")

    assert gematria.degree_to_mazal(location.degrees) == "סרטן"


table = [
    #   Date , days since hs_beginning, location, aphelion
    (HDate("יג", "כסלו", "ה-תשנג"), 71, 256.668, 102.832),
    (HDate("טו", "ניסן", "ה-תשנג"), 190, 13.960, 102.837),
    (
        HDate("יא", "סיון", "ה-תשנד"),
        600,
        58.076,
        102.854,
    ),  # it's י in the original book
    (HDate("ה", "חשון", "ה-תשנג"), 34, 220.199, 102.831),  # it's ד in the original book
]


@pytest.mark.parametrize("date, since_beg, location, aphelion", table)
def test_hazon_shamaim(date, since_beg, location, aphelion):
    assert since_beg == molad.Months.days_diff(sun.hs_location_coefs["t0"], date)
    computed_location = sun.Sun._compute_location_on_day(date, sun.hs_location_coefs)
    assert location == float("%.3f" % computed_location.as_degrees_fraction())
    computed_aphelion = sun.Sun._compute_location_on_day(date, sun.hs_aphelion_coefs)
    assert aphelion == float("%.3f" % computed_aphelion.as_degrees_fraction())


@pytest.mark.xfail
def test_halacha_1_year():
    assert (sun.location_coefs["v"] * 354).remove_thirds().remove_circles() == angle(
        "שמח", "נה", "טו"
    )
