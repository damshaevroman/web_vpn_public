# Generated by Django 3.0.6 on 2020-07-19 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotsrvpn', '0020_auto_20200719_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='hotel_vpn_port',
            field=models.CharField(default='22', max_length=10),
        ),
    ]