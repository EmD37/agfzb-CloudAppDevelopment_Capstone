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


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
