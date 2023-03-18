from angle import angle
from hdate import HDate
import pytest
import moon
import sun
import copy


def test_halacha_8():

    the_day = HDate("ב", "אייר", "ד-תתקלח")

    sun_mean_location = sun.Sun.mean_location(the_day)
    sun_mean_location.remove_thirds()
    assert sun_mean_location == angle(35, 38, 33)

    mean_location = moon.Moon.mean_location_on_sunset(the_day)
    mean_location.round_seconds()
    assert mean_location == angle(53, 36, 39)

    mean_path = moon.Moon.mean_path(the_day)
    mean_path.round_seconds()
    assert mean_path == angle(103, 21, 46)

    double_distance = moon.Moon.double_distance(the_day)
    double_distance.round_seconds()
    assert double_distance == angle(35, 56, 11)  # 12 !

    true_path = moon.Moon.true_path(the_day)
    true_path.remove_seconds()
    assert true_path == angle(108, 21)


def test_halacha_9a():

    the_day = HDate("ב", "אייר", "ד-תתקלח")

    true_path_correction = moon.Moon.true_path_correction(the_day)
    true_path_correction.round_to_parts()
    assert true_path_correction == angle(5, 1)

    true_location = moon.Moon.true_location(the_day)
    true_location.round_to_parts()
    assert true_location == angle(48, 36)


def test_halacha_9b():

    the_day = HDate("א", "חשון", "ה-תשנג")

    true_location = moon.Moon.true_location(the_day)
    true_location.round_to_parts()

    assert true_location == angle(237, 35)


def test_truth_molad():
    the_day1 = HDate("כט", "שבט", "ה-תשפג")
    sun_location = sun.Sun.location(the_day1).as_degrees_fraction()
    moon_location = moon.Moon.true_location(the_day1).as_degrees_fraction()
    diff1 = sun_location - moon_location
    print(sun_location - moon_location)
    the_day = copy.copy(the_day1)
    the_day._month_day += 1
    sun_location2 = sun.Sun.location(the_day).as_degrees_fraction()
    moon_location2 = moon.Moon.true_location(the_day).as_degrees_fraction()

    print(sun_location2 - moon_location2)
    diff2 = sun_location2 - moon_location2
    distance_moon_sun_per_hour = (diff1-diff2) / 24
    hours_to_no_distance = diff1/distance_moon_sun_per_hour
    print(hours_to_no_distance)
    # so, the molad is at the_day+18+hours_to_no_distance
    if hours_to_no_distance > 24:
        the_day._month_day += 1
        hours_to_no_distance -= 24

    hours = angle(18+hours_to_no_distance)
    print(the_day1, hours.degrees, ":", hours.parts)
    import pdb
    pdb.set_trace()
