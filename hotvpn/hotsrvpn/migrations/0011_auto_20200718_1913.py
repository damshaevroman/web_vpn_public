# Generated by Django 3.0.6 on 2020-07-18 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotsrvpn', '0010_auto_20200718_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='hotel_vpn_address',
            field=models.GenericIPAddressField(),
        ),
    ]