"""
Class for hebrew date representation
"""
import typing

import gematria
from angle import angle
from hdate import HDate
import molad


class Sun:
    """
    Sun movements. Ch. 12..
    """

    def __init__(
        self,
    ):
        """
        """
        pass

    @staticmethod
    def mean_location(date: HDate):
        """
        Compute the mean location of the sun in a specific day
        It may be the location in the beginning of the night, 
        or an hour before sunset, or an hour after sunset # פרק יב הלכה ב
        """
        return Sun.__compute_location_on_day(date, location_coefs)

    @staticmethod
    def aphelion(date: HDate):
        """
        Compute the aphelion of the sun in a specific day
        It may be the location in the beginning of the night, 
        or an hour before sunset, or an hour after sunset # פרק יב הלכה ב
        """
        return Sun.__compute_location_on_day(date, aphelion_coefs)

    @staticmethod
    def __compute_location_on_day(date: HDate, coefficients):
        days_since_t0 = molad.Months.days_diff(coefficients["t0"], date)
        location = coefficients["x0"] + coefficients["v"]*days_since_t0
        return location.remove_circles()

    @staticmethod
    def aphelion(date: HDate):
        """
        Compute the aphelion of the sun in a specific day
        """
        days = molad.Months.days_diff(location["t0"], date)
        location = location["x0"] + location["v"]*days

        return location.remove_circles()


RambamBeginningDay = HDate("ג", "ניסן", "ד-תתקלח")
location_coefs = {"t0": RambamBeginningDay, "x0": angle(7, 3, "לב"), "v": angle(27*360 + gematria.str_to_num("קלו"),
                                                                                "כח", "כ") / 10000}  # פרק יב הלכה א
aphelion_coefs = {"t0": RambamBeginningDay, "x0": angle(
    "כו", "מה", 8) + angle(gematria.mazal_to_degree("תאומים")), "v": angle(0, 0, 1, "ל") / 10}  # פרק יב הלכה א
