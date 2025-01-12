from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        return "Name: " + self.name + ", " + \
               "Description: " + self.description


class CarModel(models.Model):
    
    TYPE_CHOICES = [
        ('SUV', 'SUV'),
        ('Pickup', 'Pickup'),
        ('Van', 'Van'),
        ('Wagon', 'Wagon'),
        ('Sedan', 'Sedan'),
        ('Coupe', 'Coupe')
    ]

    dealer_id = models.IntegerField()
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default='Sedan')
    year = models.DateField()

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    def __str__(self):
        return "Name: " + self.name + ", " + \
                "Type: " + self.type + ", " + \
                "Year: " + str(self.year) + ", " + \
                "Make: " + self.make.name + ", " + \
                "Dealer ID: " + str(self.dealer_id)


class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, state, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.state = state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, id, sentiment='Neutral'):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return f"Dealer name: {self.dealership}, /n \
                Customer name: {self.name}, /n \
                Review: {self.review}, /n \
                Car Make: {self.car_make}, /n \
                Sentiment: {self.sentiment}" 
        