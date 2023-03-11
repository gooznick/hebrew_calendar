
import gematria
from angle import angle
from hdate import HDate
import molad
import sun


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
            (15, 60,): angle(0, 0, "טו"),  # חצי טלה עד תאומים
            (60, 120,): angle(0, 0, "ל"),  # תאומים עד אריה
            (120, 165,): angle(0, 0, "טו"),  # אריה עד חצי בתולה
            (165, 195,): angle(0),  # חצי בתולה עד חצי מאזניים
            (195, 240,): 0-angle(0, 0, "טו"),  # חצי מאזניים עד קשת
            (240, 300,): 0-angle(0, 0, "ל"),  # קשת עד דלי
            (300, 345,): 0-angle(0, 0, "טו"),  # דלי עד חצי דגים
        }

        sun_location_deg = sun.Sun.location(
            date).as_degrees_fraction()

        for (min, max), correction in corrections.items():
            if sun_location_deg >= min and min <= max:
                sun_correction = correction
        moon_location = Moon.mean_location(date)
        moon_location += sun_correction
        moon_location = moon_location.remove_circles()
        return moon_location

    @staticmethod
    def mean_location(date: HDate):
        """
        Compute the mean location of the moon in a specific day
        אמצע הירח, פרק יד הלכה א
        """
        return Moon._compute_location_on_day(date, mean_location_coefs)

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
