import typing


# prepare the values dictionary
chars = "אבגדהוזחטיכלמנסעפצקרשת"
val = {chars[v]: v + 1 for v in range(10)}
val.update({chars[v]: (v - 8) * 10 for v in range(10, 19)})
val.update({chars[v]: (v - 17) * 100 for v in range(19, 22)})

# create num to val sorted dictionary
value_to_letter = {v: l for l, v in val.items()}
ends = ("מנצפכ", "םןץףך")
val.update({e: val[v] for v, e in zip(ends[0], ends[1])})


# prepare months lists
def _remove_vowels(s):
    """
    Remove vowels from months names, for easier search
    """
    return s.replace("י", "").replace("ו", "").replace("'", "")


def _remove_list_vowels(month_list):
    return [_remove_vowels(m) for m in month_list]


MONTHS_NO_LEAP = [
    "תשרי",
    "חשון",
    "כסלו",
    "טבת",
    "שבט",
    "אדר",
    "ניסן",
    "אייר",
    "סיון",
    "תמוז",
    "אב",
    "אלול",
]
MONTHS_LEAP = [m for m in MONTHS_NO_LEAP]  # deep copy
MONTHS_LEAP[5] = "אדר א'"
MONTHS_LEAP.insert(6, "אדר ב'")

# Create two more lists, for shortened months, to make it easier to find
# both "חשוון/חשון" etc.
MONTHS_NO_LEAP_SHORT = _remove_list_vowels(MONTHS_NO_LEAP)
MONTHS_LEAP_SHORT = _remove_list_vowels(MONTHS_LEAP)
MONTHS_SHORT = {True: MONTHS_LEAP_SHORT, False: MONTHS_NO_LEAP_SHORT}
MONTHS = {True: MONTHS_LEAP, False: MONTHS_NO_LEAP}

# Days names
DAYS = {chr(ord("א") + i): i + 1 for i in range(7)}
DAYS["ש"] = 7
DAYS_NAMES = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
DAYS.update({name: ind + 1 for ind, name in enumerate(DAYS_NAMES)})


def num_to_day(day: int):
    """
    Convert a number to day name

    Examples :
        >>> num_to_day(1)
        'ראשון'
    """
    return DAYS_NAMES[day - 1]


def day_to_num(day: str):
    """
    Convert a day word to it's numeric value

    Examples :
        >>> day_to_num("ראשון")
        1
        >>> day_to_num(7)
        7
    """
    if type(day) == str:
        return day_str_to_num(day)
    return day


def day_str_to_num(day: str):
    """
    Convert a day word to it's numeric value

    Examples :
        >>> day_to_num("ראשון")
        1
        >>> day_to_num("ו")
        6
    """
    return DAYS[day]


def num_to_str(num: int):
    """
    Convert a number to it's word value

    Examples :
        >>> num_to_str(320)
        'כש'
        >>> num_to_str(123)
        'גכק'
        >>> num_to_str(431)
        'אלת'
    """
    word = ""
    for v, l in reversed(value_to_letter.items()):
        while num >= v:
            num -= v
            word = l + word
    return word


def num_to_year(num: int):
    """
    Convert a year to it's word value

    Examples :
        >>> num_to_year(5782)
        "בפשת'ה"
        >>> num_to_year(1000)
        "'א"
        >>> num_to_year(5900)
        "קתת'ה"
    """
    word = ""
    thousands = num // 1000
    if thousands:
        num -= thousands * 1000
        word = "'" + num_to_str(thousands)
    return num_to_str(num) + word


def str_to_num(word: typing.Union[int, str]):
    """
    Convert a word to it's numeric value

    input : a hebrew word
    output : numerical value

    Examples :
        >>> str_to_num("שלום")
        376
        >>> str_to_num("שלום רב שובך ציפורה")
        1297
        >>> str_to_num("גימטריה") == str_to_num("ערבה")
        True
    """
    if type(word) == int:
        return word
    return sum([val.get(c, 0) for c in word])


def year_str_to_num(word: str):
    """
    Convert a word to it's numeric value
    Support using first letter for thousands

    input : a hebrew word
    output : numerical value

    Examples :
        >>> year_str_to_num("ה'תשפב")
        5782
    """
    thousands = 0
    if word[1] in "-'`":
        thousands = val.get(word[0], 0) * 1000
        word = word[2:]
    return thousands + str_to_num(word)


def year_to_num(year):
    """
    Convert year to number, it may be a number or a gematria

    Examples :
        >>> year_to_num("ה'תשפב")
        5782
        >>> year_to_num(5782)
        5782
    """
    if type(year) == str:
        return year_str_to_num(year)
    return int(year)


def num_to_month(is_leap_year: bool, month: int):
    """
    Convert a number to month name

    Examples :
        >>> num_to_month(False, 1)
        'תשרי'
    """
    months_list = MONTHS[is_leap_year]
    return months_list[month - 1]


def month_str_to_num(is_leap_year: bool, month: str):
    """
    Convert month string to ordered month #, according to leap year
    """
    months_list = MONTHS_SHORT[is_leap_year]
    return months_list.index(_remove_vowels(month)) + 1


def month_to_num(is_leap_year: bool, month: typing.Union[int, str]):
    """
    Convert a month to it's ordinal number (0 based)

    >>> month_to_num(True, "תשרי")
    1
    >>> month_to_num(False, "חשון")
    2
    """
    if type(month) == int:
        return month
    return month_str_to_num(is_leap_year, month)
