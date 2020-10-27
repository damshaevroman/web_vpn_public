# Create your tasks here
from __future__ import absolute_import, unicode_literals
from dashboard.busineslogic.dashboard import Dashboard
from celery.task import periodic_task
from celery import shared_task
from celery.schedules import crontab



'''Start method periodically get ip address vpn and ping them and check availble'''
@periodic_task(run_every=crontab(minute='*/10'), name='celery_ping_task')
def celery_ping_task():
    ping_hosts = Dashboard()
    ping_hosts.check_availble_hosts()
