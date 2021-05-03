import json
import os


#files
from models.car import Car
from models.rental import Rental

input_file = os.path.join(os.getcwd(),"data","input.json")
output_file = os.path.join(os.getcwd(),"data","output.json")

output = {"rentals":[]}

with open(input_file,"r") as f:
    input_json = json.loads(f.read())
cars = input_json["cars"]
rentals = input_json["rentals"]

#cars  objects list
cars_list = []
for car in cars:
    car_object = Car(car["id"],car["price_per_day"],car["price_per_km"])
    cars_list.append(car_object)

#rental objetcs list
rentals_list =[]
for rental in rentals:
    rental_object = Rental(rental["id"],rental["car_id"],rental["start_date"],rental["end_date"],rental["distance"])
    rentals_list.append(rental_object)

for r in rentals_list:
    car = r.getcar(cars_list)
    price = r.calculate_price(car.price_per_day,car.price_per_km)
    commission = r.calculatecommission()
    dict_rental = {"id":r.id,"price":price,"commission":commission}
    output["rentals"].append(dict_rental)
#print(output)

#white into outputfil
with open(output_file,"w") as f:
    json.dump(output,f,indent=2)
