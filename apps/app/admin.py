# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Real_estate

# Register your models here.
class RealEstateAdmin(admin.ModelAdmin):
    model = Real_estate
    fieldsets = [
        ('Real estate', {'fields': ['property_type', 'charging_points_to_install', 'charging_points_expandable', 'house_connection_power']}),
        ('General information', {'fields': ['pub_date', 'person', 'image_path']}),
    ] 
    list_display = ('pk', 'person', 'property_type', 'charging_points_to_install', 'pub_date')
    #inlines = [PvPlantInline, BatteryInline]
    list_filter = ['person']

admin.site.register(Real_estate, RealEstateAdmin)