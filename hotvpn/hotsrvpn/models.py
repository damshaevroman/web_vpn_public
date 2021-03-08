

from datetime import date
from django.db import models

'''models for create in database table record with information about hotel also that infomation need for create 
certificate '''




class Hotel(models.Model):
    hotel_admin_id = models.CharField(max_length=6, default='no id')
    hotel_country = models.CharField(max_length=20, default='no country')
    hotel_city = models.CharField(max_length=60, default='no city')
    hotel_name = models.CharField(max_length=60, default='noname')
    hotel_name_certification = models.CharField(max_length=60, unique=True)
    hotel_ip_address = models.GenericIPAddressField(default='0.0.0.0')
    hotel_port = models.CharField(max_length=10, default="22")
    hotel_vpn_ip_address = models.GenericIPAddressField(default='0.0.0.0')
    hotel_vpn_port = models.CharField(max_length=10, default="22")
    hotel_date_of_creation_certificate = models.DateField(auto_now_add=True, null=True, editable=True)
    hotel_ping_status = models.BooleanField(default=False)
    class Meta:
        ordering = ['hotel_admin_id']


'''models for create in database table record with information about users also that information need for create user 
certificate '''


class Hotel_User(models.Model):
    organisation = models.CharField(max_length=20)
    user_city = models.CharField(max_length=20)
    user_fio = models.CharField(max_length=20)
    user_cert = models.CharField(max_length=20, unique=True)
    user_date_of_creation_certificate = models.DateField(auto_now_add=True, null=True, editable=True)
    class Meta:
        ordering = ['user_fio']

