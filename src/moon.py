
import gematria
from angle import angle
from hdate import HDate
import molad
import sun

import math


class Moon:
    """
    Moon movements. Ch. 14
    """

    @staticmethod
    def mean_location_on_sunset(date: HDate):
        """
        Compute the mean location of the moon during the sunset of a specific day
        אמצע הירח בשעת הראיה, פרק יד הלכה ה
        """
        corrections = {
            (345, 360,): angle(0),  # חצי דגים עד חצי טלה
            (0, 15,): angle(0),
            (15, 60,): angle(0, "טו"),  # חצי טלה עד תאומים
            (60, 120,): angle(0, "ל"),  # תאומים עד אריה
            (120, 165,): angle(0, "טו"),  # אריה עד חצי בתולה
            (165, 195,): angle(0),  # חצי בתולה עד חצי מאזניים
            (195, 240,): 0-angle(0, "טו"),  # חצי מאזניים עד קשת
            (240, 300,): 0-angle(0, "ל"),  # קשת עד דלי
            (300, 345,): 0-angle(0, "טו"),  # דלי עד חצי דגים
        }

        sun_location_deg = sun.Sun.location(
            date).as_degrees_fraction()

        for (min, max), correction in corrections.items():
            if sun_location_deg >= min and sun_location_deg <= max:
                sun_correction = correction
        moon_location = Moon.mean_location(date)

        moon_location += sun_correction
        moon_location = moon_location.remove_circles()
        return moon_location

    @staticmethod
    def true_path_correction(date: HDate):
        """
        מנת המסלול הנכון, פרק ט"ו הלכה ו
        """
        path = Moon.true_path(date)
        if path > 180:
            # TODO: this should make inversion of the correction direction
            path = 360 - path
        path = round(path.as_degrees_fraction())
        assert (path <= 180.0)
        assert (path >= 0.0)
        correction_values = {
            0: angle(0),
            10: angle(0, 50),
            20: angle(1, 38),
            30: angle(2, 24),
            40: angle(3, 6),
            50: angle(3, 44),
            60: angle(4, 16),
            70: angle(4, 41),
            80: angle(5),
            90: angle(5, 8),
            100: angle(5, 8),
            110: angle(4, 59),
            120: angle(4, 40),
            130: angle(4, 11),
            140: angle(3, 33),
            150: angle(2, 48),
            160: angle(1, 56),
            170: angle(0, 59),
            180: angle(0),
        }

        floor = math.floor(path/10)*10
        ceil = math.ceil(path/10)*10
        floor_cor = correction_values[floor]
        ceil_cor = correction_values[ceil]
        if ceil_cor < floor_cor:
            correction_per_degree = (floor_cor - ceil_cor)/10
            correction = floor_cor - correction_per_degree*(path-floor)
        else:
            correction_per_degree = (ceil_cor - floor_cor)/10
            correction = floor_cor + correction_per_degree*(path-floor)
        return correction

    @staticmethod
    def true_location(date: HDate):
        """
        מקום הירח האמיתי לשעת הראיה, פרק ט"ו הלכה ד
        """
        true_path_correction = Moon.true_path_correction(
            date).as_degrees_fraction()
        true_path = Moon.true_path(date)
        mean_location = Moon.mean_location_on_sunset(date)
        if true_path.as_degrees_fraction() < 180:
            mean_location -= true_path_correction
        elif true_path.as_degrees_fraction() > 180:

            mean_location += true_path_correction
        return mean_location

    @staticmethod
    def mean_location(date: HDate):
        """
        Compute the mean location of the moon in a specific day
        אמצע הירח, פרק יד הלכה א
        """
        return Moon._compute_location_on_day(date, mean_location_coefs)

    @staticmethod
    def double_distance(date: HDate):
        """
        Compute the "doubled_distance" of the moon in a specific day
        מרחק הכפול, פרק טו הלכה א
        """
        mean_location = Moon.mean_location_on_sunset(date)
        mean_sun_location = sun.Sun.mean_location(date)
        return (mean_location - mean_sun_location)*2

    @staticmethod
    def true_path(date: HDate):
        """
        Compute the "true path" of the moon in a specific day
        המסלול הנכון, פרק ט"ו הלכה ג
        """
        corrections = {
            (6, 11.5,): angle(1),
            (11.5, 18.5,): angle(2),
            (18.5, 24.5,): angle(3),
            (24.5, 31.5,): angle(4),
            (31.5, 38.5,): angle(5),
            (38.5, 45.5,): angle(6),
            (45.5, 51.5,): angle(7),
            (51.5, 59.5,): angle(8),
            (59.5, 63.5,): angle(9),
        }
        double_distance = Moon.double_distance(date)
        mean_path = Moon.mean_path(date)

        for (min, max), correction in corrections.items():
            if double_distance.as_degrees_fraction() >= min and double_distance.as_degrees_fraction() < max:
                mean_path += correction

        return mean_path

    @staticmethod
    def mean_path(date: HDate):
        """
        Compute the mean path of the moon in a specific day
        אמצע המסלול, פרק יד הלכה ג
        """
        return Moon._compute_location_on_day(date, mean_path_coefs)

    @staticmethod
    def _compute_location_on_day(date: HDate, coefficients):
        days_since_t0 = molad.Months.days_diff(coefficients["t0"], date)
        location = coefficients["x0"] + coefficients["v"]*days_since_t0
        return location.remove_circles()


RambamBeginningDay = HDate("ג", "ניסן", "ד-תתקלח")
mean_location_coefs = {"t0": RambamBeginningDay, "x0": angle(1, "יד", "מג") + angle(
    gematria.mazal_to_degree("שור")), "v": angle("יג", "י", "לה")+angle(0, 0, 3)/100}  # פרק יד הלכה ב,ד מהלך אמצע הירח

mean_path_coefs = {"t0": RambamBeginningDay, "x0": angle("פד", "כח", "מב"), "v": angle(
    "יג", 3, "נד")-angle(0, 0, 7)/100}  # פרק יד הלכה ג,ד  אמצע המסלול

HazonShamaimBeginningDay = HDate("א", "תשרי", "ה-תשנג")

hs_location_coefs = {"t0": HazonShamaimBeginningDay, "x0": angle(
    196.71), "v": mean_location_coefs["v"]}  # חזון שמים עמ' סח
hs_path_coefs = {"t0": HazonShamaimBeginningDay, "x0": angle(
    228.71), "v": mean_path_coefs["v"]}  # חזזון שמים עמ' סח
