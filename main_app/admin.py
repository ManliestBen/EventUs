from django.contrib import admin
from .models import Event, Item, Photo, UserProfile

# admin.site.register(User)
admin.site.register(Event)
admin.site.register(Item)
admin.site.register(Photo)
admin.site.register(UserProfile)
