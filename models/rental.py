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
        total_price = self.rentalduration()*price_per_day + self.distance * price_per_km
        #print(f" price per day {price_per_day}")
        #print(f" price per km{price_per_km}")
        #print(f" duration {self.rentalduration()}")
        self.price = total_price
        return self.price
