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
    CHOICES_property_type = (('Haus', 'Haus'), ('Wohnung', 'Wohnung'))
    CHOICES_number_properties = (('1', '1'), ('5', '5'), ('10', '10'), ('20', '20'), ('30', '30'))
    CHOICES_water_heating = (('ohne Strom', 'ohne Strom'), ('mit Strom', 'mit Strom'))
    CHOICES_number_persons = (('1 Person', '1 Person'), ('2 Personen', '2 Personen'), ('3 Personen', '3 Personen'), ('4 Personen', '4 Personen'), ('> 4 Personen', '> 4 Personen'))
    CHOICES_driving_profile = (('20', '20 km/Tag'), ('40', '40 km/Tag'), ('60', '60 km/Tag'), ('100', '100 km/Tag'))
    CHOICES_cable_length = (('10', '10 m'), ('20', '20 m'), ('30', '30 m'), ('40', '40 m'), ('50', '50 m'), ('100', '100 m'), ('200', '200 m'))
    CHOICES_usage_years = (('10', '10 Jahre'), ('20', '20 Jahre'), ('30', '30 Jahre'), ('40', '40 Jahre'))
    CHOICES_arrival_time = (('Home Office', 'Home Office'), ('15', '15 Uhr'), ('16', '16 Uhr'), ('17', '17 Uhr'), ('18', '18 Uhr'), ('19', '19 Uhr'), ('20', '20 Uhr'))
    CHOICES_departure_time = (('Home Office', 'Home Office'), ('4', '4 Uhr'), ('5', '5 Uhr'), ('6', '6 Uhr'), ('7', '7 Uhr'), ('8', '8 Uhr'), ('9', '9 Uhr'))
    
    property_type = models.CharField(max_length=200, choices= CHOICES_property_type, default=None)
    number_properties = models.CharField(max_length=200, choices= CHOICES_number_properties, default=None)
    water_heating = models.CharField(max_length=200, choices= CHOICES_water_heating, default=None)
    number_persons = models.CharField(max_length=200, choices= CHOICES_number_persons, default=None)
    electricity_consumption_year = models.IntegerField(default= 3800)

    charging_points_to_install = models.IntegerField(default=4)
    house_connection_power = models.IntegerField(default=43)
    image_path = models.CharField(max_length=200, default="")
    driving_profile = models.CharField(max_length=200, choices= CHOICES_driving_profile, default=None)
    arrival_time = models.CharField(max_length=200, choices= CHOICES_arrival_time, default=None)
    departure_time = models.CharField(max_length=200, choices= CHOICES_departure_time, default=None)
    cable_length = models.CharField(max_length=200, choices= CHOICES_cable_length, default=None)
    usage_years = models.CharField(max_length=200, choices= CHOICES_usage_years, default=None)
    
    pub_date = models.DateTimeField('date published', default=timezone.now)
    person = models.CharField(max_length=200, default="jonas Sievers")

class Lokal_Energy(models.Model):
    CHOICES_roof_size = (('7', '7'),('14', '14'),('20', '20'), ('30', '30'), ('40', '40'), ('50', '50'), ('60', '60'))
    CHOICES_solar_radiation = (('950', '950'), ('1000', '1000'), ('1050', '1050'), ('1100', '1100'), ('1150', '1150'))
    CHOICES_roof_tilt = (('0', '0°'), ('15', '15°'), ('30', '30°'), ('45', '45°'))
    CHOICES_roof_orientation = (('Süd', 'Süd'), ('Süd-West/ Süd-Ost', 'Süd-West/ Süd-Ost'), ('West/ Ost', 'West/ Ost'), ('Nord-West/ Nord-Ost', 'Nord-West/ Nord-Ost'), ('Nord', 'Nord'))
    CHOICES_battery_capacity = (('0', '0'), ('1', '1'), ('3', '3'), ('5', '5'), ('7', '7'), ('10', '10'), ('14', '14'))

    roof_size = models.CharField(max_length=200, choices= CHOICES_roof_size, default=None)
    solar_radiation = models.CharField(max_length=200, choices= CHOICES_solar_radiation, default=None)
    roof_tilt = models.CharField(max_length=200, choices= CHOICES_roof_tilt, default=None)
    roof_orientation = models.CharField(max_length=200, choices= CHOICES_roof_orientation, default=None)
    battery_capacity = models.CharField(max_length=200, choices= CHOICES_battery_capacity, default=None)

    pub_date = models.DateTimeField('date published', default=timezone.now)
    person = models.CharField(max_length=200, default="jonas Sievers")


