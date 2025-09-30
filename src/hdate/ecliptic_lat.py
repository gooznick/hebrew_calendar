from . import gematria
from .angle import angle
from .hdate import HDate
from . import molad
from . import sun
from . import moon

import math


class EclipticLatitude:
    """
    Calculations of Moon's ecliptic latitude. פרק יז
    """

    @staticmethod
    def compute(date: HDate):
        """
        חישוב רוחב הירח
        פרק טז הלכה י

        returns : is_south, latitude
        """
        location = moon.Moon.true_location(date).as_degrees_fraction()
        head = EclipticLatitude.compute_head_location(date).as_degrees_fraction()
        diff = location - head
        corrections = {
            0: angle(0),
            10: angle(0, "נב"),
            20: angle(1, "מג"),
            30: angle(2, "ל"),
            40: angle(3, "יג"),
            50: angle(3, "נ"),
            60: angle(4, "כ"),
            70: angle(4, "מב"),
            80: angle(4, "נה"),
            90: angle(5),
        }
        diff = diff % 360  # positive
        is_south = diff > 180
        if diff > 270:
            diff = 360 - diff
        elif diff > 180:
            diff = diff - 180
        elif diff > 90:
            diff = 180 - diff
        rounded = diff // 10 * 10
        low = corrections[int(rounded)]
        high = corrections[int(rounded) + 10]
        units = diff // 1 - rounded
        result = low + (high - low) * (units / 10)
        return is_south, result

    @staticmethod
    def compute_head_location(date: HDate, coefficients=None):
        """
        חישוב מקום הראש פרק טז הלכה ד
        """
        if coefficients is None:
            coefficients = moon_plane_coefs
        days_since_t0 = molad.Months.days_diff(coefficients["t0"], date)
        location = coefficients["x0"] + coefficients["v"] * days_since_t0
        return (angle(360) - location).remove_circles()


RambamBeginningDay = HDate("ג", "ניסן", "ד-תתקלח")
moon_plane_coefs = {
    "t0": RambamBeginningDay,
    "x0": angle("קפ", "נז", "כח"),  # פרק יז הלכה ב
    # "v": (angle(0, "לא", "מז")/10.0),
    "v": (angle("קסט", "לא", "מ") + angle(360) * 1) / 10000,
}


HazonShamaimBeginningDay = HDate("א", "תשרי", "ה-תשנג")

hs_moon_plane_coefs = {
    "t0": HazonShamaimBeginningDay,
    "x0": angle(93.879638),
    "v": moon_plane_coefs["v"],
}  # חזון שמים עמ' פד


def set_hazon_shamaim():
    global moon_plane_coefs
    moon_plane_coefs = hs_moon_plane_coefs
