import gematria


class leapYear(object):
    CYCLE = 19
    IS_LEAP = [False] * CYCLE
    for leap in [3, 6, 8, 11, 13, 17, 19]:  # פרק ו הלכה יא
        IS_LEAP[leap % CYCLE] = True  # 0 base...

    @staticmethod
    def is_leap(year):
        """
        >>> leapYear.is_leap(5780)
        False
        >>> leapYear.is_leap(5779)
        True
        >>> leapYear.is_leap("ה'תשפב")
        True
        """
        if type(year) == str:
            year = gematria.gematria(year)
        cycle = year % leapYear.CYCLE
        return leapYear.IS_LEAP[cycle]

    @staticmethod
    def months(year):
        """
        >>> leapYear.months(5780)
        12
        >>> leapYear.months(5779)
        13
        >>> leapYear.months("ה'תשפב")
        13
        """
        if leapYear.is_leap(year):
            return 13
        return 12
