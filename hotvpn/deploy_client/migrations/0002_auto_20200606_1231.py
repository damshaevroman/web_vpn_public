# Generated by Django 3.0.6 on 2020-06-06 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy_client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saveconfig',
            name='name_config',
            field=models.CharField(max_length=110, unique=True),
        ),
        migrations.AlterField(
            model_name='saveconfig',
            name='packedes_config',
            field=models.CharField(max_length=20001),
        ),
    ]
