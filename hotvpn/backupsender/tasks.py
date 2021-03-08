from __future__ import absolute_import, unicode_literals

import configparser
import os
from celery.task import periodic_task
from celery.schedules import crontab
from backupsender.businesslogic.sender import ReportBackuper


from django.conf import settings



#  for Celery test enter in terminal -  celery -A hotvpn worker -B -l INFO
@periodic_task(run_every=crontab(minute='*/10'), name='send_data_backup')
def send_data_backup():
    config_settings = configparser.ConfigParser()
    config_settings.read(os.path.join(settings.BASE_DIR, "vpn_settings.ini"))
    backup_ip = config_settings["Config"]["backup_server"]
    backup_port = config_settings["Config"]["backup_server_port"]
    backup_login = config_settings["Config"]["backup_login"]
    print('SEND BAckUP')
    backup_sender = ReportBackuper()
    """start task for send file hosts to backupserver"""
    backup_sender.send_server(backup_ip, backup_port, backup_login)
    backup_sender.get_reports(backup_ip, backup_port, backup_login)




