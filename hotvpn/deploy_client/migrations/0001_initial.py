# Generated by Django 3.0.6 on 2020-06-06 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SaveConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_config', models.CharField(max_length=100, unique=True)),
                ('packedes_config', models.CharField(max_length=20000)),
            ],
        ),
    ]