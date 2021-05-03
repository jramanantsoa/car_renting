import pytest

from models.option import Option


def test_optiondoesntexist():
    with pytest.raises(Exception):
        Option(1, 2, "foo")

def test_option_price():
    assert Option.option_price("gps",3) == 1500
    assert Option.option_price("baby_seat", 3) == 600
    assert Option.option_price("additional_insurance", 3) == 3000
