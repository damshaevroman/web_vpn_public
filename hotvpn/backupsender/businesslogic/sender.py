import configparser
import os
import shutil


import json, logging
import paramiko
from scp import SCPClient
import tempfile

from backupsender.models import ReportBackupBase
from django.core import serializers
from hotsrvpn.models import Hotel

from django.conf import settings


class ReportBackuper():

    def get_reports(self, backup_ip, backup_port, backup_login):
        """ This method send to backup server json with hotels data"""
        ReportBackupBase.objects.all().delete()
        with tempfile.TemporaryDirectory() as report_dir:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(backup_ip, port=int(backup_port), timeout=10, username=backup_login, password='')
                scp = SCPClient(ssh.get_transport())
                scp.get('/home/admin/rsync_server/reports', report_dir, recursive=True)
                scp.close()
                self.write_success_base(report_dir)
                self.write_error_base(report_dir)
                self.write_wrong_base(report_dir)
            except Exception as error:
                logging.warning(str(error))

    def write_result_database(self, data_json):
        for data in data_json:
            print(data)
            try:
                report = ReportBackupBase()
                report.hotel_id = data["hotel_id"]
                report.hotel_name = data["hotel_name"]
                report.hotel_vpn_ip_address = data["ip_address"]
                report.hotel_vpn_port = data["port"]
                report.date_update = data["update_date"]
                report.status = data["status"]
                report.type = data["type"]
                report.save()
            except Exception as write_data:
                print(write_data)
                logging.warning(write_data)

    def write_success_base(self, report_dir):
        with open(report_dir + '/reports/hotel_success.json', 'r') as data_json:
            data_json = json.loads(data_json.read())
            self.write_result_database(data_json)

    def write_error_base(self, report_dir):
        with open(report_dir + '/reports/hotel_error.json', 'r') as data_json:
            data_json = json.loads(data_json.read())
            self.write_result_database(data_json)

    def write_wrong_base(self, report_dir):
        with open(report_dir + '/reports/wrong_backup_hotels.json', 'r') as data_json:
            data_json = json.loads(data_json.read())
            self.write_result_database(data_json)

    def send_server(self, backup_ip, backup_port, backup_login):
        text_list = []
        text = Hotel.objects.all().exclude(hotel_admin_id='hadmin').values()
        for textvalue in text:
            data = {
                "hotel_id": textvalue['hotel_admin_id'],
                "hotel_name": textvalue['hotel_name'],
                "hotel_vpn_ip_address": textvalue['hotel_vpn_ip_address'],
                "hotel_vpn_port": textvalue['hotel_vpn_port']
            }
            text_list.append(data)
        text = json.dumps(text_list)
        with tempfile.NamedTemporaryFile() as fp:
            fp.write(str(text).encode())
            fp.seek(0)
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(backup_ip, port=int(backup_port), timeout=10, username=backup_login, password='')
                scp = SCPClient(ssh.get_transport())
                scp.put(fp.name, remote_path='/home/admin/rsync_server/hosts')
                scp.close()
                shutil.copyfile(fp.name, '/home/roman/Desktop/django/rsync_server/hosts')
            #    return True
            except Exception as error:
                logging.warning(error)

    def auth_data(self, backup_login, backup_port, backup_ip):
        return backup_login, backup_port, backup_ip


def get_report_from_base():
    get_report = ReportBackupBase.objects.all()
    get_report = serializers.serialize('json', get_report)
    return get_report
