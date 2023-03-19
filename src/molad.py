"""
New moon computations
"""
import typing
from enum import Enum
import math

from leap_years import leapYear
import duration
import gematria
from hdate import HDate
from datetime import date, timedelta

try:
    import ephem
except ImportError:
    ephem = None


class YearType(Enum):
    """
    Year types according to פרק ח הלכה ז
    """

    PARTIAL = 1  # חסרה
    ORDINAL = 2  # כסדרה
    FULL = 3  # שלמה


YEAR_TYPES = {
    # פרק ח הלכה ז
    False: {2: YearType.PARTIAL, 3: YearType.ORDINAL, 4: YearType.FULL},
    # פרק ח הלכה ח
    True: {4: YearType.PARTIAL, 5: YearType.ORDINAL, 6: YearType.FULL},
}


def to_georgian_BC(hdate: HDate):
    h_first = HDate(25, 12, 0)
    # According to wikipedia, it should be -3760,9,21
    e_first = ephem.Date('-3760/9/22')
    days = Months.days_diff(h_first, hdate)
    return ephem.Date(e_first+days)


def to_georgian(hdate: HDate):
    h_one = HDate("יח", "טבת", "ג-תשסא")
    g_one = date(1, 1, 1)
    days = Months.days_diff(h_one, hdate)
    return g_one+timedelta(days=days)


def from_georgian(gdate: typing.Union[date, ephem.Date]):
    if type(gdate) == date:
        h_one = HDate("יח", "טבת", "ג-תשסא")
        g_one = date(1, 1, 1)
        days = (gdate - g_one).days
        return Months.date_add_days(h_one, days)
    h_first = HDate(25, 12, 0)
    # According to wikipedia, it should be -3760,9,21
    e_first = ephem.Date('-3760/9/22')
    days = int(gdate - e_first)
    return Months.date_add_days(h_first, days)


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
        # may be negative. it's o.k
        cycles = (last_cycle_begin - first_cycle_end) // 19
        months += cycles * leapYear.months_in_cycle()
        for year in range(last_cycle_begin, end):
            months += leapYear.months(year)
        return max(0, months)

    @staticmethod
    def months_till(
        year: typing.Union[int, str], month: typing.Union[int, str] = 1, begin=1
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
            months_in_years +
            gematria.month_to_num(leapYear.is_leap(year), month) - 1
        )

    @staticmethod
    def molad(year: typing.Union[int, str], month: typing.Union[int, str]):

        months_num = Months.months_till(year, month)
        molad = duration.sinodal_month * months_num
        return molad

    @staticmethod
    def molad_day(year: typing.Union[int, str], month: typing.Union[int, str]):
        """
        Calculate the mean new moon of a specific month

        Examples:
            >>> Months.molad_day(1, "תשרי")
            duration(2, 5, 204)
            >>> Months.molad_day(5782, "ניסן")
            duration(6, 22, 648)
            >>> Months.molad_day("ה-תשפב", "ניסן")
            duration(6, 22, 648)
            >>> Months.molad_day(5782, 1)
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
            months_head, activated[2] = Months.potpone_rule_3(
                molad_tishrei, is_leap)
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
        molad = Months.molad_day(year, 1)
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
            [30, 29, 30, 29, 30, 30, 29, 30, 29, 30, 29, 30, 29]
        """
        is_leap = leapYear.is_leap(year)
        year_type = Months.year_type(year)
        lengths = [30, 29] * 6
        if is_leap:
            lengths.insert(5, 30)

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
    def weekday(date: HDate):
        """
        Find the weekday of a specific date

        Example:
            >>> Months.weekday(HDate(1, 9 , 5782))
            2
            >>> Months.weekday(HDate(1, 1, 5782))
            3
            >>> Months.weekday(HDate(13, 12, 5786))
            4
            >>> Months.weekday(HDate("ז", "טבת", "ה'תשלז"))
            3
        """

        # find day of rosh hashana
        year_begin_weekday, _ = Months.year_begin_weekday(date._year)
        # find days to the begining of the month
        days_from_year_begin = sum(
            Months.months_length(date._year)[: date._month - 1])
        # days from month begin
        days_in_month = date._month_day - 1
        weekday = (
            year_begin_weekday + days_from_year_begin + days_in_month - 1
        ) % 7 + 1
        return weekday

    @staticmethod
    def days_diff_o_n_(begin: HDate, end: HDate):
        """
        Compute days diff between two dates

        Examples:
            >>> Months.days_diff_o_n_(HDate(1, 9 , 5782), HDate(1, 9 , 5782))
            0
            >>> Months.days_diff_o_n_(HDate(1, 9 , 5782), HDate(2, 9 , 5782))
            1
            >>> Months.days_diff_o_n_(HDate(1, 9 , 5782), HDate(1, 10 , 5782))
            29
            >>> Months.days_diff_o_n_(HDate(1, 10 , 5782), HDate(1, 11 , 5782))
            30
            >>> Months.days_diff_o_n_(HDate(1, 10 , 5782), HDate(1, 10 , 5783))
            385
            >>> Months.days_diff_o_n_(HDate(1, 10 , 5783), HDate(1, 10 , 5782))
            0

        """

        days = 0
        for year in range(begin._year, end._year):
            days += Months.year_days(year)
        begin_year_months_length = Months.months_length(begin._year)
        days -= sum(begin_year_months_length[: begin._month - 1])
        days -= begin._month_day

        end_year_months_length = Months.months_length(end._year)
        days += sum(end_year_months_length[: end._month - 1])
        days += end._month_day

        return max(0, days)

    @staticmethod
    def _days_to_date(date: HDate):
        """
        Count days between beginging (1,1,1) to a specific date
        """
        # count the days from the begining of the year
        days_from_tishrei = Months.days_diff_o_n_(
            HDate(1, 1, date._year), date)

        # count the duration between first molad and first of Tishrei
        sinodal_months = Months.months_till(date._year, 1)

        sinodal_months_duration = (
            duration.sinodal_month * sinodal_months + duration.begining_time
        )
        _, postpones = Months.year_begin_weekday(date._year)
        return sum(postpones) + sinodal_months_duration._days + days_from_tishrei

    @staticmethod
    def _diff_to_date(days_diff: int):
        """
        Compute the date with specific number of days for the begining (1,1,1)

        Examples:
            >>> Months._diff_to_date(1)
            HDate(2, 1, 1)
            >>> Months._diff_to_date(30) # length of first month
            HDate(1, 2, 1)
            >>> Months._diff_to_date(355) # length of first year
            HDate(1, 1, 2)
        """
        # count the full sinodal months
        sinodal_months = int(
            math.floor(days_diff / duration.sinodal_month.as_days_fraction())
        )

        # count full cycles
        full_cycles = sinodal_months // leapYear.months_in_cycle()

        # find which year are we in
        year = leapYear.CYCLE * full_cycles + 1
        sinodal_months -= full_cycles * leapYear.months_in_cycle()
        while sinodal_months > leapYear.months(year):
            sinodal_months -= leapYear.months(year)
            year += 1

        # days till the begining of the year
        days_until_year_begin = Months.days_diff(
            HDate(1, 1, 1), HDate(1, 1, year))

        return Months.date_add_days_o_n_(
            HDate(1, 1, year), days_diff - days_until_year_begin
        )

    @staticmethod
    def date_add_days(date: HDate, days_add: int):
        """
        Compute the date with specific number of days after given date

        Examples:
            >>> Months.date_add_days_o_n_(HDate(29, 8, 5782), 1)
            HDate(30, 8, 5782)
            >>> Months.date_add_days_o_n_(HDate(29, 8, 5782), 2)
            HDate(1, 9, 5782)
            >>> Months.date_add_days_o_n_(HDate(29, 8, 5782), 32)
            HDate(2, 10, 5782)
            >>> Months.date_add_days_o_n_(HDate(29, 13, 5782), 1)
            HDate(1, 1, 5783)
            >>> Months.date_add_days_o_n_(HDate(29, 13, 5782), 1000)
            HDate(25, 9, 5785)
            >>> Months.date_add_days(HDate(4,5,5700), 600)
            HDate(13, 12, 5701)

        """
        # Count days from the beginging to the date
        days_from_begining_to_date = Months.days_diff(HDate(1, 1, 1), date)

        # Add the given days
        days_from_begining = days_from_begining_to_date + days_add

        # compute date by days from begining
        return Months._diff_to_date(days_from_begining)

    @staticmethod
    def days_diff(begin: HDate, end: HDate):
        """
        Count days between two dates

        Examples:
            >>> Months.days_diff_o_n_(HDate(1, 9 , 5782), HDate(1, 9 , 5782))
            0
            >>> Months.days_diff_o_n_(HDate(1, 9 , 5782), HDate(2, 9 , 5782))
            1
            >>> Months.days_diff_o_n_(HDate(1, 9 , 5782), HDate(1, 10 , 5782))
            29
            >>> Months.days_diff_o_n_(HDate(1, 10 , 5782), HDate(1, 11 , 5782))
            30
            >>> Months.days_diff_o_n_(HDate(1, 10 , 5782), HDate(1, 10 , 5783))
            385
            >>> Months.days_diff_o_n_(HDate(1, 10 , 5783), HDate(1, 10 , 5782))
            0
        """
        return Months._days_to_date(end) - Months._days_to_date(begin)

    @staticmethod
    def date_add_days_o_n_(begin: HDate, days: int):
        """
        Add some days to a date to get a new date

        Examples:
            >>> Months.date_add_days_o_n_(HDate(29, 8, 5782), 1)
            HDate(30, 8, 5782)
            >>> Months.date_add_days_o_n_(HDate(29, 8, 5782), 2)
            HDate(1, 9, 5782)
            >>> Months.date_add_days_o_n_(HDate(29, 8, 5782), 32)
            HDate(2, 10, 5782)
            >>> Months.date_add_days_o_n_(HDate(29, 13, 5782), 1)
            HDate(1, 1, 5783)
            >>> Months.date_add_days_o_n_(HDate(29, 13, 5782), 1000)
            HDate(25, 9, 5785)

        """
        # Count the days in each month on the given date
        months_length = Months.months_length(begin._year)
        while True:
            days_in_begin_month = min(
                months_length[begin._month - 1] - begin._month_day, days
            )
            days -= days_in_begin_month
            begin._month_day += days_in_begin_month

            if not days:
                break

            begin._month_day = 1
            begin._month += 1
            days -= 1

            if begin._month == (len(months_length) + 1):
                begin._year += 1
                begin._month = 1
                months_length = Months.months_length(begin._year)
        return begin

    @staticmethod
    def tkufot_shmuel(year: typing.Union[int, str]):
        """
        Find all 4 tkufot of the year : תשרי, טבת, ניסן, תמוז

        Example :
            >>> Months.tkufot_shmuel(5782)
            [(HDate(1, 2, 5782), 9, 0.0), (HDate(4, 5, 5782), 16, 30.0), (HDate(7, 8, 5782), 0, 0.0), (HDate(9, 11, 5782), 7, 30.0)]

        Note:
            Example verified with "Itim Lebina" calendar
            Not including light saving clock calculations

        """
        return Months._tkufot(
            year,
            duration.first_tkufa_diff_shmuel,
            duration.days_in_sun_year_shmuel,
            hours_only=True,
        )

    @staticmethod
    def tkufot_rav_ada(year: typing.Union[int, str]):
        """
        Find all 4 tkufot of the year : תשרי, טבת, ניסן, תמוז


        Note:
            Example verified with "Itim Lebina" calendar
            Not including light saving clock calculations

        """
        return Months._tkufot(
            year,
            duration.first_tkufa_diff_rav_ada,
            duration.days_in_sun_year_rav_ada,
            hours_only=False,
        )

    @staticmethod
    def _tkufot(year: typing.Union[int, str], first_tkufa, sun_year, hours_only):
        """
        Find all 4 tkufot of the year : תשרי, טבת, ניסן, תמוז
        Internal method to find both shmuel and rav ada's tkufa

        """
        year = gematria.year_to_num(year)

        nissan_first_molad = Months.molad(1, "ניסן")
        nissan_first_tkufa = nissan_first_molad - first_tkufa

        def days_to_tkufa(duration_from_beginning):
            date = Months.date_add_days(
                HDate(1, 1, 1), duration_from_beginning.days)
            return (date, d.hours, d.minutes)

        # tkufa of nissan
        nissans_tkufa_from_begining = sun_year * \
            (year - 1) + nissan_first_tkufa
        if hours_only:
            nissans_tkufa_from_begining = duration.duration(
                nissans_tkufa_from_begining.days, nissans_tkufa_from_begining.hours
            )
        tkufa_duration = sun_year / 4
        tishrey_tkufa_from_begining = nissans_tkufa_from_begining - tkufa_duration * 3
        d = tishrey_tkufa_from_begining
        tkufot_list = []
        for _ in range(4):
            d = d + tkufa_duration
            tkufot_list.append(days_to_tkufa(d))
        return tkufot_list
