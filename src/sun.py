"""
Class for hebrew date representation
"""
import typing

import gematria
from angle import angle
from hdate import HDate
import molad
import math


class Sun:
    """
    Sun movements. Ch. 12,13
    """

    def __init__(
        self,
    ):
        """ """
        pass

    @staticmethod
    def mean_location(date: HDate):
        """
        Compute the mean location of the sun in a specific day
        It may be the location in the beginning of the night,
        or an hour before sunset, or an hour after sunset # פרק יב הלכה ב
        """
        return Sun._compute_location_on_day(date, location_coefs)

    @staticmethod
    def aphelion(date: HDate):
        """
        Compute the aphelion of the sun in a specific day
        It may be the location in the beginning of the night,
        or an hour before sunset, or an hour after sunset # פרק יב הלכה ב
        """
        return Sun._compute_location_on_day(date, aphelion_coefs)

    @staticmethod
    def _compute_location_on_day(date: HDate, coefficients):
        days_since_t0 = molad.Months.days_diff(coefficients["t0"], date)
        location = coefficients["x0"] + coefficients["v"] * days_since_t0
        return location.remove_circles()

    @staticmethod
    def location(date: HDate, correction_func=None):
        """
        Compute the location of the sun in a specific day (ecliptic long of the sun)
        פרק יג הלכה א
        """
        if correction_func == None:
            correction_func = Sun.rambam_correction
        mean_location = Sun.mean_location(date)
        aphelion = Sun.aphelion(date)
        sun_path = aphelion - mean_location

        correction = correction_func(sun_path)
        location = mean_location + correction
        location = location.remove_circles()
        return location

    @staticmethod
    def correction(angle):
        """
        Compute the correction (מנת המסלול)
        פרק יג הלכה ב
        """
        if angle > 180:
            # TODO: this should make inversion of the correction direction
            angle = 360 - angle
        angle = round(angle.as_degrees_fraction())
        assert angle <= 180.0
        assert angle >= 0.0
        angle_rad = angle / 180 * math.pi
        correction = math.atan2(math.sin(angle_rad), (math.cos(angle_rad) + 28.877))
        correction_deg = correction * 180 / math.pi

        return -correction_deg

    @staticmethod
    def rambam_correction(path):
        """
        Compute the correction (מנת המסלול)
        פרק יג הלכה ד-ח
        """
        inv = False
        if path > 180:
            # TODO: this should make inversion of the correction direction
            path = 360 - path
            inv = True
        path = round(path.as_degrees_fraction())
        assert path <= 180.0
        assert path >= 0.0
        correction_values = {
            0: angle(0),
            10: angle(0, 20),
            20: angle(0, 40),
            30: angle(0, 58),
            40: angle(1, 15),
            50: angle(1, 29),
            60: angle(1, 41),
            70: angle(1, 51),
            80: angle(1, 57),
            90: angle(1, 59),
            100: angle(1, 58),
            110: angle(1, 53),
            120: angle(1, 45),
            130: angle(1, 33),
            140: angle(1, 19),
            150: angle(1, 1),
            160: angle(0, 42),
            170: angle(0, 21),
            180: angle(0),
        }

        floor = math.floor(path / 10) * 10
        ceil = math.ceil(path / 10) * 10
        floor_cor = correction_values[floor].as_degrees_fraction()
        ceil_cor = correction_values[ceil].as_degrees_fraction()
        correction_per_degree = (ceil_cor - floor_cor) / 10
        correction = floor_cor + correction_per_degree * (path - floor)
        if inv:
            correction = -correction
        return correction


RambamBeginningDay = HDate("ג", "ניסן", "ד-תתקלח")
location_coefs = {
    "t0": RambamBeginningDay,
    "x0": angle(7, 3, "לב"),
    "v": angle(27 * 360 + gematria.str_to_num("קלו"), "כח", "כ") / 10000,
}  # פרק יב הלכה א
aphelion_coefs = {
    "t0": RambamBeginningDay,
    "x0": angle("כו", "מה", 8) + angle(gematria.mazal_to_degree("תאומים")),
    "v": angle(0, 0, 1, "ל") / 10,
}  # פרק יב הלכה א

HazonShamaimBeginningDay = HDate("א", "תשרי", "ה-תשנג")

hs_location_coefs = {
    "t0": HazonShamaimBeginningDay,
    "x0": angle(186.68737),
    "v": location_coefs["v"],
}  # חזון שמים עמ' מז
hs_aphelion_coefs = {
    "t0": HazonShamaimBeginningDay,
    "x0": angle(102, 49, 44.76),
    "v": aphelion_coefs["v"],
}  # חזזון שמים עמ' מה הערה 6


def set_hazon_shamaim():
    global location_coefs
    global aphelion_coefs
    location_coefs = hs_location_coefs
    aphelion_coefs = hs_aphelion_coefs
