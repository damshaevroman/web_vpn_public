# Generated by Django 3.0.6 on 2021-01-10 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_admin_id', models.CharField(default='no id', max_length=6)),
                ('hotel_country', models.CharField(default='no country', max_length=20)),
                ('hotel_city', models.CharField(default='no city', max_length=20)),
                ('hotel_name', models.CharField(default='noname', max_length=20)),
                ('hotel_name_certification', models.CharField(max_length=30, unique=True)),
                ('hotel_ip_address', models.GenericIPAddressField(default='0.0.0.0')),
                ('hotel_port', models.CharField(default='22', max_length=10)),
                ('hotel_vpn_ip_address', models.GenericIPAddressField(default='0.0.0.0')),
                ('hotel_vpn_port', models.CharField(default='22', max_length=10)),
                ('hotel_date_of_creation_certificate', models.DateField(auto_now_add=True, null=True)),
                ('hotel_ping_status', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['hotel_admin_id'],
            },
        ),
        migrations.CreateModel(
            name='Hotel_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisation', models.CharField(max_length=20)),
                ('user_city', models.CharField(max_length=20)),
                ('user_fio', models.CharField(max_length=20)),
                ('user_cert', models.CharField(max_length=20, unique=True)),
                ('hotel_date_of_creation_certificate', models.DateField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['user_fio'],
            },
        ),
    ]
