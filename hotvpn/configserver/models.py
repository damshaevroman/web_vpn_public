from django.db import models
from django.core.validators import RegexValidator


# Create your models here.

class ConfigServer(models.Model):
    nameserver = models.CharField(max_length=100)
    protocol = models.CharField(max_length=3, default='udp')
    typeInterface = models.CharField(max_length=10)
    serverip = models.GenericIPAddressField()
    serverport = models.PositiveIntegerField()
    subnetmask = models.GenericIPAddressField()
    startIP = models.GenericIPAddressField()
    endIP = models.GenericIPAddressField()
