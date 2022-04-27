from leap_years import leapYear
import duration
import gematria


def _remove_vowels(s):
    """
    Remove vowels from months names, for easier search
    """
    return s.replace("י", "").replace("ו", "").replace("'", "")


def _remove_list_vowels(month_list):
    return [_remove_vowels(m) for m in month_list]


class months(object):
    MONTHS_NO_LEAP = [
        "תשרי",
        "חשון",
        "כסלו",
        "טבת",
        "שבט",
        "אדר",
        "ניסן",
        "אייר",
        "סיון",
        "תמוז",
        "אב",
        "אלול",
    ]
    MONTHS_LEAP = [m for m in MONTHS_NO_LEAP]  # deep copy
    MONTHS_LEAP[5] = "אדר א'"
    MONTHS_LEAP.insert(6, "אדר ב'")

    # Create two more lists, for shortened months, to make it easier to find
    # both "חשוון/חשון" etc.
    MONTHS_NO_LEAP_SHORT = _remove_list_vowels(MONTHS_NO_LEAP)
    MONTHS_LEAP_SHORT = _remove_list_vowels(MONTHS_LEAP)
    MONTHS_SHORT = {True: MONTHS_LEAP_SHORT, False: MONTHS_NO_LEAP_SHORT}

    @staticmethod
    def _ord_month(month_list, month_str):
        return month_list.index(_remove_vowels(month_str))

    @staticmethod
    def _month_to_ord(year, month_str):
        """
        Convert month string to ordered month #, according to leap year
        """
        return months._ord_month(months.MONTHS_SHORT[leapYear.is_leap(year)], month_str)

    @staticmethod
    def month_to_ord(year, month):
        """
        Convert month name or number to ordered number, 0 based.

        >>> months.month_to_ord(5782,12)
        11
        >>> months.month_to_ord(5782,"אדר א")
        5
        >>> months.month_to_ord(5782,"אדר")
        Traceback (most recent call last):
        ...
        ValueError: 'אדר' is not in list
        """
        if type(month) == int:
            return month - 1
        return months._month_to_ord(year, month)

    @staticmethod
    def _months_in_years(year, begin=1):
        """
        Return number of months from the beginning.

        >>> months._months_in_years(0) # first year is 1
        0
        >>> months._months_in_years(5782)
        71514
        >>> months._months_in_years("ה'תשפב")
        71514
        """
        year = gematria.year_to_num(year)
        months = 0
        for y in range(begin, year + 1):
            months += leapYear.months(y)
        return months

    @staticmethod
    def months_till(year, month, begin=1):
        """
        Count months until specific date(year,month)
        """
        year = gematria.year_to_num(year)
        months_in_years = months._months_in_years(year - 1, begin)
        return months_in_years + months.month_to_ord(year, month)

    @staticmethod
    def molad(year, month):
        """
        Calculate he mean new moon of a specific month

        >>> months.molad(5782, "ניסן")
        duration(6, 22, 648)
        >>> months.molad("ה-תשפב", "ניסן")
        duration(6, 22, 648)
        """
        # פרק ו הלכה יד
        months_num = months.months_till(year, month)
        molad = duration.first_month + duration.sinodal_month * months_num
        molad.trim_weeks()
        return molad
