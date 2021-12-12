# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Charging, Real_estate

# Register your models here.
class RealEstateAdmin(admin.ModelAdmin):
    model = Real_estate
    fieldsets = [
        ('Real estate', {'fields': ['property_type', 'charging_points_to_install', 'charging_points_expandable', 'house_connection_power']}),
        ('General information', {'fields': ['pub_date', 'person', 'image_path']}),
    ] 
    list_display = ('pk', 'person', 'property_type', 'charging_points_to_install', 'pub_date')
    list_filter = ['person']

class ChargingAdmin(admin.ModelAdmin):
    model = Charging
    fieldsets = [
        ('Charging', {'fields': ['driving_profile', 'cable_length', 'usage_years']}),
        ('General information', {'fields': ['pub_date', 'person']}),
    ] 
    list_display = ('pk', 'person', 'driving_profile', 'cable_length', 'pub_date')
    list_filter = ['person']

admin.site.register(Real_estate, RealEstateAdmin)
admin.site.register(Charging, ChargingAdmin)