from django.contrib import admin
from .models import User, Event, Item, Photo

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Item)
admin.site.register(Photo)

# Register your models here.
