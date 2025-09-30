from hdate import angle
from hdate import gematria


def test_halacha_8():
    position = angle.angle("ע", "ל", "מ")
    assert gematria.degree_to_mazal(position.degrees) == "תאומים"
    position.to_degree_in_mazal()
    assert position.degrees == 10


def test_halacha_9():
    position = angle.angle(320)
    assert gematria.degree_to_mazal(position.degrees) == "דלי"
    position.to_degree_in_mazal()
    assert position.degrees == 20


def test_halacha_12():
    p1 = angle.angle(200, "נ", "מ")
    p2 = angle.angle("ק", "כ", "ל")
    position = p2 - p1
    assert position == angle.angle("רנט", "כט", "נ")
