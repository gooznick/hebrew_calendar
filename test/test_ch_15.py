from angle import angle
from hdate import HDate
import pytest
import moon
import sun
import molad
import math
import datetime

import ephem


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

    assert true_location == angle(237, 50)


def test_sun_location():
    d0 = HDate("א", "חשון", "ה-תשנג")
    # d0 = sun.RambamBeginningDay
    # sun.set_hazon_shamaim()
    for x in range(100):
        the_day = molad.Months.date_add_days(d0, x * 10)

        true_location = sun.Sun.location(the_day).as_degrees_fraction()
        gdate = molad.to_georgian(the_day)
        esun = ephem.Sun()
        esun.compute(gdate)
        ecliptic_sun_longitude = math.degrees(ephem.Ecliptic(esun).lon)
        diff = ecliptic_sun_longitude - true_location
        if diff > 180:
            diff = diff - 360
        assert abs(diff) < 0.5


def test_moon_location():
    d0 = HDate("א", "חשון", "ה-תשנג")
    # d0 = sun.RambamBeginningDay
    # sun.set_hazon_shamaim()
    for x in range(100):
        the_day = molad.Months.date_add_days(d0, x * 10)

        true_location = moon.Moon.true_location(the_day).as_degrees_fraction()
        gdate = molad.to_georgian(the_day)
        if gdate.day == 1:
            continue
        gdate = datetime.datetime(
            year=gdate.year, month=gdate.month, day=gdate.day-1, hour=18)
        emoon = ephem.Moon()
        emoon.compute(gdate)
        ecliptic_moon_longitude = math.degrees(ephem.Ecliptic(emoon).lon)
        diff = abs(ecliptic_moon_longitude - true_location)
        if diff > 180:
            diff = diff - 360
        assert diff < 3.2


def calc_sun_location(date: HDate):
    return sun.Sun.location(date).as_degrees_fraction()


def calc_sun_location_ephem(date: HDate):
    gdate = molad.to_georgian(date)
    esun = ephem.Sun()
    esun.compute(gdate)
    return math.degrees(ephem.Ecliptic(esun).lon)


def calc_moon_location(date: HDate):
    return moon.Moon.true_location(date).as_degrees_fraction()


def calc_moon_location_ephem(date: HDate):
    gdate = molad.to_georgian(date)
    gdate = datetime.datetime(
        year=gdate.year, month=gdate.month, day=gdate.day-1, hour=18)
    emoon = ephem.Moon()
    emoon.compute(gdate)
    return math.degrees(ephem.Ecliptic(emoon).lon)


def test_sun_moon_velocity():
    t0 = sun.RambamBeginningDay

    for x in range(40):
        d0 = molad.Months.date_add_days(t0, x * 10)
        d1 = molad.Months.date_add_days(t0, x * 10 + 1)
        sun_location0 = sun.Sun.location(d0).as_degrees_fraction()
        sun_location1 = sun.Sun.location(d1).as_degrees_fraction()
        if sun_location0 > 180 and sun_location1 < 180:
            sun_location1 += 360
        assert abs(sun_location0 - sun_location1) < 1.3
        assert abs(sun_location0 - sun_location1) > 0.7

        moon_location0 = moon.Moon.true_location(d0).as_degrees_fraction()
        moon_location1 = moon.Moon.true_location(d1).as_degrees_fraction()
        if moon_location0 > 180 and moon_location1 < 180:
            moon_location1 += 360
        assert abs(moon_location0 - moon_location1) < 16
        assert abs(moon_location0 - moon_location1) > 10


def truth_molad(month, year):

    the_day = HDate("א", month, year)
    day_before = molad.Months.date_add_days(the_day, -1)

    # sun.set_hazon_shamaim()
    # moon.set_hazon_shamaim()

    sun_location = calc_sun_location(day_before)
    moon_location = calc_moon_location(day_before)
    diff1 = sun_location - moon_location
    if diff1 < -180:
        diff1 += 360
    if diff1 < 0:
        the_day = day_before
        day_before = molad.Months.date_add_days(the_day, -1)
        sun_location = calc_sun_location(day_before)
        moon_location = calc_moon_location(
            day_before)
        diff1 = sun_location - moon_location
    sun_location2 = calc_sun_location(the_day)
    moon_location2 = calc_moon_location(the_day)
    diff2 = sun_location2 - moon_location2

    distance_moon_sun_per_hour = (diff1 - diff2) / 24
    hours_to_no_distance = diff1 / distance_moon_sun_per_hour

    # so, the molad is at the_day+18+hours_to_no_distance
    day_before._month_day += hours_to_no_distance // 24
    hours_to_no_distance = hours_to_no_distance % 24
    hours = hours_to_no_distance + 18
    if hours > 24:
        hours -= 24
    hours = angle(hours)
    return day_before, (hours.degrees, hours.parts)


def test_truth_molad():
    molads = {
        ("תשרי", "ה-תשפג"): ("ל", 13, 48),
        ("חשון", "ה-תשפג"): ("כט", 00, 57),
        ("כסלו", "ה-תשפג"): ("כט", 12, 16),
        ("טבת", "ה-תשפג"): ("כט", 22, 53),
        ("שבט", "ה-תשפג"): ("כט", 9, 5),
        ("אדר", "ה-תשפג"): ("כט", 19, 23),
        ("ניסן", "ה-תשפג"): ("כט", 7, 12),
        ("איר", "ה-תשפג"): ("כט", 18, 53),
        ("סיון", "ה-תשפג"): ("כט", 7, 37),
        ("תמוז", "ה-תשפג"): ("כט", 21, 31),
        ("אב", "ה-תשפג"): ("כט", 12, 38),
    }
    # convert to HDates
    ground_truths = {}
    for k, v in molads.items():
        key = HDate(1, k[0], k[1])
        ground_truths[key] = v

    year = "ה-תשפג"
    for month in range(1, 13):
        day, (hour, minute) = truth_molad(month, year)
        key = HDate(1, day._month, day._year)

        if key in ground_truths:
            print(day, ground_truths[key][1] - hour)
