from django.contrib import auth
from django.db import models


class Event(models.Model):
    choices = ((1, 'open'), (2, 'cancelled'), (3, 'postponed'), (4, 'closed'))

    title = models.CharField(max_length=50)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.CharField(max_length=300, null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    status = models.IntegerField(choices=choices, default=1)

    location = models.CharField(max_length=50, null=True, blank=True, default="tel aviv")
    longitude = models.DecimalField(max_digits=16, decimal_places=12, null=True, blank=True)
    latitude = models.DecimalField(max_digits=16, decimal_places=12, null=True, blank=True)
    host = models.ForeignKey(auth.models.User, related_name='events')

    # host = models.ForeignKey(auth.models.User)

    def __str__(self):
        return self.title


class Item(models.Model):
    title = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    slot_num = models.IntegerField()
    comment = models.CharField(max_length=200)
    event = models.ForeignKey(Event, related_name="items")

    def __str__(self):
        return self.title


class Slot(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='slots')
    guest = models.ForeignKey(auth.models.User, related_name='slots', null=True,
                              blank=True)  # TODO: what's the best way to contrain to guests + host
    comment = models.CharField(max_length=100, null=True, blank=True)
    index = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return "{} #{}".format(self.item.title, self.index)


class Guest(models.Model):
    class Status:
        NO_RESPONSE = 1
        ACCEPTED = 2
        DECLINED = 3
        MAYBE = 4

        choices = ((NO_RESPONSE, 'no response'), (ACCEPTED, 'accepted'), (DECLINED, 'declined'), (MAYBE, 'maybe'))

    name = models.CharField(max_length=200)
    email = models.EmailField()
    status = models.IntegerField(choices=Status.choices, default=Status.NO_RESPONSE)
    invited_by = models.ForeignKey(auth.models.User, related_name='invitees')
    invited_at = models.DateTimeField()
    secret_code = models.CharField(max_length=200, unique=True)
    user = models.ForeignKey(auth.models.User, null=True, blank=True, related_name='invitations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {} {}".format(self.event.title, self.name, self.email)

    class Meta:
        unique_together = (('event', 'email'))


    # class EventGuests(models.Model):
    #     ''' many2many relationship events - guests
    #     '''
    #     guest = models.ForeignKey(auth.models.User, related_name='guest_events')
    #     event = models.ForeignKey(Event, related_name='event_guests')
    #     can_edit = models.BooleanField(default=False)
    #
    #     class Meta:
    #         unique_together = (('guest', 'event'))
    #
    #     def __str__(self):
    #         return self.guest.username

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
