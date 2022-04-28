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

        >>> months.potpone_rule_1(0)
        (1, True)
        >>> months.potpone_rule_1(1)
        (1, False)
        """
        fobidden_days = [d - 1 for d in [1, 4, 6]]  # 0 based...
        if day%7 in fobidden_days:
            return (day+1)%7, True
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
        if molad.hours>=18:
            return molad.days+1, True
        return molad.days, False

    @staticmethod
    def potpone_rule_3(molad: duration, is_leap: bool):
        """
        rule ג"ט ר"ד
        from פרק ז הלכה ד
        Note : two days postpone (to Thursday)

        >>> months.potpone_rule_3(duration.duration(2, 10, 5), False)
        (4, True)
        >>> months.potpone_rule_3(duration.duration(3, 17, 5), True)
        (3, False)
        """

        if not is_leap and (molad.days==2 and ((molad.hours==9 and molad.parts>=204) or molad.hours>9)):
            return molad.days+2, True
        return molad.days, False


    @staticmethod
    def potpone_rule_4(molad: duration, is_former_leap: bool):
        """
        rule בט"ו תקפט
        from פרק ז הלכה ה

        >>> months.potpone_rule_4(duration.duration(1, 3, 600), True)
        (2, True)
        >>> months.potpone_rule_4(duration.duration(1, 3, 2), True)
        (1, False)
        """

        if is_former_leap and (molad.days==1 and ((molad.hours==12+3 and molad.parts>=589) or molad.hours>12+3)):
            return molad.days+1, True
        return molad.days, False

    @staticmethod
    def apply_postpone_rules(molad_tishrei: duration, is_former_leap: bool, is_leap: bool):
        """
        Apply postpone rules on first month's molad (תשרי), and get day of month's head ראש חודש

        >>> months.apply_postpone_rules(duration.duration(0,4,5) ,True, True)
        1
        """
        activated = [False] * 4
        months_head, activated[1] = months.potpone_rule_2(molad_tishrei)
        if not any(activated):
            months_head, activated[2] = months.potpone_rule_3(molad_tishrei, is_leap)
        if not any(activated):
            months_head, activated[3] = months.potpone_rule_4(molad_tishrei, is_former_leap)
        months_head, activated[0] = months.potpone_rule_1(months_head)

        return months_head, activated

    @staticmethod
    def first_month_head(year):
        """
        Apply postpone rules on first month's molad (תשרי), and get day of month's head ראש חודש

        >>> months.first_month_head(5782)
        1
        """
        year = gematria.year_to_num(year)
        is_leap = leapYear.is_leap(year)
        is_former_leap = leapYear.is_leap(year-1)
        molad = months.molad(year, 1)
        return months.apply_postpone_rules(molad, is_former_leap, is_leap)

print(months.first_month_head(5810))
for y in range(5082,7000):
    day, p = months.first_month_head(y)
    if p[3]:
        print (y, day, p)
#6013 2 [False, False, False, True]
#6111 2 [False, False, False, True]