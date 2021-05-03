import datetime
import json

from models.option import Option


class Rental:
    def __init__(self,id,car_id,start_date,end_date,distance):
        self.id = int(id)
        self.car_id = int(car_id)
        self.start_date = Rental.stringtodate(start_date)
        self.end_date = Rental.stringtodate(end_date)
        self.distance = int(distance)
        self.price = 0
        self.options = []


    @staticmethod
    def stringtodate(date):
        date_split = date.split("-")
        return datetime.datetime(int(date_split[0]),int(date_split[1]),int(date_split[2]))

    def rentalduration(self):
        return (self.end_date - self.start_date).days+1

    def getcar(self,cars_list):
        return [car for car in cars_list if car.id == self.car_id][0]

    #the price paid by the driver
    def calculate_price_with_options(self,price_per_day,price_per_km):
        total_days_price = price_per_day
        actual_day_price = price_per_day
        if self.rentalduration() == 1:
            self.price = price_per_day + self.distance*price_per_km
        else:
            for day in range(2, self.rentalduration()+1):
                if day == 2:
                    actual_day_price *= 0.9
                elif day == 5:
                    actual_day_price = price_per_day
                    actual_day_price *= 0.7
                elif day == 11:
                    actual_day_price = price_per_day
                    actual_day_price *= 0.5
                total_days_price += actual_day_price
        options_fees = 0
        for option in self.options:
            options_fees += Option.option_price(option, self.rentalduration())
        total_price = total_days_price + self.distance * price_per_km + options_fees
        self.price = int(total_price)
        return self.price

    def calculate_price_without_options(self):
        options_fees = 0
        for option in self.options:
            options_fees += Option.option_price(option, self.rentalduration())
        return self.price - options_fees

    def calculatecommission(self):
        commission_price = self.calculate_price_without_options() * 0.3
        insurance_fee = int(commission_price/2)
        assistance_fee = int(100 * self.rentalduration())
        drivy_fee = int(commission_price - (insurance_fee + assistance_fee))
        commission = {
            "insurance_fee": insurance_fee,
            "assistance_fee": assistance_fee,
            "drivy_fee": drivy_fee
        }
        return commission

    def createaction(self,actor,price):
        who = actor
        action_type =""
        if actor == "driver":
            action_type = "debit"
        else:
            action_type = "credit"
        action = {
            "who": who,
            "type": action_type,
            "amount": price
        }
        return action

    def setactions(self):
        duration = self.rentalduration()
        actions = []
        driver = self.createaction("driver",self.price)
        actions.append(driver)
        commission = self.calculatecommission()

        #options
        gps = 0
        baby_seat = 0
        additional_insurance = 0
        if "gps" in self.options:
            gps = Option.option_price("gps",duration)
        if "baby_seat" in self.options:
            baby_seat = Option.option_price("baby_seat",duration)
        if "additional_insurance" in self.options:
            additional_insurance = Option.option_price("additional_insurance",duration)

        insurance = self.createaction("insurance",commission["insurance_fee"])
        assistance = self.createaction("assistance", commission["assistance_fee"])
        drivy = self.createaction("drivy", commission["drivy_fee"]+additional_insurance)
        commission_total =commission["insurance_fee"] + commission["assistance_fee"] + commission["drivy_fee"]
        owner = self.createaction("owner",self.calculate_price_without_options() - commission_total +gps +baby_seat)
        actions.append(owner)
        actions.append(insurance)
        actions.append(assistance)
        actions.append(drivy)
        return actions

    def getoptions(self,options_list):
        self.options = [option.type for option in options_list if option.rental_id == self.id]
        return self.options