from django.db import models


class ReportBackupBase(models.Model):
    hotel_id = models.CharField(max_length=6)
    hotel_name = models.CharField(max_length=50)
    hotel_vpn_ip_address = models.GenericIPAddressField()
    hotel_vpn_port = models.CharField(max_length=10)
    date_update = models.DateField(null=True, editable=True)
    status = models.CharField(max_length=200)
    type = models.CharField(max_length=10)

    class Meta:
        ordering = ['hotel_id']

# class ErrorBackup(models.Model):
#     e_hotel_id = models.CharField(max_length=6)
#     e_hotel_name = models.CharField(max_length=50)
#     e_hotel_vpn_ip_address = models.GenericIPAddressField()
#     e_hotel_vpn_port = models.CharField(max_length=10)
#     e_date_update = models.DateField(null=True, editable=True)
#     e_error = models.CharField(max_length=200)
#
#
# class WrongBackup(models.Model):
#     w_hotel_id = models.CharField(max_length=6)
#     w_hotel_name = models.CharField(max_length=50)
#     w_hotel_vpn_ip_address = models.GenericIPAddressField()
#     w_hotel_vpn_port = models.CharField(max_length=10)
#     w_date_update = models.DateField(null=True, editable=True)
#     w_error = models.CharField(max_length=200)
