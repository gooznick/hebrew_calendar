from hdate import duration
from hdate import leap_years
from hdate import molad
from hdate import gematria


def test_sun_year_diff():
    """
    Test diff between sun year and moon years on each cycle

    Source : פרק ט הלכה ב
    """
    sun_days_in_cycle = duration.days_in_sun_year_shmuel * leap_years.leapYear.CYCLE
    moon_days_in_cycle = duration.sinodal_month * leap_years.leapYear.months_in_cycle()
    sun_moon_year_diff_in_cycle = sun_days_in_cycle - moon_days_in_cycle
    assert (
        sun_moon_year_diff_in_cycle == duration.sun_moon_year_diff_in_cycle
    )  # פרק ט הלכה ב


def test_tkufa():
    """
    Test duration of a single Tkufa

    Source : פרק ט הלכה ב
    """
    tkufa_duration = duration.days_in_sun_year_shmuel / 4
    assert tkufa_duration == duration.duration(91, 7.5)  # פרק ט הלכה ג


def test_tkufa_time():
    """
    Test time of the tkufos

    Source : פרק ט הלכה ה
    """
    for year in range(5700, 5800):
        tkufot = molad.Months.tkufot_shmuel(year)
        nissan = gematria.tkufa_to_num("ניסן")
        assert tkufot[nissan][2] == 0
        assert tkufot[nissan][1] % 6 == 0

        tamuz = gematria.tkufa_to_num("תמוז")
        assert tkufot[tamuz][1:] in [
            (7, 30.0),
            (1, 30.0),
            (7 + 12, 30.0),
            (1 + 12, 30.0),
        ]

        tishrey = gematria.tkufa_to_num("תשרי")
        assert tkufot[tishrey][1:] in [(9, 0.0), (3, 0.0), (9 + 12, 0.0), (3 + 12, 0.0)]

        tevet = gematria.tkufa_to_num("טבת")
        assert tkufot[tevet][1:] in [
            (10, 30.0),
            (4, 30.0),
            (10 + 12, 30.0),
            (4 + 12, 30.0),
        ]
