from angle import angle
from hdate import HDate
import pytest
import moon
import sun


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


# def test_halacha_5():
#     today = HDate("כט", "שבט", "ה-תשפג")
#     today = HDate("כט", "טבת", "ה-תשפג")
#     today = HDate("כט", "כסלו", "ה-תשפג")
#     for month in ["תשרי", "חשון", "כסלו", "טבת"]:
#         for days in range(1, 30):
#             today = HDate(days, month, "ה-תשפג")
#             print(today)

#             moon_during_sunset = moon.Moon.mean_location_on_sunset(today)
#             sun_at_18 = sun.Sun.location(today)

#             print((0-moon_during_sunset +
#                   sun_at_18).remove_circles().as_degrees_fraction())


# def test_halacha_6():
#     today = HDate("ב", "אייר", "ד-תתקלח")
#     # today = HDate("א", "תשרי", "ה-תשנג")
#     # today = HDate("ג", "ניסן", 4938)
#     print(moon.Moon.mean_path(today))
#     print(moon.Moon.mean_location(today))
