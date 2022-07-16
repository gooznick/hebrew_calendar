import duration
import leap_years
import molad
import gematria
from hdate import HDate

def test_rav_ada_sun_year_moon_year():
    """
    Test rav ada's sun year vs moon year

    Source : פרק י הלכה א
    """

    sun_year = duration.days_in_sun_year_rav_ada
    moon_year = duration.sinodal_month * 12
    assert (
        sun_year-moon_year  == duration.duration("י", "כא", "קכא", "מח")
    )



def test_rav_ada_sun_year_vs_19_cycle():
    """
    Test rav ada's cycles

    Source : פרק י הלכה א
    """

    sun_days_in_cycle = duration.days_in_sun_year_rav_ada * leap_years.leapYear.CYCLE
    moon_days_in_cycle = duration.sinodal_month * leap_years.leapYear.months_in_cycle()
    assert (
        sun_days_in_cycle == moon_days_in_cycle
    )

def test_rav_ada_tkufa():
    """
    Test rav ada's tkufa time

    Source : פרק י הלכה ב
    """

    rav_adas_tkufa = duration.days_in_sun_year_rav_ada / 4
    assert (
        rav_adas_tkufa == duration.duration("צא", "ז", "תקיט", "לא")
    )

def test_rav_ada_tkufa_in_cycle_begin():
    """
    Test rav ada's tkufa in the beginning of a cycle

    Source : פרק י הלכה ב
    """

    for year in range(1,100,19):
        # rav ada's tkufa in first year of the cycle
        rav_adas_tkufa_of_nissan = molad.Months.tkufot_rav_ada(year)[2]
        tkufa_according_to_molad_of_nissan = molad.Months.molad(year, "ניסן")-duration.first_tkufa_diff_rav_ada
        # convert to date
        date_of_molad_of_nissan = molad.Months.date_add_days(HDate(1, 1, 1), tkufa_according_to_molad_of_nissan.days)

        assert (
            date_of_molad_of_nissan == rav_adas_tkufa_of_nissan[0]
        )
        assert (
            tkufa_according_to_molad_of_nissan.minutes == rav_adas_tkufa_of_nissan[2]
        )
        assert (
            tkufa_according_to_molad_of_nissan.hours == rav_adas_tkufa_of_nissan[1]
        )