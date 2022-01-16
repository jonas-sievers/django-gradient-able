from django import forms
from django.forms import ModelForm
from .models import Lokal_Energy, Real_estate

class Real_estateForm(ModelForm):
    class Meta:
        model = Real_estate

        fields = ('property_type', 'number_properties', 'water_heating', 'number_persons', 'charging_points_to_install', 'house_connection_power', 'driving_profile', 'arrival_time', 'departure_time', 'cable_length', 'usage_years')
        labels = {
            'property_type': ('In welchem Gebäudetyp wohnen Sie?'),
            'number_properties': ('Wie viele Wohneinheiten hat Ihr Gebäude?'),
            'water_heating': ('Wie wird in Ihrem Gebäude das Warmwasser aufbereitet?'),
            'number_persons': ('Wie viele Personen leben durchschnittlich in einer Wohneinheit?'),
            'charging_points_to_install': ('Wie viele Ladestationen sollen insgesamt installiert werden?'),
            'house_connection_power': ('Welche Hausanschlussleistung [kW] hat Ihre gesamtes Gebäude?'),
            'driving_profile': ('Wie viele km fährt ein/e Bewohner*in im Durchschnitt mit dem Elektroauto am Tag?'),
            'arrival_time': ('Um wie viel Uhr können die Fahrzeuge an das Ladesystem angeschlossen werden?'),
            'departure_time': ('Um wie viel Uhr müssen die Elektroautos vollgeladen sein?'),
            'cable_length': ('Wie weit sind die Wallboxen durchschnittlich von dem Anschlusskasten entfernt?'),
            'usage_years': ('Wie lange planen Sie die Kabel für das Ladesystem zu nutzen bevor Sie neue Kabel verlegen?'),
        }

class Lokal_EnergyForm(ModelForm):
    class Meta:
        model = Lokal_Energy
        fields = ('roof_size', 'solar_radiation', 'roof_tilt', 'roof_orientation', 'battery_capacity')
        labels = {
            'roof_size': ('Welche Dachfläche soll für Ihre PV-Anlage verwendet werden?'),
            'roof_tilt': ('Welche Neigung hat Ihr Hausdach?'),
            'roof_orientation': ('Welche Ausrichtung hat Ihr Hausdach?'),
            'solar_radiation': ('Welche jährliche Sonneneinstrahlung hat Ihr Standort?'),
            'battery_capacity': ('Welche Speicherkapazität soll Ihr Stromspeicher haben?'),
        }