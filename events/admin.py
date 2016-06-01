from django.contrib import admin

# Register your models here.

from .models import Event, Item, Slot

admin.site.register(Event)
admin.site.register(Item)
admin.site.register(Slot)
