# Generated by Django 3.0.6 on 2020-06-30 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy_client', '0007_auto_20200630_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='installed_packeges',
            name='installed',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='installed_packeges',
            name='non_install',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
