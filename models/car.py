class Car:
    def __init__(self,id,price_per_day,price_per_km):
        self.id = int(id)
        self.price_per_day = int(price_per_day)
        self.price_per_km = int(price_per_km)

    def __str__(self):
        return(f" Car with id = {self.id} - {self.price_per_day} per day and {self.price_per_km} per km")