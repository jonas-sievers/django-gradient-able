# Generated by Django 3.2.6 on 2021-12-21 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_real_estate_property_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='real_estate',
            name='arrival_time',
            field=models.CharField(choices=[('1', 'Home Office'), ('15', '15 Uhr'), ('16', '16 Uhr'), ('17', '17 Uhr'), ('18', '18 Uhr'), ('19', '19 Uhr'), ('20', '20 Uhr')], default='17', max_length=200),
        ),
        migrations.AddField(
            model_name='real_estate',
            name='departure_time',
            field=models.CharField(choices=[('23', 'Home Office'), ('4', '4 Uhr'), ('5', '5 Uhr'), ('6', '6 Uhr'), ('7', '7 Uhr'), ('8', '8 Uhr'), ('9', '9 Uhr')], default='8', max_length=200),
        ),
    ]
