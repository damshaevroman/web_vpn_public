# Generated by Django 3.0.6 on 2020-08-30 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotsrvpn', '0023_auto_20200727_0004'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='hotel_ping_status',
            field=models.BooleanField(default=False),
        ),
    ]
