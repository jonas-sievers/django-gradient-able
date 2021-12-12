from django import forms
from django.forms import ModelForm
from .models import Charging, Real_estate

class Real_estateForm(ModelForm):
    class Meta:
        model = Real_estate
        fields = ('property_type', 'charging_points_to_install', 'charging_points_expandable', 'house_connection_power')
        labels = {
            'property_type': ('In welchem Gebäudetyp wohnen Sie?'),
            'charging_points_to_install': ('Wie viele Ladestationen sollen installiert werden?'),
            'charging_points_expandable': ('Wie viele Ladestationen sollen später erweitert werden können?'),
            'house_connection_power': ('Welche Hausanschlussleistung steht den Stellplätzen zur Verfügung [kW]?'),
        }

class ChargingForm(ModelForm):
    class Meta:
        model = Charging
        fields = ('driving_profile', 'cable_length', 'usage_years')
        labels = {
            'driving_profile': ('Wie viele km fahren Sie pro Tag?'),
            'cable_length': ('Wie weit ist Ihre Wallbox von dem Anschlusskasten entfernt?'),
            'usage_years': ('Wie lange planen Sie die Kabel zu nutzen bevor Sie neue Kabel verlegen?'),
        }