from django import forms
from django.forms import ModelForm
from .models import Lokal_Energy, Real_estate

class Real_estateForm(ModelForm):
    class Meta:
        model = Real_estate
        fields = ('property_type', 'water_heating', 'number_persons', 'charging_points_to_install', 'house_connection_power', 'driving_profile', 'arrival_time', 'departure_time', 'cable_length', 'usage_years')
        labels = {
            'property_type': ('In welchem Gebäudetyp wohnen Sie?'),
            'water_heating': ('Womit erhitzen Sie Ihr Wasser?'),
            'number_persons': ('Wie viele Personen leben in Ihrem Haushalt?'),
            'charging_points_to_install': ('Wie viele Ladestationen sollen installiert werden?'),
            'house_connection_power': ('Welche Hausanschlussleistung steht den Stellplätzen zur Verfügung [kW]?'),
            'driving_profile': ('Wie viele km fahren Sie pro Tag?'),
            'arrival_time': ('Um wie viel Uhr können Sie Ihr Fahrzeug an das Ladesystem anschließen?'),
            'departure_time': ('Um wie viel fahren Sie morgens los?'),
            'cable_length': ('Wie weit ist Ihre Wallbox von dem Anschlusskasten entfernt?'),
            'usage_years': ('Wie lange planen Sie die Kabel zu nutzen bevor Sie neue Kabel verlegen?'),
        }

class Lokal_EnergyForm(ModelForm):
    class Meta:
        model = Lokal_Energy
        fields = ('roof_size', 'solar_radiation', 'roof_tilt', 'roof_orientation')
        labels = {
            'roof_size': ('Weleche Dachfläche können für die PV-Anlage verwendet werden?'),
            'roof_tilt': ('Welche Neigung hat Ihr Hausdach?'),
            'roof_orientation': ('Welche Ausrichtung hat Ihr Hausdach?'),
            'solar_radiation': ('Welche ungefähre Sonneneinstrahlung hat Ihr Standort?'),
        }