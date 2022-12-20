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
        Compute the mean location of the sun in the beginning of a day
        """
        days = molad.Months.days_diff(BeginningDay, date)
        location = LocationInBeginningDay + OneDayMeanMovement*days

        return location.remove_circles()


OneDayMeanMovement = angle(27*360 + gematria.str_to_num("קלו"),
                           "כח", "כ") / 10000  # פרק יב הלכה א

OneDayAphelionMovement = angle(0, 0, 1, "ל") / 10  # פרק יב הלכה ב

BeginningDay = HDate("ג", "ניסן", "ד-תתקלח")
AphelionInBeginningDay = angle(
    "כו", "מה", 8) + angle(gematria.mazal_to_degree("תאומים"))  # פרק יב הלכה ב
LocationInBeginningDay = angle(7, 3, "לב")   # פרק יב הלכה ב
