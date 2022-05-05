

import duration
import leap_years

def test_sun_year_diff():
    """
    Test diff between sun year and moon years on each cycle

    Source : פרק ט הלכה ב
    """
    sun_days_in_cycle = duration.days_in_sun_year_shmuel * leap_years.leapYear.CYCLE
    moon_days_in_cycle = duration.sinodal_month * leap_years.leapYear.months_in_cycle()
    sun_moon_year_diff_in_cycle = sun_days_in_cycle - moon_days_in_cycle
    assert sun_moon_year_diff_in_cycle == duration.sun_moon_year_diff_in_cycle # פרק ט הלכה ב

def test_tkufa():
    """
    Test duration of a single Tkufa

    Source : פרק ט הלכה ב
    """
    tkufa_duration = duration.days_in_sun_year_shmuel / 4
    assert tkufa_duration == duration.duration(91, 7.5) # פרק ט הלכה ג

import gematria
import molad

def tkufa_for_year(year):
    """
    Calculate duration of all 4 tkufut for a year

    Source : 
    """

    # calculate the Tkufa of nissan
    year = gematria.year_to_num(year)
    months = molad.Months.months_till(year)
    diff = (year-1) * duration.days_in_sun_year_shmuel - months * duration.sinodal_month - duration.first_tkufa_diff
    tkufa_of_nissan = molad.Months.molad(year, "ניסן") + diff 
    import pdb;pdb.set_trace()


def test_tkufa_for_year():
    tkufa_for_year(5781)