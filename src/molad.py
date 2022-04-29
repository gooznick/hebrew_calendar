from leap_years import leapYear
import duration
import gematria
import typing


class months(object):
    @staticmethod
    def _months_in_years_o_n_(end: typing.Union[int, str], begin: int = 1):
        """
        Return number of months from the beginning. O(n) method.

        >>> months._months_in_years_o_n_(1) # first year is 1
        0
        >>> months._months_in_years_o_n_(5782)
        71501
        >>> months._months_in_years_o_n_("ה'תשפב")
        71501
        """
        end = gematria.year_to_num(end)
        months = 0
        for y in range(begin, end):
            months += leapYear.months(y)
        return months

    @staticmethod
    def _months_in_years_o_1_(end: typing.Union[int, str], begin: int = 1):
        """
        Return number of months from the beginning. O(1) method.

        >>> months._months_in_years_o_1_(1) # first year is 1
        0
        >>> months._months_in_years_o_1_(5782)
        71501
        >>> months._months_in_years_o_1_("ה'תשפב")
        71501
        """
        end = gematria.year_to_num(end)
        months = 0
        begin_cycle = leapYear.cycle(begin)
        end_cycle = leapYear.cycle(end)
        first_cycle_end = begin - begin_cycle + 19 + 1
        last_cycle_begin = end - end_cycle + 1
        for y in range(begin, first_cycle_end):
            months += leapYear.months(y)
        cycles = (last_cycle_begin - first_cycle_end) // 19  # may be negative. it's o.k
        months += cycles * leapYear.months_in_cycle()
        for y in range(last_cycle_begin, end):
            months += leapYear.months(y)
        return max(0, months)

    @staticmethod
    def months_till(
        year: typing.Union[int, str], month: typing.Union[int, str], begin=1
    ):
        """
        Count months until specific date(year,month)

        Examples:
            >>> months.months_till(1, 1)
            0
            >>> months.months_till(1, 2)
            1
            >>> months.months_till(2, 1)
            12
            >>> months.months_till(2, 2)
            13
        """
        year = gematria.year_to_num(year)
        months_in_years = months._months_in_years_o_1_(year, begin)
        return (
            months_in_years + gematria.month_to_num(leapYear.is_leap(year), month) - 1
        )

    @staticmethod
    def molad(year: typing.Union[int, str], month: typing.Union[int, str]):
        """
        Calculate he mean new moon of a specific month

        Examples:
            >>> months.molad(1, "תשרי")
            duration(2, 5, 204)
            >>> months.molad(5782, "ניסן")
            duration(6, 22, 648)
            >>> months.molad("ה-תשפב", "ניסן")
            duration(6, 22, 648)
            >>> months.molad(5782, 1)
            duration(3, 5, 497)

        Can be verified vs https://he-date.info/moladcalculateyear.html
        """
        # פרק ו הלכה יד
        months_num = months.months_till(year, month)
        molad = duration.first_month + duration.sinodal_month * months_num
        molad.trim_weeks()
        return molad

    @staticmethod
    def potpone_rule_1(day: duration):
        """
        rule of לא אדו ראש
        from פרק ז הלכה א

        >>> months.potpone_rule_1(1)
        (2, True)
        >>> months.potpone_rule_1(2)
        (2, False)
        """
        fobidden_days = [d for d in [1, 4, 6]]
        if day in fobidden_days:
            return day + 1, True
        return day, False

    @staticmethod
    def potpone_rule_2(molad: duration):
        """
        old molad rule פרק ז הלכה ב

        >>> months.potpone_rule_2(duration.duration(1, 18, 5))
        (2, True)
        >>> months.potpone_rule_2(duration.duration(3, 17, 5))
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

        >>> months.potpone_rule_3(duration.duration(3, 10, 5), False)
        (4, True)
        >>> months.potpone_rule_3(duration.duration(3, 17, 5), True)
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

        >>> months.potpone_rule_4(duration.duration(2, 18, 600), True)
        (3, True)
        >>> months.potpone_rule_4(duration.duration(1, 3, 2), True)
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

        >>> months.apply_postpone_rules(duration.duration(1,4,5) ,True, True)
        (2, [True, False, False, False])
        """
        activated = [False] * 4
        months_head, activated[1] = months.potpone_rule_2(molad_tishrei)
        if not any(activated):
            months_head, activated[2] = months.potpone_rule_3(molad_tishrei, is_leap)
        if not any(activated):
            months_head, activated[3] = months.potpone_rule_4(
                molad_tishrei, is_former_leap
            )
        months_head, activated[0] = months.potpone_rule_1(months_head)

        return months_head, activated

    @staticmethod
    def first_month_head(year: typing.Union[int, str]):
        """
        Apply postpone rules on first month's molad (תשרי), and get day of month's head ראש חודש

        Examples:
            >>> months.first_month_head(5782)
            (3, [False, False, False, False])
            >>> months.first_month_head("ה-תשסו")
            (3, [False, False, False, True])
            >>> months.first_month_head("ה-תשפט")
            (5, [True, False, True, False])
            >>> months.first_month_head("ה-תשפו")
            (3, [False, True, False, False])
            >>> months.first_month_head("ה-תשפח")
            (7, [True, False, False, False])

        Verified with https://he-date.info/moladcalculateyear.html
        """
        year = gematria.year_to_num(year)
        is_leap = leapYear.is_leap(year)
        is_former_leap = leapYear.is_leap(year - 1)
        molad = months.molad(year, 1)
        return months.apply_postpone_rules(molad, is_former_leap, is_leap)


def test_months_in_years_o_1_():
    """
    Test computation on months_in_years_o(1) vs o(n) simpler computation
    """
    for begin in range(0, 100):
        for end in range(0, 100):
            assert months._months_in_years_o_1_(
                end, begin
            ) == months._months_in_years_o_n_(end, begin)
