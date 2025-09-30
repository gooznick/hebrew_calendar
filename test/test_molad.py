from hdate.hdate import HDate
from hdate.molad import (
    Months,
    YEARS_PATTERNS,
    YEARS_PATTERNS_LEAP,
    YEARS_PATTERNS_NON_LEAP,
)
from hdate.gematria import MONTHS_LEAP, str_to_num, num_to_str

from collections import Counter
import copy


def test_days_diff():
    for y in range(1, 100):
        assert Months.days_diff_o_n_(
            HDate(1, 1, 1), HDate(1, 1, y)
        ) == Months.days_diff(HDate(1, 1, 1), HDate(1, 1, y))


def test_date_add_days():
    for d in range(500, 800, 3):
        date = HDate(4, 5, 5700)
        assert Months.date_add_days(date, d) == Months.date_add_days_o_n_(date, d)


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


def test_year_patterns():

    patterns = Counter()
    for y in range(4000, 6000):
        pat = Months.year_pattern(y)
        patterns[pat] += 1
        assert pat in YEARS_PATTERNS
    assert len(patterns) == 14


def test_find_possible_weekday_per_date():
    month_days = [30, 29, 29, 29, 30, 29, 0, 0, 30, 29, 30, 29, 30, 29]
    dates = {}

    def update_dates(dates, months, current_day):
        for month, days in enumerate(months):
            for day in range(days):
                val = dates.setdefault((month, day), set())
                val.add(current_day % 7)
                current_day = current_day + 1

    for pattern in YEARS_PATTERNS_NON_LEAP:
        specific_month_days = copy.copy(month_days)
        if pattern[1] == "ש":
            specific_month_days[1] += 1
            specific_month_days[2] += 1
        elif pattern[1] == "כ":
            specific_month_days[2] += 1

        update_dates(dates, specific_month_days, str_to_num(pattern[0]))
    month_days = [30, 29, 29, 29, 30, 0, 29, 30, 30, 29, 30, 29, 30, 29]
    for pattern in YEARS_PATTERNS_LEAP:
        specific_month_days = copy.copy(month_days)
        if pattern[1] == "ש":
            specific_month_days[1] += 1
            specific_month_days[2] += 1
        elif pattern[1] == "כ":
            specific_month_days[2] += 1
        update_dates(dates, specific_month_days, str_to_num(pattern[0]))
    months_names = copy.copy(MONTHS_LEAP)
    months_names.insert(5, "אדר")
    months_names[6] = "אדר א'"

    # TODO: move to doc
    for k, v in dates.items():
        print(f"{num_to_str(k[1]+1)[::-1]} {months_names[k[0]]}"[::-1])
        print("".join([num_to_str(vv if vv != 0 else 7) for vv in v][::-1]))


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
