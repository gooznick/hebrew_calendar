"""
Class for hebrew date representation
"""
import typing

from leap_years import leapYear
import gematria


class HDate:
    """
    A hebrew date
    """

    def __init__(
        self,
        month_day: typing.Union[int, str],
        month: typing.Union[int, str],
        year: typing.Union[int, str],
    ):
        """
        Init a hebrew date
        """
        self._year = gematria.year_to_num(year)
        self._is_leap = leapYear.is_leap(self._year)
        self._month = gematria.month_to_num(self._is_leap, month)
        self._month_day = gematria.str_to_num(month_day)

    def __str__(self):
        """
        >>> str(HDate(2,1,5783))
        "גפשת'ה תשרי ב"
        """

        return f"{gematria.num_to_year(self._year)} {gematria.num_to_month(self._is_leap, self._month)} {gematria.num_to_str(self._month_day)}"

    def __repr__(self):
        """
        >>> repr(HDate(2,1,5783))
        'HDate(5783, 1, 2)'
        """
        return f"HDate({self._month_day}, {self._month}, {self._year})"

    def __eq__(self, other):
        """
        >>> HDate(1,2,3) == HDate(1,2,3)
        True
        """
        return (
            self._year == other._year
            and self._month == other._month
            and self._month_day == other._month_day
        )