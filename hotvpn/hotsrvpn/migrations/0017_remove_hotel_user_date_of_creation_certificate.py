# Generated by Django 3.0.6 on 2020-07-19 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotsrvpn', '0016_remove_hotel_date_of_creation_certificate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel_user',
            name='date_of_creation_certificate',
        ),
    ]
