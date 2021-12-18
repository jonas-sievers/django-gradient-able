# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Real_estate(models.Model):
    #person = models.ForeignKey(Person, on_delete=models.CASCADE)
    CHOICES_property_type = (('Einfamilienhaus1', 'Einfamilienhaus'), ('Mehrfamilienhaus', 'Mehrfamilienhaus'))
    property_type = models.CharField(max_length=200, choices= CHOICES_property_type, default='Einfamilienhaus')
    person = models.CharField(max_length=200, default="jonas Sievers")
    charging_points_to_install = models.IntegerField(default=4)
    charging_points_expandable = models.IntegerField(default=5)
    house_connection_power = models.IntegerField(default=40)
    image_path = models.CharField(max_length=200, default="")
    pub_date = models.DateTimeField('date published', default=timezone.now)

class Charging(models.Model):
    CHOICES_driving_profile = (('20', '20 km/Tag'), ('40', '40 km/Tag'), ('60', '60 km/Tag'), ('100', '100 km/Tag'))
    CHOICES_cable_length = (('10', '10 m'), ('20', '20 m'), ('30', '30 m'), ('40', '40 m'), ('50', '50 m'), ('100', '100 m'), ('200', '200 m'))
    CHOICES_usage_years = (('10', '10 Jahre'), ('20', '20 Jahre'), ('30', '30 Jahre'), ('40', '40 Jahre'))
    
    driving_profile = models.CharField(max_length=200, choices= CHOICES_driving_profile, default='40')
    person = models.CharField(max_length=200, default="jonas Sievers")
    cable_length = models.CharField(max_length=200, choices= CHOICES_cable_length, default='10')
    usage_years = models.CharField(max_length=200, choices= CHOICES_usage_years, default='20')
    pub_date = models.DateTimeField('date published', default=timezone.now)

