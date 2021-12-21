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
    CHOICES_property_type = (('Einfamilienhaus', 'Einfamilienhaus'), ('Mehrfamilienhaus', 'Mehrfamilienhaus'))
    CHOICES_driving_profile = (('20', '20 km/Tag'), ('40', '40 km/Tag'), ('60', '60 km/Tag'), ('100', '100 km/Tag'))
    CHOICES_cable_length = (('10', '10 m'), ('20', '20 m'), ('30', '30 m'), ('40', '40 m'), ('50', '50 m'), ('100', '100 m'), ('200', '200 m'))
    CHOICES_usage_years = (('10', '10 Jahre'), ('20', '20 Jahre'), ('30', '30 Jahre'), ('40', '40 Jahre'))
    CHOICES_arrival_time = (('1', 'Home Office'), ('15', '15 Uhr'), ('16', '16 Uhr'), ('17', '17 Uhr'), ('18', '18 Uhr'), ('19', '19 Uhr'), ('20', '20 Uhr'))
    CHOICES_departure_time = (('23', 'Home Office'), ('4', '4 Uhr'), ('5', '5 Uhr'), ('6', '6 Uhr'), ('7', '7 Uhr'), ('8', '8 Uhr'), ('9', '9 Uhr'))
    
   
    property_type = models.CharField(max_length=200, choices= CHOICES_property_type, default='Einfamilienhaus')
    charging_points_to_install = models.IntegerField(default=4)
    charging_points_expandable = models.IntegerField(default=5)
    house_connection_power = models.IntegerField(default=40)
    image_path = models.CharField(max_length=200, default="")
    driving_profile = models.CharField(max_length=200, choices= CHOICES_driving_profile, default='40')
    arrival_time = models.CharField(max_length=200, choices= CHOICES_arrival_time, default='17')
    departure_time = models.CharField(max_length=200, choices= CHOICES_departure_time, default='8')
    cable_length = models.CharField(max_length=200, choices= CHOICES_cable_length, default='10')
    usage_years = models.CharField(max_length=200, choices= CHOICES_usage_years, default='20')
    
    pub_date = models.DateTimeField('date published', default=timezone.now)
    person = models.CharField(max_length=200, default="jonas Sievers")



