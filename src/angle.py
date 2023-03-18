import gematria


class angle(object):
    """
    Class that represent an angle. פרק יא הלכה ז

    >>> angle(40, 8, 30)
    angle(40, 8, 30, 0.0)
    """

    PARTS = 60  # פרק יא הלכה ז
    DEGREES = 360
    THIRDS_IN_CIRCLE = DEGREES*(PARTS**3)

    def __init__(self, degrees=0, parts=0, seconds=0, thirds=0):
        self._degrees = gematria.str_to_num(degrees)
        self._parts = gematria.str_to_num(parts)  # חלקים
        self._seconds = gematria.str_to_num(seconds)  # שניות
        self._thirds = gematria.str_to_num(thirds)  # שלשיות

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
            ((self._degrees * self.PARTS + self._parts) * self.PARTS + self._seconds) * self.PARTS +
            self._thirds
        )
        if thirds < 0:
            thirds += self.THIRDS_IN_CIRCLE
        self._seconds = int(thirds / self.PARTS)
        self._thirds = thirds - self._seconds * self.PARTS

        self._parts = int(self._seconds / self.PARTS)
        self._seconds = int(self._seconds - self._parts * self.PARTS)

        self._degrees = int(self._parts / self.PARTS)
        self._parts = int(self._parts - self._degrees * self.PARTS)
        self._thirds = float(self._thirds)
        if abs(self._thirds) < 1e-3:
            self._thirds = 0.0

    def remove_circles(self):
        self._degrees %= self.DEGREES
        return self

    def to_degree_in_mazal(self):
        self._degrees = self._degrees % 30

    def to_mazal(self):
        mazal = gematria.degree_to_mazal(self.as_degrees_fraction())
        angle_in_mazal = angle(self.as_degrees_fraction() % 30)
        return mazal, angle_in_mazal

    def remove_thirds(self):
        self._thirds = 0
        return self

    def round_thirds(self):
        self._thirds = round(self._thirds)
        return self

    def round_seconds(self):
        # פרק יג הלכה י
        # ואל תפנה אל השניות
        if self._thirds > self.PARTS//2:
            self._seconds = self._seconds+1
        self._thirds = 0
        self.__normalize()
        return self

    def round_to_parts(self):
        # פרק יג הלכה י
        # ואל תפנה אל השניות
        if self._thirds > self.PARTS//2:
            self._seconds = self._seconds+1
        if self._seconds > self.PARTS//2:
            self._parts = self._parts+1
        self._thirds = 0
        self._seconds = 0
        self.__normalize()
        return self

    def remove_seconds(self):
        self._thirds = 0
        self._seconds = 0
        return self

    def round_parts(self):
        # פרק יג הלכה ט
        self.round_seconds()
        if self._parts > self.PARTS//2:
            self._degrees = self._degrees+1
        self._parts = 0
        self.__normalize()
        return self

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

    def __add__(self, scalar):
        """
        >>> angle(1,2,3) + angle(7,1,2)
        angle(8, 3, 5, 0.0)
        """
        if type(scalar) == angle:
            return angle(
                self._degrees + scalar._degrees,
                self._parts + scalar._parts,
                self._seconds + scalar._seconds,
                self._thirds + scalar._thirds,
            )
        res = angle(self.as_degrees_fraction() + scalar)
        return res

    def __mul__(self, scalar):
        """
        >>> angle(7,1,2) * 10
        angle(70, 10, 20, 0.0)
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
        angle(70, 10, 20, 0.0)
        """
        res = angle(self._degrees, self._parts,
                    self._seconds, self._thirds) * scalar
        return res

    def __gt__(self, other):
        """
        >>> angle(9,1,2) > 10
        False

        >>> angle(7,1,2) > angle(7,1,1)
        True
        """
        if type(other) == angle:
            other = other.as_degrees_fraction()
        return self.as_degrees_fraction() > other

    def __rsub__(self, scalar):
        """
        >>> 10 - angle(7,1,2)
        angle(2, 58, 58, 0.0)
        """
        if type(scalar) == angle:
            scalar = scalar.as_degrees_fraction()
        res = angle(scalar - self.as_degrees_fraction())
        return res

    def __radd__(self, scalar):
        """
        >>> 10 + angle(7,1,2)
        angle(17, 1, 2, 0.0)
        """
        if type(scalar) == angle:
            scalar = scalar.as_degrees_fraction()
        res = angle(scalar + self.as_degrees_fraction())
        return res

    def __sub__(self, scalar):
        """
        >>> angle(17,1,2) - 10
        angle(7, 1, 2, 0.0)
        """
        if type(scalar) == angle:
            return angle(
                self._degrees - scalar._degrees,
                self._parts - scalar._parts,
                self._seconds - scalar._seconds,
                self._thirds - scalar._thirds,
            )
        res = angle(self.as_degrees_fraction() - scalar)
        return res

    def __truediv__(self, scalar):
        """
        >>> angle(70, 10, 20, 0) / 10
        angle(7, 1, 2, 0.0)
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
        if type(other) == float:
            other = angle(other)
        return (
            self._degrees == other._degrees
            and self._parts == other._parts
            and self._seconds == other._seconds
            and self._thirds == other._thirds
        )
