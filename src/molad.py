"""
New moon computations
"""
import typing
from enum import Enum

from leap_years import leapYear
import duration
import gematria


class YearType(Enum):
    """
    Year types according to פרק ח הלכה ז
    """

    PARTIAL = 1  # חסרה
    ORDINAL = 2  # כסדרה
    FULL = 3  # שלמה


YEAR_TYPES = {
    False: {2: YearType.PARTIAL, 3: YearType.ORDINAL, 4: YearType.FULL},  # פרק ח הלכה ז
    True: {4: YearType.PARTIAL, 5: YearType.ORDINAL, 6: YearType.FULL},  # פרק ח הלכה ח
}


class Months:
    """
    Class for months computations
    """

    @staticmethod
    def _months_in_years_o_n_(end: typing.Union[int, str], begin: int = 1):
        """
        Return number of months from the beginning. O(n) method.

        >>> Months._months_in_years_o_n_(1) # first year is 1
        0
        >>> Months._months_in_years_o_n_(5782)
        71501
        >>> Months._months_in_years_o_n_("ה'תשפב")
        71501
        """
        end = gematria.year_to_num(end)
        months = 0
        for year in range(begin, end):
            months += leapYear.months(year)
        return months

    @staticmethod
    def _months_in_years_o_1_(end: typing.Union[int, str], begin: int = 1):
        """
        Return number of months from the beginning. O(1) method.

        >>> Months._months_in_years_o_1_(1) # first year is 1
        0
        >>> Months._months_in_years_o_1_(5782)
        71501
        >>> Months._months_in_years_o_1_("ה'תשפב")
        71501
        """
        end = gematria.year_to_num(end)
        months = 0
        begin_cycle = leapYear.cycle(begin)
        end_cycle = leapYear.cycle(end)
        first_cycle_end = begin - begin_cycle + 19 + 1
        last_cycle_begin = end - end_cycle + 1
        for year in range(begin, first_cycle_end):
            months += leapYear.months(year)
        cycles = (last_cycle_begin - first_cycle_end) // 19  # may be negative. it's o.k
        months += cycles * leapYear.months_in_cycle()
        for year in range(last_cycle_begin, end):
            months += leapYear.months(year)
        return max(0, months)

    @staticmethod
    def months_till(
        year: typing.Union[int, str], month: typing.Union[int, str], begin=1
    ):
        """
        Count months until specific date(year,month)

        Examples:
            >>> Months.months_till(1, 1)
            0
            >>> Months.months_till(1, 2)
            1
            >>> Months.months_till(2, 1)
            12
            >>> Months.months_till(2, 2)
            13
        """
        year = gematria.year_to_num(year)
        months_in_years = Months._months_in_years_o_1_(year, begin)
        return (
            months_in_years + gematria.month_to_num(leapYear.is_leap(year), month) - 1
        )

    @staticmethod
    def molad(year: typing.Union[int, str], month: typing.Union[int, str]):
        """
        Calculate he mean new moon of a specific month

        Examples:
            >>> Months.molad(1, "תשרי")
            duration(2, 5, 204)
            >>> Months.molad(5782, "ניסן")
            duration(6, 22, 648)
            >>> Months.molad("ה-תשפב", "ניסן")
            duration(6, 22, 648)
            >>> Months.molad(5782, 1)
            duration(3, 5, 497)

        Can be verified vs https://he-date.info/moladcalculateyear.html
        """
        # פרק ו הלכה יד
        months_num = Months.months_till(year, month)
        molad = duration.first_month + duration.sinodal_month * months_num
        molad.trim_weeks()
        return molad

    @staticmethod
    def potpone_rule_1(day: duration):
        """
        rule of לא אדו ראש
        from פרק ז הלכה א

        >>> Months.potpone_rule_1(1)
        (2, True)
        >>> Months.potpone_rule_1(2)
        (2, False)
        """
        fobidden_days = [1, 4, 6]
        if day in fobidden_days:
            return day + 1, True
        return day, False

    @staticmethod
    def potpone_rule_2(molad: duration):
        """
        old molad rule פרק ז הלכה ב

        >>> Months.potpone_rule_2(duration.duration(1, 18, 5))
        (2, True)
        >>> Months.potpone_rule_2(duration.duration(3, 17, 5))
        (3, False)
        """
        if molad.hours >= 18:
            return molad.days + 1, True
        return molad.days, False

    @staticmethod
    def potpone_rule_3(molad: duration, is_leap: bool):
        """
        rule ג"ט ר"ד בשנה פשוטה גרוש
        from פרק ז הלכה ד
        Note : another postpone will be done by rule1 (to Thursday)

        >>> Months.potpone_rule_3(duration.duration(3, 10, 5), False)
        (4, True)
        >>> Months.potpone_rule_3(duration.duration(3, 17, 5), True)
        (3, False)
        """

        if not is_leap and (
            molad.days == 3
            and ((molad.hours == 9 and molad.parts >= 204) or molad.hours > 9)
        ):
            return molad.days + 1, True
        return molad.days, False

    @staticmethod
    def potpone_rule_4(molad: duration, is_former_leap: bool):
        """
        rule בט"ו תקפ"ט אחר עיבור עקור מלשרוש
        from פרק ז הלכה ה

        >>> Months.potpone_rule_4(duration.duration(2, 18, 600), True)
        (3, True)
        >>> Months.potpone_rule_4(duration.duration(1, 3, 2), True)
        (1, False)
        """

        if is_former_leap and (
            molad.days == 2
            and ((molad.hours == 12 + 3 and molad.parts >= 589) or molad.hours > 12 + 3)
        ):
            return molad.days + 1, True
        return molad.days, False

    @staticmethod
    def apply_postpone_rules(
        molad_tishrei: duration, is_former_leap: bool, is_leap: bool
    ):
        """
        Apply postpone rules on first month's molad (תשרי), and get day of month's head ראש חודש

        >>> Months.apply_postpone_rules(duration.duration(1,4,5) ,True, True)
        (2, [True, False, False, False])
        """
        activated = [False] * 4
        months_head, activated[1] = Months.potpone_rule_2(molad_tishrei)
        if not any(activated):
            months_head, activated[2] = Months.potpone_rule_3(molad_tishrei, is_leap)
        if not any(activated):
            months_head, activated[3] = Months.potpone_rule_4(
                molad_tishrei, is_former_leap
            )
        months_head, activated[0] = Months.potpone_rule_1(months_head)

        return months_head, activated

    @staticmethod
    def year_begin_weekday(year: typing.Union[int, str]):
        """
        Apply postpone rules on first month's molad (תשרי), and get day of month's head ראש חודש

        Examples:
            >>> Months.year_begin_weekday(5782)
            (3, [False, False, False, False])
            >>> Months.year_begin_weekday("ה-תשסו")
            (3, [False, False, False, True])
            >>> Months.year_begin_weekday("ה-תשפט")
            (5, [True, False, True, False])
            >>> Months.year_begin_weekday("ה-תשפו")
            (3, [False, True, False, False])
            >>> Months.year_begin_weekday("ה-תשפח")
            (7, [True, False, False, False])

        Verified with https://he-date.info/moladcalculateyear.html
        """
        year = gematria.year_to_num(year)
        is_leap = leapYear.is_leap(year)
        is_former_leap = leapYear.is_leap(year - 1)
        molad = Months.molad(year, 1)
        return Months.apply_postpone_rules(molad, is_former_leap, is_leap)

    @staticmethod
    def year_type(year: typing.Union[int, str]):
        """
        Check the type of the year (חסרה, כסדרה, שלמה)

        Examples:
            >>> Months.year_type(5782)
            <YearType.ORDINAL: 2>
            >>> Months.year_type(5783)
            <YearType.FULL: 3>
            >>> Months.year_type(5784)
            <YearType.PARTIAL: 1>
        """
        year = gematria.year_to_num(year)
        is_leap = leapYear.is_leap(year)
        year_begin_weekday, _ = Months.year_begin_weekday(year)
        next_first_month_head, _ = Months.year_begin_weekday(year + 1)
        days_diff = (next_first_month_head - year_begin_weekday - 1) % 7
        return YEAR_TYPES[is_leap][days_diff]

    @staticmethod
    def months_length(year: typing.Union[int, str]):
        """
        Check months lengths of a year

        according to פרק ח הלכה ה

        Example:
            >>> Months.months_length(5782)
            [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30]
        """
        months_num = leapYear.months(year)
        year_type = Months.year_type(year)
        lengths = ([30, 29] * 7)[:months_num]

        # פרק ח הלכה ו
        if year_type == YearType.FULL:
            lengths[1] = 30
        if year_type == YearType.PARTIAL:
            lengths[2] = 29

        return lengths

    @staticmethod
    def year_days(year: typing.Union[int, str]):
        """
        Number of days in a year

        Example:
            >>> Months.year_days(5780)
            355
            >>> [Months.year_days(y) for y in range(5780,5790)]
            [355, 353, 384, 355, 383, 355, 354, 385, 355, 354]
        """

        return sum(Months.months_length(year))

    @staticmethod
    def weekday(
        year: typing.Union[int, str],
        month: typing.Union[int, str],
        day_month: typing.Union[int, str],
    ):
        """
        Find the weekday of a specific date

        Example:
            >>> Months.weekday(5782, 9, 1)
            1
            >>> Months.weekday(5782, 1, 1)
            3
            >>> Months.weekday(5786, 12, 13)
            4
            >>> Months.weekday("ה-תשלז", "טבת", "ז")
            3
        """

        # find day of rosh hashana
        year_begin_weekday, _ = Months.year_begin_weekday(year)
        # find days to the begining of the month
        month = gematria.month_to_num(leapYear.is_leap(year), month)
        days_from_year_begin = sum(Months.months_length(year)[: month - 1])
        # days from month begin
        if type(day_month) == str:
            day_month = gematria.str_to_num(day_month)
        days_in_month = day_month - 1
        weekday = (
            year_begin_weekday + days_from_year_begin + days_in_month - 1
        ) % 7 + 1
        return weekday


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
