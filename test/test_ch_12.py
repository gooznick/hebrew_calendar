import sun
import gematria
from angle import angle
import pytest


def test_halacha_1():
    assert ((sun.OneDayMovement * 10).remove_thirds().remove_circles()
            == angle(9, 51, 23))
    assert ((sun.OneDayMovement * 100).remove_thirds().remove_circles()
            == angle(98, 33, 53))
    assert ((sun.OneDayMovement * 1000).remove_thirds().remove_circles()
            == angle("רסה", "לח", "נ"))
    assert ((sun.OneDayMovement * 10000).remove_thirds().remove_circles()
            == angle("קלו", "כח", "כ"))
    assert ((sun.OneDayMovement * 29).remove_thirds().remove_circles()
            == angle("כח", "לה", 1))


@pytest.mark.xfail
def test_halacha_1_year():
    assert ((sun.OneDayMovement * 354).remove_thirds().remove_circles()
            == angle("שמח", "נה", "טו"))
