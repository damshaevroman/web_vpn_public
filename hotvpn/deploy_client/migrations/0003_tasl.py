# Generated by Django 3.0.6 on 2020-06-08 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy_client', '0002_auto_20200606_1231'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=244)),
                ('date', models.DateField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
    ]
