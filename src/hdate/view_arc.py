from . import gematria
from .angle import angle
from .hdate import HDate
from . import molad
from . import sun
from . import moon
from . import ecliptic_lat

import math


class ViewArc:
    """
    Calculations of קשת הראיה
    פרק יז
    """

    @staticmethod
    def is_seen(date: HDate) -> bool:
        sun_location = sun.Sun.location(date).as_degrees_fraction()
        moon_location = moon.Moon.true_location(date).as_degrees_fraction()
        first_length = moon_location - sun_location  # הלכה א

        # הלכה ג
        moon_between_cancer_and_twins = (
            moon_location > gematria.mazal_to_degree("סרטן")
            and moon_location < gematria.mazal_to_degree("קשת") + 30
        )
        if not moon_between_cancer_and_twins:
            if first_length <= 9:
                return False
            if first_length > 15:
                return True
        else:
            if first_length <= 10:
                return False
            if first_length > 24:
                return True
        return None

    @staticmethod
    def compute(date: HDate) -> angle:
        """
        פרק יז
        """
        sun_location = sun.Sun.location(date).as_degrees_fraction()
        moon_location = moon.Moon.true_location(date).as_degrees_fraction()
        is_south, latitude = ecliptic_lat.EclipticLatitude.compute(date)  # רוחב הירח
        first_length = moon_location - sun_location  # הלכה א

        # הלכה ה
        second_length = first_length - ViewArc.look_diff(moon_location)

        second_lat = latitude + ViewArc.lat_diff(moon_location)
        third_length = ViewArc.compute_third_length(
            moon_location, second_lat, second_length
        )
        forth_length = ViewArc.compute_forth_length(moon_location, third_length)
        world_lat = 2 / 3  # jerusalem - 32 lat
        if is_south:
            view_arc = forth_length - latitude * world_lat
        else:
            view_arc = forth_length + latitude * world_lat
        return view_arc

    m2d = gematria.mazal_to_degree
    lon_correction = {
        m2d("טלה"): angle(0, "נט"),
        m2d("שור"): angle(1),
        m2d("תאומים"): angle(0, "נח"),
        m2d("סרטן"): angle(0, "נב"),
        m2d("אריה"): angle(0, "מג"),
        m2d("בתולה"): angle(0, "לז"),
        m2d("מאזניים"): angle(0, "לד"),
        m2d("עקרב"): angle(0, "לד"),
        m2d("קשת"): angle(0, "לו"),
        m2d("גדי"): angle(0, "מד"),
        m2d("דלי"): angle(0, "נג"),
        m2d("דגים"): angle(0, "נח"),
    }
    # טבלת חזון שמים, עמ' צה
    hs_lon_correction = {
        m2d("טלה"): angle(0, "נו"),
        m2d("שור"): angle(0, "נו"),
        m2d("תאומים"): angle(0, "נג"),
        m2d("סרטן"): angle(0, "מו"),
        m2d("אריה"): angle(0, "לט"),
        m2d("בתולה"): angle(0, "לד"),
        m2d("מאזניים"): angle(0, "לב"),
        m2d("עקרב"): angle(0, "לד"),
        m2d("קשת"): angle(0, "לט"),
        m2d("גדי"): angle(0, "מו"),
        m2d("דלי"): angle(0, "נג"),
        m2d("דגים"): angle(0, "נו"),
    }

    @staticmethod
    def look_diff(moon_location: angle, corr=lon_correction) -> angle:
        """
        שינוי המראה
        פרק יז הלכה ה-ו
        """

        return corr[moon_location // 30 * 30]

    lat_correction = {
        m2d("טלה"): angle(0, "ט"),
        m2d("שור"): angle(0, "י"),
        m2d("תאומים"): angle(0, "טז"),
        m2d("סרטן"): angle(0, "כז"),
        m2d("אריה"): angle(0, "לח"),
        m2d("בתולה"): angle(0, "מד"),
        m2d("מאזניים"): angle(0, "מו"),
        m2d("עקרב"): angle(0, "מה"),
        m2d("קשת"): angle(0, "מד"),
        m2d("גדי"): angle(0, "לו"),
        m2d("דלי"): angle(0, "כד"),
        m2d("דגים"): angle(0, "יב"),
    }
    lat_hs_correction = {
        m2d("טלה"): angle(0, 8),
        m2d("שור"): angle(0, 12),
        m2d("תאומים"): angle(0, 21),
        m2d("סרטן"): angle(0, 33),
        m2d("אריה"): angle(0, 42),
        m2d("בתולה"): angle(0, 47),
        m2d("מאזניים"): angle(0, 48),
        m2d("עקרב"): angle(0, 47),
        m2d("קשת"): angle(0, 42),
        m2d("גדי"): angle(0, 33),
        m2d("דלי"): angle(0, 21),
        m2d("דגים"): angle(0, 12),
    }

    @staticmethod
    def lat_diff(moon_location: angle, corr=lat_correction) -> angle:
        """
        שינוי רוחב
        פרק יז הלכה ז
        """

        # todo :
        # התעלמנו מלהחסיר או להוסיף בצפוני או בדרומי כיוון שהרוחב אצלנו הוא בערך מוחלט
        return corr[moon_location // 30 * 30]

    s2n = gematria.str_to_num
    circle_corrections = (
        #        (angle(m2d("טלה")), 0),
        (angle(m2d("טלה") + s2n("כ")), 2 / 5),
        (angle(m2d("שור") + s2n("י")), 1 / 3),
        (angle(m2d("שור") + s2n("כ")), 1 / 4),
        (angle(m2d("תאומים")), 1 / 5),
        (angle(m2d("תאומים") + s2n("י")), 1 / 6),
        (angle(m2d("תאומים") + s2n("כ")), (1 / 6) / 2),
        (angle(m2d("תאומים") + s2n("כה")), (1 / 6) / 4),
        (angle(m2d("סרטן") + s2n("ה")), 0),
        (angle(m2d("סרטן") + s2n("י")), (1 / 6) / 4),
        (angle(m2d("סרטן") + s2n("כ")), (1 / 6) / 2),
        (angle(m2d("אריה")), 1 / 6),
        (angle(m2d("אריה") + s2n("י")), 1 / 5),
        (angle(m2d("אריה") + s2n("כ")), 1 / 4),
        (angle(m2d("בתולה") + s2n("י")), 1 / 3),
        (angle(m2d("מאזניים")), 2 / 5),
        (angle(m2d("מאזניים") + s2n("כ")), 2 / 5),
        (angle(m2d("עקרב") + s2n("י")), 1 / 3),
        (angle(m2d("עקרב") + s2n("כ")), 1 / 4),
        (angle(m2d("קשת")), 1 / 5),
        (angle(m2d("קשת") + s2n("י")), 1 / 6),
        (angle(m2d("קשת") + s2n("כ")), (1 / 6) / 2),
        (angle(m2d("קשת") + s2n("כה")), (1 / 6) / 4),
        (angle(m2d("גדי") + s2n("ה")), 0),
        (angle(m2d("גדי") + s2n("י")), (1 / 6) / 4),
        (angle(m2d("גדי") + s2n("כ")), (1 / 6) / 2),
        (angle(m2d("דלי")), 1 / 6),
        (angle(m2d("דלי") + s2n("י")), 1 / 5),
        (angle(m2d("דלי") + s2n("כ")), 1 / 4),
        (angle(m2d("דגים") + s2n("י")), 1 / 3),
        (angle(m2d("טלה")), 2 / 5),
    )

    @staticmethod
    def compute_third_length(
        moon_location: angle, second_lat: angle, second_lon: angle
    ) -> angle:
        """
        שינוי נליזת הירח
        פרק יז הלכה י
        """
        for max_degree, correction in ViewArc.circle_corrections:
            if moon_location < max_degree:
                break
        moon_circle = second_lat * correction
        moon_mazal = moon_location // 30 * 30
        if moon_mazal >= ViewArc.m2d("סרטן") and moon_mazal <= ViewArc.m2d("קשת"):
            return second_lon - moon_circle
        return second_lon + moon_circle

    lon_4th_correction = {
        m2d("טלה"): 7 / 6,
        m2d("שור"): 6 / 5,
        m2d("תאומים"): 7 / 6,
        m2d("סרטן"): 1,
        m2d("אריה"): 4 / 5,
        m2d("בתולה"): 2 / 3,
        m2d("מאזניים"): 2 / 3,
        m2d("עקרב"): 4 / 5,
        m2d("קשת"): 1,
        m2d("גדי"): 7 / 6,
        m2d("דלי"): 6 / 5,
        m2d("דגים"): 7 / 6,
    }

    @staticmethod
    def compute_forth_length(moon_location: angle, third_lon: angle) -> angle:
        """
        חישוב האורך הרביעי
        פרק יז הלכה יב
        """

        return third_lon * ViewArc.lon_4th_correction[moon_location // 30 * 30]
