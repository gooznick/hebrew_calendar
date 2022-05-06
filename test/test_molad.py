from molad import Months
from hdate import HDate

def test_days_diff():
    for y in range(1,100):
        assert(Months.days_diff_o_n_(HDate(1,1,1), HDate(1, 1 , y)) ==
            Months.days_diff(HDate(1,1,1), HDate(1, 1 , y)))


def test_year_type():
    """
    Test year type does not fail on
    """
    for year in range(5000, 6000):
        Months.year_type(year)


def test_months_in_years_o_1_():
    """
    Test computation on months_in_years_o(1) vs o(n) simpler computation
    """
    for begin in range(0, 100):
        for end in range(0, 100):
            assert Months._months_in_years_o_1_(  # pylint: disable=W0212
                end, begin
            ) == Months._months_in_years_o_n_(  # pylint: disable=W0212
                end, begin
            )
