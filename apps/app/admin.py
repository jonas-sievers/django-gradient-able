# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Lokal_Energy, Real_estate

# Register your models here.
class RealEstateAdmin(admin.ModelAdmin):
    model = Real_estate
    fieldsets = [
        ('Real estate', {'fields': ['property_type', 'number_properties', 'water_heating', 'number_persons', 'electricity_consumption_year', 'charging_points_to_install', 'house_connection_power']}),
        ('Charging', {'fields': ['driving_profile', 'arrival_time', 'departure_time', 'cable_length', 'usage_years']}),
        ('General information', {'fields': ['pub_date', 'person', 'image_path']}),
    ] 
    list_display = ('pk', 'person', 'property_type', 'charging_points_to_install','driving_profile', 'pub_date')
    list_filter = ['person']

class LokalEnergyAdmin(admin.ModelAdmin):
    model = Lokal_Energy
    fieldsets = [
        ('PV-Analge', {'fields': ['roof_size', 'solar_radiation', 'roof_orientation', 'roof_tilt', 'pv_kw_peak', 'electricity_generation_year']}),
        ('General information', {'fields': ['pub_date', 'person']}),
    ] 
    list_display = ('pk', 'person', 'roof_size', 'solar_radiation', 'pv_kw_peak', 'pub_date')
    list_filter = ['person']



admin.site.register(Real_estate, RealEstateAdmin)
admin.site.register(Lokal_Energy, LokalEnergyAdmin)