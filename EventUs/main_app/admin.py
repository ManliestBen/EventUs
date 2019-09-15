from django.contrib import admin
from .models import User, Event, Item

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Item)

# Register your models here.
