from django.db import models

class ServerHardware(models.Model):
    server_info = models.CharField(max_length=50, default="server_info", unique=True)
    arch = models.CharField(max_length=50)
    brand_raw = models.CharField(max_length=50)
    hz_advertised_friendly = models.CharField(max_length=50)
    l3_cache_size = models.CharField(max_length=50)
    ram_total = models.CharField(max_length=50)
