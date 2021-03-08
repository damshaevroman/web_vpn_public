# Create your tasks here
from __future__ import absolute_import, unicode_literals

from .busineslogic.dashboard import Dashboard

from celery.task import periodic_task
from celery import shared_task
from celery.schedules import crontab



@periodic_task(run_every=crontab(minute='*/10'), name='celery_ping_task')
def celery_ping_task():
    """Start method periodically get ip address vpn and ping them and check availble"""
    ping_hosts = Dashboard()
    ping_hosts.check_availble_hosts()


# @periodic_task(run_every=crontab(0, 0, day_of_month='2'), name='send_data_backup')
# def send_data_backup():
#     """start task for send file hosts to backupserver"""
#     send_server()
