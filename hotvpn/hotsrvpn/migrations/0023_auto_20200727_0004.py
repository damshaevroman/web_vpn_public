# Generated by Django 3.0.6 on 2020-07-26 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotsrvpn', '0022_auto_20200725_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel_user',
            name='user_date_of_creation_certificate',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]