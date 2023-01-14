import gematria
from angle import angle
from hdate import HDate
import pytest
import moon


def test_halacha_2():
    assert (
        (moon.mean_location_coefs["v"]*10).remove_thirds() == angle("קלא", "מה", 50))
    assert (
        (moon.mean_location_coefs["v"]*100).remove_circles() == angle("רלז", "לח", "כג"))
    assert (
        (moon.mean_location_coefs["v"]*1000).remove_circles() == angle("ריו", "כג", "נ"))
    assert (
        (moon.mean_location_coefs["v"]*10000).remove_circles() == angle("ג", "נח", "כ"))
    assert (
        (moon.mean_location_coefs["v"]*29).remove_circles().round_seconds() == angle("כב", 6, "נו"))


print((moon.mean_location_coefs["v"]*354).remove_circles())


@pytest.mark.xfail
def test_halacha_3a():
    assert (
        (moon.mean_path_coefs["v"]*10).remove_thirds() == angle("קל", "לט", 0))


@pytest.mark.xfail
def test_halacha_3b():
    assert (
        (moon.mean_location_coefs["v"]*354).remove_circles() == angle("שמד", "כו", "מג"))


def test_halacha_3():
    assert (
        (moon.mean_path_coefs["v"]*100).remove_circles().remove_thirds() == angle("רכו", "כט", "נג"))
    assert (
        (moon.mean_path_coefs["v"]*1000).remove_circles().remove_thirds() == angle("קד", "נח", 50))
    assert (
        (moon.mean_path_coefs["v"]*10000).remove_circles().remove_thirds() == angle("שכט", "מח", 20))
    assert (
        (moon.mean_path_coefs["v"]*29).round_seconds().remove_circles().remove_thirds() == angle("יח", "נג", "ד"))


@pytest.mark.xfail
def test_halacha_4():
    d1 = angle("יג", 3, "נד")
    d10 = angle("קל", "לט", 0)
    d100 = angle("רכו", "כט", "נג")
    d29 = angle("יח", "נג", "ד")
    expected = angle("שה", "יג", 0)
    assert ((d100*3+d10*5+d1*4) .remove_circles() == expected)
    assert ((d29*12+d1*6) .remove_circles() == expected)
    assert ((moon.mean_path_coefs["v"]*354).remove_circles() == expected)
