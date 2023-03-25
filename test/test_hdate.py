from hdate import HDate
from molad import Months, to_georgian, to_georgian_BC, from_georgian
from datetime import date
import ephem


def test_to_georgian_BC():
    h_today = HDate(26, 6, 5783)
    to_georgian_BC(h_today)


def test_to_georgian():
    h_today = HDate(26, 6, 5783)
    assert date(2023, 3, 19) == to_georgian(h_today)


def test_from_georgian():
    today = date(2023, 3, 19)
    assert HDate(26, 6, 5783) == from_georgian(today)

    today = ephem.Date("2023/3/19")
    assert HDate(26, 6, 5783) == from_georgian(today)


def test_hebrew_vs_georgian():
    h_first = HDate(25, 12, 0)

    # According to wikipedia, it should be -3760,9,21
    #   (It should be something with the 0.5 of the ephem.Date value)
    # g_first = date(-3760, 9, 22) # python's date can evaluate BC
    e_first = ephem.Date("-3760/9/22")
    h_today = HDate(26, 6, 5783)
    g_today = date(2023, 3, 19)
    e_today = ephem.Date("2023/3/19")
    h_diff = Months.days_diff(h_first, h_today)
    e_diff = int(e_today - e_first)
    assert h_diff == e_diff

    h_one = HDate("יח", "טבת", "ג-תשסא")
    g_one = date(1, 1, 1)
    h_diff = Months.days_diff(h_one, h_today)
    g_diff = (g_today - g_one).days
    assert h_diff == g_diff

    h_state = HDate("ה", "אייר", "ה-תשח")
    g_state = date(1948, 5, 14)
    h_diff = Months.days_diff(h_state, h_today)
    h_diff = Months.days_diff(h_state, h_today)
    g_diff = (g_today - g_state).days
    assert h_diff == g_diff

    h_rosh = HDate("א", "תשרי", "ה-תשפג")
    g_rosh = date(2022, 9, 26)
    h_diff = Months.days_diff(h_rosh, h_today)
    g_diff = (g_today - g_rosh).days
    assert h_diff == g_diff
