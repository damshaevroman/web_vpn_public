from django.db import models

'''This model form for add data to database. Frontend site create request to database get  data and clean database '''


class Installed_packeges(models.Model):
    hotel_id = models.CharField(max_length=100)
    installed = models.CharField(max_length=200, blank=True)
    non_install = models.CharField(max_length=200, blank=True)
    task_completed = models.CharField(max_length=200, blank=True)
    task_non_completed = models.CharField(max_length=200, blank=True)


'''Table there write cutrent deploy task and status'''

class Task_and_Status(models.Model):
    hotel_id = models.CharField(max_length=100, unique=True)
    task = models.CharField(max_length=100)
    status = models.IntegerField()
