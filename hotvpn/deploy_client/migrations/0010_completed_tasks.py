# Generated by Django 3.0.6 on 2020-07-04 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy_client', '0009_auto_20200701_2014'),
    ]

    operations = [
        migrations.CreateModel(
            name='Completed_tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.CharField(blank=True, max_length=200)),
                ('non_completed', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]