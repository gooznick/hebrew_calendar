import gematria


class angle(object):
    """
    Class that represent an angle. פרק יא הלכה ז

    >>> angle(40, 8, 30)
    angle(40, 8, 30, 0)
    """

    PARTS = 60  # פרק יא הלכה ז
    DEGREES = 360
    THIRDS_IN_CIRCLE = DEGREES*(PARTS**3)

    def __init__(self, degrees=0, parts=0, seconds=0, thirds=0):
        self._degrees = gematria.str_to_num(degrees)
        self._parts = gematria.str_to_num(parts)  # חלקים
        self._seconds = gematria.str_to_num(seconds) # שניות
        self._thirds = gematria.str_to_num(thirds) # שלשיות

        self.__normalize()

    def __str__(self):
        return f"שלישיות {self._thirds} שניות {self._seconds} חלקים {self._parts} מעלות {self._degrees}"


    def __repr__(self):
        return (
            f"angle({self._degrees}, {self._parts}, {self._seconds}, {self._thirds})"
        )

    def __normalize(self):
        """
        Convert to int within the correct range of each member
        """
        thirds = (
            ((self._degrees * self.PARTS +self._parts) * self.PARTS + self._seconds) * self.PARTS +
            self._thirds
            )
        thirds = thirds%self.THIRDS_IN_CIRCLE
        self._seconds = int(thirds / self.PARTS)
        self._thirds = int(thirds - self._seconds * self.PARTS)

        self._parts = int(self._seconds / self.PARTS)
        self._seconds = int(self._seconds - self._parts * self.PARTS)

        self._degrees = int(self._parts / self.PARTS)
        self._parts = int(self._parts - self._degrees * self.PARTS)

        self._degrees %= self.DEGREES

    def to_degree_in_mazal(self):
        self._degrees = self._degrees%30

    def as_degrees_fraction(self):
        """
        Get the angle in degrees only

        """
        return (
            self._degrees
            + (
                self._parts
                + (self._seconds + (self._thirds / self.PARTS))
                / self.PARTS
            )
            / self.PARTS
        )

    @property
    def seconds(self):
        return self._seconds

    @property
    def thirds(self):
        return self._thirds

    @property
    def parts(self):
        return self._parts

    @property
    def degrees(self):
        return self._degrees

    def __add__(self, d):
        """
        >>> angle(1,2,3) + angle(7,1,2)
        angle(8, 3, 5, 0)
        """
        res = angle(
            self._degrees + d._degrees,
            self._parts + d._parts,
            self._seconds + d._seconds,
            self._thirds + d._thirds,
        )
        return res

    def __sub__(self, d):
        """
        >>> angle(37,4,3) - angle(7,1,2)
        angle(30, 3, 1, 0)
        """
        res = angle(
            self._degrees - d._degrees,
            self._parts - d._parts,
            self._seconds - d._seconds,
            self._thirds - d._thirds,
        )
        return res

    def __mul__(self, scalar):
        """
        >>> angle(7,1,2) * 10
        angle(70, 10, 20, 0)
        """
        res = angle(
            self._degrees * scalar,
            self._parts * scalar,
            self._seconds * scalar,
            self._thirds * scalar,
        )
        return res

    def __rmul__(self, scalar):
        """
        >>> 10 * angle(7,1,2)
        angle(70, 10, 20, 0)
        """
        res = angle(self._degrees, self._parts, self._seconds, self._thirds) * scalar
        return res

    def __truediv__(self, scalar):
        """
        >>> angle(70, 10, 20, 0) / 10
        angle(7, 1, 2, 0)
        """
        res = angle(
            self._degrees / scalar,
            self._parts / scalar,
            self._seconds / scalar,
            self._thirds / scalar,
        )
        return res

    def __eq__(self, other):
        """
        >>> angle(7, 1, 2, 0) == angle(7, 1, 2)
        True
        """
        return (
            self._degrees == other._degrees
            and self._parts == other._parts
            and self._seconds == other._seconds
            and self._thirds == other._thirds
        )


