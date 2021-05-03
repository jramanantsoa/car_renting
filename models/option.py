class Option:
    price_per_day = {"gps" :500, "baby_seat":200,"additional_insurance":1000}
    def __init__(self,id,rental_id,type):
        self.id = int(id)
        self.rental_id = int(rental_id)
        if type in Option.price_per_day.keys():
            self.type = type
        else:
            raise Exception(f"Option Type must be in {Option.price_per_day.keys()} ")

    @staticmethod
    def option_price(type,period):
        return int(period * Option.price_per_day[type])