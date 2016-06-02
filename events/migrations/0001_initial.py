# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-02 07:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('price', models.PositiveIntegerField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(1, 'open'), (2, 'cancelled'), (3, 'postponed'), (4, 'closed')], default=1)),
                ('location', models.CharField(blank=True, default='tel aviv', max_length=50, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=12, max_digits=16, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=12, max_digits=16, null=True)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventGuests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_edit', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_guests', to='events.Event')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest_events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('slot_num', models.IntegerField()),
                ('comment', models.CharField(max_length=200)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='events.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=100)),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slots', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='events.Item')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='eventguests',
            unique_together=set([('guest', 'event')]),
        ),
    ]
