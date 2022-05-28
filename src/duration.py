import gematria


class duration(object):
    """
    Class that represent a duration with integer parts

    >>> sinodal_month * 12
    duration(354, 8, 876)
    >>> sinodal_month * 13
    duration(383, 21, 589)
    """

    PARTS_PER_HOUR = 1080  # פרק ו הלכה ב
    HOURS_PER_DAY = 24  # פרק ו הלכה ב
    MOMENTS_PER_PART = 76  # פרק י הלכה א

    def __init__(self, days=0, hours=0, parts=0, moments=0):
        self._days = gematria.str_to_num(days)
        self._hours = gematria.str_to_num(hours)
        self._parts = gematria.str_to_num(parts)  # חלקים
        self._moments = gematria.str_to_num(moments)  # רגעים

        self.__normalize()

    def __str__(self):
        if self._moments:
            return f"{self._days} ימים {self._hours} שעות {self._parts} חלקים {self._moments} רגעים"
        else:
            return f"{self._days} ימים {self._parts} שעות ו-{self._hours} חלקים"

    def __repr__(self):
        if self._moments:
            return (
                f"duration({self._days}, {self._hours}, {self._parts}, {self._moments})"
            )
        else:
            return f"duration({self._days}, {self._hours}, {self._parts})"

    def __normalize(self):
        """
        Convert to int within the correct range of each member
        """
        moments = (
            (self._days * self.HOURS_PER_DAY + self._hours) * self.PARTS_PER_HOUR
            + self._parts
        ) * self.MOMENTS_PER_PART + self._moments
        self._parts = int(moments / self.MOMENTS_PER_PART)
        self._moments = moments - self._parts * self.MOMENTS_PER_PART

        self._hours = int(self._parts / self.PARTS_PER_HOUR)
        self._parts = int(self._parts - self._hours * self.PARTS_PER_HOUR)

        self._days = int(self._hours / self.HOURS_PER_DAY)
        self._hours = int(self._hours - self._days * self.HOURS_PER_DAY)

    def trim_weeks(self):
        """
        Remove all weeks (days>7) so that the duration will be within a single week

        >>> duration(15,2).trim_weeks()
        duration(1, 2, 0)
        """
        self._days = self._days % 7
        return self

    def as_days_fraction(self):
        """
        Get the duration in days only

        >>> duration(15,12).as_days_fraction()
        15.5
        """
        return (
            self._days
            + (
                self._hours
                + (self._parts + (self._moments / self.MOMENTS_PER_PART))
                / self.PARTS_PER_HOUR
            )
            / self.HOURS_PER_DAY
        )

    @property
    def days(self):
        return self._days

    @days.setter
    def days(self, d):
        assert type(d) == int
        self._days = d

    @property
    def hours(self):
        return self._hours

    @hours.setter
    def hours(self, h):
        assert type(h) == int
        assert h <= self.HOURS_PER_DAY
        self._hours = h

    @property
    def parts(self):
        return self._parts

    @property
    def minutes(self):
        return (
            (self._parts + (self._moments / self.MOMENTS_PER_PART))
            / self.PARTS_PER_HOUR
            * 60
        )

    @parts.setter
    def parts(self, p):
        assert type(p) == int
        assert p <= self.PARTS_PER_HOUR
        self._parts = p

    @property
    def moments(self):
        return self._moments

    def __add__(self, d):
        """
        >>> duration(1,2,3) + duration(7,1,2)
        duration(8, 3, 5)
        """
        res = duration(
            self._days + d._days,
            self._hours + d._hours,
            self._parts + d._parts,
            self._moments + d._moments,
        )
        return res

    def __sub__(self, d):
        """
        >>> duration(37,4,3) - duration(7,1,2)
        duration(30, 3, 1)
        """
        res = duration(
            self._days - d._days,
            self._hours - d._hours,
            self._parts - d._parts,
            self._moments - d._moments,
        )
        return res

    def __mul__(self, scalar):
        """
        >>> sinodal_month * 12
        duration(354, 8, 876)
        """
        res = duration(
            self._days * scalar,
            self._hours * scalar,
            self._parts * scalar,
            self._moments * scalar,
        )
        return res

    def __rmul__(self, scalar):
        """
        >>> 12 * sinodal_month
        duration(354, 8, 876)
        """
        res = duration(self._days, self._hours, self._parts, self._moments) * scalar
        return res

    def __truediv__(self, scalar):
        """
        >>> duration(100, 24, 2) / 2
        duration(50, 12, 1)
        """
        res = duration(
            self._days / scalar,
            self._hours / scalar,
            self._parts / scalar,
            self._moments / scalar,
        )
        return res

    def __eq__(self, other):
        """
        >>> duration(1,2,3,5) == duration(1,2,3,5)
        True
        """
        return (
            self._days == other._days
            and self._hours == other._hours
            and self._parts == other._parts
            and self._moments == other._moments
        )


sinodal_month = duration(29, 12, 793)  # פרק ו הלכה ד
first_month = duration(2, 5, 204)  # פרק ו הלכה ח
begining_time = duration(0, first_month.hours, first_month.parts)

days_in_sun_year_shmuel = duration(365, 6)  # פרק ט הלכה א
days_in_sun_year_rav_ada = duration(365, 5, "תתקצז", "מח")  # פרק י הלכה א
first_tkufa_diff_rav_ada = duration(0, 9, "תרמ'ב")  # פרק י הלכה ג
first_tkufa_diff_shmuel = duration(7, 9, "תרמ'ב")  # פרק ט הלכה ג

sun_moon_year_diff_in_cycle = duration(0, 1, 485)  # פרק ט הלכה ב
