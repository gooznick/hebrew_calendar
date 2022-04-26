import math


class duration(object):
    """
    Class that represent a duration with integer parts

    >>> sinodal_month * 12
    duration(354, 8, 876)
    >>> sinodal_month * 13
    duration(383, 21, 589)
    """

    PARTS = 1080
    HOURS = 24

    def __init__(self, days=0, hours=0, parts=0):
        self._days = days
        self._hours = hours
        self._parts = parts  # חלקים

        self.__normalize()

    def __str__(self):
        return f"{self._days} ימים {self._parts} שעות ו-{self._hours} חלקים"

    def __repr__(self):
        return f"duration({self._days}, {self._hours}, {self._parts})"

    def __normalize(self):
        """
        Convert to int within the correct range of each member
        """
        parts = (self._days * self.HOURS + self._hours) * self.PARTS + self._parts
        self._hours = int(parts / self.PARTS)
        self._parts = int(math.fmod(parts, self.PARTS))

        self._days = int(self._hours / self.HOURS)
        self._hours = int(math.fmod(self._hours, self.HOURS))

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
        assert h <= self.HOURS
        self._hours = h

    @property
    def parts(self):
        return self._parts

    @parts.setter
    def parts(self, p):
        assert type(p) == int
        assert p <= self.PARTS
        self._parts = p

    def __add__(self, d):
        """
        >>> duration(1,2,3) + duration(7,1,2)
        duration(8, 3, 5)
        """
        res = duration(
            self._days + d._days, self._hours + d._hours, self._parts + d._parts
        )
        return res

    def __sub__(self, d):
        """
        >>> duration(37,4,3) - duration(7,1,2)
        duration(30, 3, 1)
        """
        res = duration(
            self._days - d._days, self._hours - d._hours, self._parts - d._parts
        )
        return res

    def __mul__(self, scalar):
        """
        >>> sinodal_month * 12
        duration(354, 8, 876)
        """
        res = duration(self._days * scalar, self._hours * scalar, self._parts * scalar)
        return res


sinodal_month = duration(29, 12, 793)
