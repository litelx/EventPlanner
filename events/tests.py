import pytz as pytz
from django.test import TestCase
import events.models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.conf import settings


# Create your tests here.

class ModelTest(TestCase):
    def test_create_event(self):
        user = User.objects.create_user("litel")

        n = 1
        for i in range(n):
            e = events.models.Event(
            title="party {}".format(i),
            start=datetime.now(tz=pytz.timezone(settings.TIME_ZONE)),
            end=datetime.now(tz=pytz.timezone(settings.TIME_ZONE))+timedelta(days=1),
            host=user,
            )
            e.full_clean()
            e.save()

        self.assertEquals(events.models.Event.objects.count(), n)


