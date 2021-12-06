from django import forms
from django.forms import ModelForm
from .models import Real_estate

class Real_estateForm(ModelForm):
    class Meta:
        model = Real_estate
        fields = ('property_type', 'charging_points_to_install', 'charging_points_expandable', 'house_connection_power')
        widgets = {
            'property_type': forms.RadioSelect,
        }
        labels = {
            'property_type': ('In welchem Gebäudetyp wohnen Sie?'),
            'charging_points_to_install': ('Wie viele Ladestationen sollen installiert werden?'),
            'charging_points_expandable': ('Wie viele Ladestationen sollen später erweitert werden können?'),
            'house_connection_power': ('Welche Hausanschlussleistung steht den Stellplätzen zur Verfügung [kW]?'),
        }