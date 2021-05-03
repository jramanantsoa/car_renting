import datetime

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


def test_calculate_price():
    r1 = Rental(1, 1, "2017-12-8", "2017-12-8", 100)
    r2 = Rental(2, 1, "2015-03-31", "2015-04-01", 300)
    r1.calculate_price(2000, 10)
    r2.calculate_price(2000, 10)
    assert r1.price == 3000
    assert r2.price == 6800


def test_calculatecommission():
    r1 = Rental(1, 1, "2017-12-8", "2017-12-8", 100)
    r2 = Rental(2, 1, "2015-03-31", "2015-04-01", 300)
    r1.calculate_price(2000, 10)
    r2.calculate_price(2000, 10)
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
