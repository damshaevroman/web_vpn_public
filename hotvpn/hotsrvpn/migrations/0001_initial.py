# Generated by Django 3.0.6 on 2020-07-12 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisation', models.CharField(max_length=20)),
                ('user_city', models.CharField(max_length=20)),
                ('user_fio', models.CharField(max_length=20)),
                ('user_cert', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hotels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('short_name', models.CharField(max_length=10, unique=True)),
                ('ip_address_v4', models.GenericIPAddressField(default='0.0.0.0')),
                ('hotel_admin_id', models.CharField(max_length=6)),
                ('port', models.CharField(default='22', max_length=10)),
                ('ipvpn_address', models.GenericIPAddressField(default='0.0.0.0')),
                ('portvpn', models.CharField(default='22', max_length=10)),
                ('create_data', models.DateField(auto_now_add=True)),
            ],
        ),
    ]