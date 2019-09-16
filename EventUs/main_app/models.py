from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = PhoneNumberField()

    

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    what = models.CharField(max_length=200)

    where = models.CharField(max_length=150)
    why = models.CharField(max_length=150)
    organizer = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    priority = models.CharField(max_length=50)
    cost = models.FloatField()

    def __str__(self):
        return self.name

events = [
    Event('Calebs test event 2', 'test2', 'testlocation2', 'cause its the second test', 'look at me, im the organizer now'),
]