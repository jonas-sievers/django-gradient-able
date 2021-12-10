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
    property_type = models.CharField(max_length=200, choices= CHOICES_property_type, default='Einfamilienhaus')
    person = models.CharField(max_length=200, default="jonas Sievers")
    charging_points_to_install = models.IntegerField(default=4)
    charging_points_expandable = models.IntegerField(default=5)
    house_connection_power = models.IntegerField(default=40)
    image_path = models.CharField(max_length=200, default="")
    pub_date = models.DateTimeField('date published', default=timezone.now)

