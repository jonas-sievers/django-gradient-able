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
    CHOICES_water_heating = (('ohne Strom', 'ohne Strom'), ('mit Strom', 'mit Strom'))
    CHOICES_number_persons = (('1 Person', '1 Person'), ('2 Personen', '2 Personen'), ('3 Personen', '3 Personen'), ('4 Personen', '4 Personen'), ('> 4 Personen', '> 4 Personen'))
    CHOICES_driving_profile = (('20', '20 km/Tag'), ('40', '40 km/Tag'), ('60', '60 km/Tag'), ('100', '100 km/Tag'))
    CHOICES_cable_length = (('10', '10 m'), ('20', '20 m'), ('30', '30 m'), ('40', '40 m'), ('50', '50 m'), ('100', '100 m'), ('200', '200 m'))
    CHOICES_usage_years = (('10', '10 Jahre'), ('20', '20 Jahre'), ('30', '30 Jahre'), ('40', '40 Jahre'))
    CHOICES_arrival_time = (('1', 'Home Office'), ('15', '15 Uhr'), ('16', '16 Uhr'), ('17', '17 Uhr'), ('18', '18 Uhr'), ('19', '19 Uhr'), ('20', '20 Uhr'))
    CHOICES_departure_time = (('23', 'Home Office'), ('4', '4 Uhr'), ('5', '5 Uhr'), ('6', '6 Uhr'), ('7', '7 Uhr'), ('8', '8 Uhr'), ('9', '9 Uhr'))
    
    property_type = models.CharField(max_length=200, choices= CHOICES_property_type, default='Haus')
    water_heating = models.CharField(max_length=200, choices= CHOICES_water_heating, default='mit Strom')
    number_persons = models.CharField(max_length=200, choices= CHOICES_number_persons, default='2 Personen')
    electricity_consumption_year = models.IntegerField(default= 3800)

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

class Lokal_Energy(models.Model):
    CHOICES_roof_size = (('7', '7 m2'),('14', '14 m2'),('20', '20 m2'), ('30', '30 m2'), ('40', '40 m2'), ('50', '50 m2'), ('60', '60 m2'))
    CHOICES_solar_radiation = (('1000', '1000 kWh/m2'), ('1100', '1100 kWh/ m2'), ('1200', '1200 kWh/m2'), ('1300', '1300 kWh/m2'))
    CHOICES_roof_tilt = (('0', '0°'), ('15', '15°'), ('30', '30°'), ('45', '45°'))
    CHOICES_roof_orientation = (('Süd', 'Süd'), ('Süd-West/ Süd-Ost', 'Süd-West/ Süd-Ost'), ('West/ Ost', 'West/ Ost'), ('Nord-West/ Nord-Ost', 'Nord-West/ Nord-Ost'), ('Nord', 'Nord'))

    roof_size = models.CharField(max_length=200, choices= CHOICES_roof_size, default='30')
    solar_radiation = models.CharField(max_length=200, choices= CHOICES_solar_radiation, default='1100')
    roof_tilt = models.CharField(max_length=200, choices= CHOICES_roof_tilt, default='30')
    roof_orientation = models.CharField(max_length=200, choices= CHOICES_roof_orientation, default='Süd')
    
    pv_1KWpeak_investment_cost = models.IntegerField(default= 2000)
    pv_1KWpeak_saved_costs_own_electricity = models.IntegerField(default= 1500)
    pv_1KWpeak_earnings_sold_electricity = models.IntegerField(default= 300)
    
    pv_2KWpeak_investment_cost = models.IntegerField(default= 4000)
    pv_2KWpeak_saved_costs_own_electricity = models.IntegerField(default= 3000)
    pv_2KWpeak_earnings_sold_electricity = models.IntegerField(default= 1000)

    pv_3KWpeak_investment_cost = models.IntegerField(default= 6000)
    pv_3KWpeak_saved_costs_own_electricity = models.IntegerField(default= 4500)
    pv_3KWpeak_earnings_sold_electricity = models.IntegerField(default= 2000)
    
    pv_4KWpeak_investment_cost = models.IntegerField(default= 8000)
    pv_4KWpeak_saved_costs_own_electricity = models.IntegerField(default= 7000)
    pv_4KWpeak_earnings_sold_electricity = models.IntegerField(default= 3000)

    pv_5KWpeak_investment_cost = models.IntegerField(default= 10000)
    pv_5KWpeak_saved_costs_own_electricity = models.IntegerField(default= 7000)
    pv_5KWpeak_earnings_sold_electricity = models.IntegerField(default= 3000)

    pv_6KWpeak_investment_cost = models.IntegerField(default= 12000)
    pv_6KWpeak_saved_costs_own_electricity = models.IntegerField(default= 7000)
    pv_6KWpeak_earnings_sold_electricity = models.IntegerField(default= 3000)

    pv_7KWpeak_investment_cost = models.IntegerField(default= 14000)
    pv_7KWpeak_saved_costs_own_electricity = models.IntegerField(default= 7000)
    pv_7KWpeak_earnings_sold_electricity = models.IntegerField(default= 3000)

    pv_8KWpeak_investment_cost = models.IntegerField(default= 16000)
    pv_8KWpeak_saved_costs_own_electricity = models.IntegerField(default= 7000)
    pv_8KWpeak_earnings_sold_electricity = models.IntegerField(default= 3000)

    pv_9KWpeak_investment_cost = models.IntegerField(default= 18000)
    pv_9KWpeak_saved_costs_own_electricity = models.IntegerField(default= 7000)
    pv_9KWpeak_earnings_sold_electricity = models.IntegerField(default= 3000)

    pv_10KWpeak_investment_cost = models.IntegerField(default= 20000)
    pv_10KWpeak_saved_costs_own_electricity = models.IntegerField(default= 7000)
    pv_10KWpeak_earnings_sold_electricity = models.IntegerField(default= 3000)

    pv_kw_peak = models.IntegerField(default=4)
    electricity_generation_year = models.IntegerField(default= 4100)
        
    pub_date = models.DateTimeField('date published', default=timezone.now)
    person = models.CharField(max_length=200, default="jonas Sievers")


