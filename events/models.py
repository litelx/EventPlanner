from django.db import models
from django.contrib import auth


# class Location(models.Model):
#         country = models.CharField(max_length=30)
#         city = models.CharField(max_length=40)
#
#         def __str__(self):
#                 return self.city + ",  " + self.country


class Event(models.Model):

    # class Status:
    #     OPEN = 1
    #     CANCELLED = 2
    #     POSTPONED = 3
    #     CLOSED = 4
    #
    choices = ((1, 'open'), (2, 'cancelled'), (3, 'postponed'), (4, 'closed'))

    title = models.CharField(max_length=50)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.CharField(max_length=300, null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    status = models.IntegerField(choices=choices, default=1)

    location = models.CharField(max_length=50, null=True, blank=True) # g = geocoder.google('fkjghf') >> latlng
    longitude = models.DecimalField(max_digits=15, decimal_places=3, null=True, blank=True)
    latitude = models.DecimalField(max_digits=15, decimal_places=3, null=True, blank=True)
    host = models.ForeignKey(auth.models.User)

    # TODO guests
    # location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Item(models.Model):
    title = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    slot_num = models.IntegerField()
    comment = models.CharField(max_length=200)


class Slot(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    guest = models.EmailField()
    comment = models.CharField(max_length=100)

# class Person(models.Model):
#         first_name = models.CharField(max_length=30)
#         last_name = models.CharField(max_length=30)
#         birthday = models.DateTimeField()
#
#         def __str__(self):
#                 return self.last_name + ",  " + self.first_name

# class Ad(models.Model):
#     posted_at = models.DateTimeField(auto_now_add=True)
#
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#
#     posted_by = models.CharField(max_length=200)
#     contact_email = models.EmailField()
#     contact_phone = models.CharField(max_length=30,  null=True, blank=True)
#     price = models.PositiveIntegerField(null=True, blank=True)
    # price = models.DateTimeField()

    # o = Ad()
    # o.titl= "name"    ...