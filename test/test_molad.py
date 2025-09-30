from hdate.molad import Months
from hdate.hdate import HDate


def test_days_diff():
    for y in range(1, 100):
        assert Months.days_diff_o_n_(
            HDate(1, 1, 1), HDate(1, 1, y)
        ) == Months.days_diff(HDate(1, 1, 1), HDate(1, 1, y))


def test_date_add_days():
    for d in range(500, 800, 3):
        date = HDate(4, 5, 5700)
        assert Months.date_add_days(
            date, d) == Months.date_add_days_o_n_(date, d)

def test_year_pattern():
    assert Months.year_pattern(5787) == "זשה"

    assert Months.year_pattern(5777) == "בחג"
    assert Months.year_pattern(5778) == "הכז"
    assert Months.year_pattern(5779) == "בשז"
    assert Months.year_pattern(5780) == "בשה"
    assert Months.year_pattern(5781) == "זחא"
    assert Months.year_pattern(5782) == "גכז"
    assert Months.year_pattern(5783) == "בשה"
    assert Months.year_pattern(5784) == "זחג"
    assert Months.year_pattern(5785) == "השא"
    assert Months.year_pattern(5786) == "גכה"
    assert Months.year_pattern(5788) == "זשג"
    assert Months.year_pattern(5789) == "הכז"
    assert Months.year_pattern(5790) == "בחה"


def test_year_type():
    """
    Test year type does not fail on
    """
    for year in range(5000, 6000):
        Months.year_type(year)


def test_months_in_years_o_1_():
    """
    Test computation on months_in_years_o(1) vs o(n) simpler computation
    """
    for begin in range(0, 100):
        for end in range(0, 100):
            assert Months._months_in_years_o_1_(  # pylint: disable=W0212
                end, begin
            ) == Months._months_in_years_o_n_(  # pylint: disable=W0212
                end, begin
            )
