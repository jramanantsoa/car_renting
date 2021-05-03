import datetime
import json


class Rental:
    def __init__(self,id,car_id,start_date,end_date,distance):
        self.id = int(id)
        self.car_id = int(car_id)
        self.start_date = Rental.stringtodate(start_date)
        self.end_date = Rental.stringtodate(end_date)
        self.distance = int(distance)
        self.price = 0


    @staticmethod
    def stringtodate(date):
        date_split = date.split("-")
        return datetime.datetime(int(date_split[0]),int(date_split[1]),int(date_split[2]))

    def rentalduration(self):
        return (self.end_date - self.start_date).days+1

    def getcar(self,cars_list):
        return [car for car in cars_list if car.id == self.car_id][0]

    def calculate_price(self,price_per_day,price_per_km):
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

        total_price = total_days_price + self.distance * price_per_km
        #print(f" price per day {price_per_day}")
        #print(f" price per km{price_per_km}")
        #print(f" duration {self.rentalduration()}")
        self.price = int(total_price)
        return self.price
