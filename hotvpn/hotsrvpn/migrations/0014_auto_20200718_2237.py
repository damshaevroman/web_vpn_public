# Generated by Django 3.0.6 on 2020-07-18 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotsrvpn', '0013_auto_20200718_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='date_of_creation_certificate',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='hotel_user',
            name='date_of_creation_certificate',
            field=models.DateTimeField(null=True),
        ),
    ]