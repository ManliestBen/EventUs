from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = PhoneNumberField()
    birthday = models.DateField()
    

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    what = models.CharField(max_length=200)
    date = models.DateField()
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

class Photo(models.Model):
    url = models.CharField(max_length=200)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

def __str__(self):
    return f"Photo for event_id: {self.event_id} @{self.url}"