import gematria
import typing

class leapYear(object):
    CYCLE = 19
    IS_LEAP = [False] * CYCLE
    for leap in [3, 6, 8, 11, 14, 17, 19]:  # פרק ו הלכה יא
        IS_LEAP[leap-1] = True # 0 based list


    @staticmethod
    def cycle(year: typing.Union[int, str]):
        """
        Get the ordinal number of the year in the 19 leap years cycle

        Examples:
            >>> leapYear.cycle(1)
            1
            >>> leapYear.cycle(19)
            19
            >>> leapYear.cycle(5782)
            6
            >>> leapYear.cycle("ה-תשפב")
            6
        
        Verified with https://he-date.info/moladcalculateyear.html
        """
        return ((gematria.year_to_num(year)-1)%19) + 1

    @staticmethod
    def is_leap(year: typing.Union[int, str]):
        """
        >>> leapYear.is_leap(5780)
        False
        >>> leapYear.is_leap(5779)
        True
        >>> leapYear.is_leap("ה'תשפב")
        True
        """
        cycle = leapYear.cycle(year)
        return leapYear.IS_LEAP[cycle-1]

    @staticmethod
    def months(year: typing.Union[int, str]):
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

    @staticmethod
    def months_in_cycle():
        """
        Get number of months in a full cycle

        >>> leapYear.months_in_cycle()
        235
        """
        return sum([leapYear.months(year) for year in range(1,19+1)])

