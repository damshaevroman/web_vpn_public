# Generated by Django 3.0.6 on 2020-07-18 12:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotsrvpn', '0004_auto_20200718_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='date_of_creation_certificate',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 18, 12, 23, 44, 723937)),
        ),
        migrations.AlterField(
            model_name='hotel_user',
            name='date_of_creation_certificate',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 18, 12, 23, 44, 724927)),
        ),
    ]
