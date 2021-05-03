import datetime

import pytest

from models.option import Option
from models.rental import Rental



def test_stringtodate():
    date_string = "2017-12-8"
    d0 = datetime.datetime(2017, 12, 8)
    assert Rental.stringtodate(date_string) == d0


def test_rentalduration():
    r1 = Rental(1, 1, "2017-12-8", "2017-12-10", 100)
    r2 = Rental(2, 1, "2015-03-31", "2015-04-01", 300)
    r3 = Rental(2, 1, "2017-12-14", "2017-12-18", 550)
    assert r1.rentalduration() == 3
    assert r2.rentalduration() == 2
    assert r3.rentalduration() == 5


def test_calculate_price_with_options():
    r1 = Rental(1, 1, "2017-12-8", "2017-12-8", 100)
    r2 = Rental(2, 1, "2015-03-31", "2015-04-01", 300)
    r1.options = ["gps", "baby_seat"]
    r2.options = ["additional_insurance"]
    r1.calculate_price_with_options(2000, 10)
    r2.calculate_price_with_options(2000,10)
    assert r1.price == 3700
    assert  r2.price == 8800

def test_calculate_price_without_options():
    r1 = Rental(1, 1, "2017-12-8", "2017-12-8", 100)
    r2 = Rental(2, 1, "2015-03-31", "2015-04-01", 300)
    r1.options = ["gps", "baby_seat"]
    r2.options = ["additional_insurance"]
    r1.calculate_price_with_options(2000, 10)
    r2.calculate_price_with_options(2000, 10)
    assert r1.calculate_price_without_options() == 3000
    assert r2.calculate_price_without_options() == 6800

def test_calculatecommission():
    r1 = Rental(1, 1, "2017-12-8", "2017-12-8", 100)
    r2 = Rental(2, 1, "2015-03-31", "2015-04-01", 300)
    r1.calculate_price_with_options(2000, 10)
    assert r1.calculatecommission() == {
        "insurance_fee": 450,
        "assistance_fee": 100,
        "drivy_fee": 350
    }
    assert r2.calculatecommission() == {
        "insurance_fee": 1020,
        "assistance_fee": 200,
        "drivy_fee": 820
    }

def test_setactions():
    r1 = Rental(1, 1, "2017-12-8", "2017-12-8", 100)
    r1.options = ["gps","baby_seat"]
    r1.calculate_price_with_options(2000,10)
    r1.setactions()
    assert r1.setactions() == [
        {
          "who": "driver",
          "type": "debit",
          "amount": 3700
        },
        {
          "who": "owner",
          "type": "credit",
          "amount": 2800
        },
        {
          "who": "insurance",
          "type": "credit",
          "amount": 450
        },
        {
          "who": "assistance",
          "type": "credit",
          "amount": 100
        },
        {
          "who": "drivy",
          "type": "credit",
          "amount": 350
        }
      ]

def test_createaction():
    r1 = Rental(1, 1, "2017-12-8", "2017-12-8", 100)
    assert r1.createaction("driver", 3000) == {
        "who": "driver",
        "type": "debit",
        "amount": 3000
    }
    assert r1.createaction("owner", 2100) == {
        "who": "owner",
        "type": "credit",
        "amount": 2100
    }

def test_getoptions():
    r1 = Rental(1, 1, "2017-12-8", "2017-12-8", 100)
    o1 = Option(1,1,"gps")
    o2 = Option(2,1,"baby_seat")
    o3 = Option(3,2,"additional_insurance")
    assert r1.getoptions([o1,o2,o3]) == ["gps","baby_seat"]