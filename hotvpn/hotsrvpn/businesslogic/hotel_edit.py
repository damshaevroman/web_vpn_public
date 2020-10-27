import json
import logging
import os
import shutil

import paramiko
import re
from datetime import date

from django.core import serializers
from scp import SCPClient
from hotvpn.settings import config_settings
from hotsrvpn.models import Hotel


store_cert_path = config_settings["Config"]["certificate_store_path"]

class Hotel_edit():
    def __init__(self):
        pass

    '''request data from database Hotel table'''

    def get_database(self):
        hotel_database = Hotel.objects.order_by("-hotel_admin_id")
        hotel_database = serializers.serialize("json", hotel_database)
        return hotel_database

    ''' Create users and add to database Hotel table'''

    def write_hotel_to_database(self, hotel_context):
        try:
            hotel = Hotel()
            hotel.hotel_admin_id = hotel_context["hotel_admin_id"]
            hotel.hotel_country = hotel_context["hotel_country"]
            hotel.hotel_city = hotel_context["hotel_city"]
            hotel.hotel_name = hotel_context["hotel_name"]
            hotel.hotel_name_certification = hotel_context["hotel_name_certification"]
            try:
                hotel.hotel_ip_address = hotel_context["hotel_ip_address"]
            except:
                print('Write ip')
                hotel.hotel_ip_address = '0.0.0.0'
            try:
                hotel.hotel_port = hotel_context["hotel_port"]
            except:
                print('Write port')
                hotel.hotel_port = '0.0.0.0'

            hotel.save()
            return "Hotel added in database"
        except Exception as error:
            logging.warning(error)
            return str(error)

    '''Processing errors'''
    def processing_form_errors(self, form):
        error = {}
        errors = ""
        for field in form.errors:
            error[field] = form.errors[field][0]
        for key in error.items():
            errors = str(errors) + '\n' + str(key)
            errors = re.sub("^\s+|\n|\r|'"'|"'"|\s+$", '', errors)
            errors = errors.replace("(", "")
            errors = errors.replace(")", "")
            errors = json.dumps(errors)
        return errors


    ''' в данном блоке загружаю файл с именами и ip адресами в из файла в словарь и потом ищу по полю short_name ip address'''
    def check_ip_vpn_address(self, id):
            hotel = Hotel.objects.get(id=id)
            name = hotel.hotel_name_certification
            try:

                file = open("/etc/openvpn/ip_clients.txt")
                d = file.read().split("\n")[:-1]
                dict2 = dict()
                for item in d:
                    key = item.split(",")[0]
                    value = item.split(",")[1:]
                    dict2[key] = value
                    ip_from_massiv = dict2.get(str(name))
                ipvpn = ''.join(ip_from_massiv)
                hotel.hotel_vpn_address = ipvpn
            except Exception as error:
                logging.warning(error)
            finally:
                default = '0.0.0.0'
                hotel.hotel_vpn_address = default


    '''render hotel edit page check download button which appear if find on server '''
    def edit_hotel_page(self, id):
        try:
            hotel = Hotel.objects.get(id=id)
            hotel_cert = hotel.hotel_name_certification
            path = store_cert_path + str(hotel_cert) + '/' + str(hotel_cert) + ".conf"
            check_certificate_status = os.path.isfile(path)
            return hotel, check_certificate_status
        except Exception as error:
            logging.warning(error)
            return error, False


    ''' save changing of user'''
    def save_change_hotel(self, hotel_context):
        try:
            hotel = Hotel.objects.get(hotel_name_certification=hotel_context["hotel_name_certification"])

            hotel.hotel_admin_id = hotel_context["hotel_admin_id"]
            hotel.hotel_country = hotel_context["hotel_country"]
            hotel.hotel_city = hotel_context["hotel_city"]
            hotel.hotel_name = hotel_context["hotel_name"]
            hotel.hotel_ip_address = hotel_context["hotel_ip_address"]
            hotel.hotel_port = hotel_context["hotel_port"]
            hotel.hotel_vpn_ip_address = hotel_context["hotel_vpn_ip_address"]
            hotel.hotel_vpn_port = hotel_context["hotel_vpn_port"]
            hotel.save()
            return "User changed and save"
        except Exception as error:
            logging.warning(error)
            return str(error)


    '''Delete hotel certificate '''
    def delete_hotel(self, hotel_name_certification):
        try:
            hotel = Hotel.objects.get(hotel_name_certification=hotel_name_certification)
            hotel.delete()
            shutil.rmtree('/etc/openvpn/client/' + str(hotel_name_certification))
            os.remove("/etc/openvpn/easy-rsa/keys/" + str(hotel_name_certification) + '.csr')
            os.remove("/etc/openvpn/easy-rsa/keys/" + str(hotel_name_certification) + '.crt')
            os.remove("/etc/openvpn/easy-rsa/keys/" + str(hotel_name_certification) + '.key')
            os.remove("/etc/openvpn/ccd/" + str(hotel_name_certification) + '.key')
            os.remove("/etc/openvpn/ccd/" + str(hotel_name_certification) + '.crt')
            return "User deleted"
        except Exception as error:
            logging.warning(error)
            return str(error)

    '''Create certification or check exist of file and get feedack'''

    def make_certificate(self, hotel_name_certification):
        try:
            hotel = Hotel.objects.get(hotel_name_certification=hotel_name_certification)
            path = store_cert_path + hotel_name_certification +'/' +hotel_name_certification + '.conf'
            if os.path.isfile(path):
                data = {"result": False}
                data = json.dumps(data)
                return data

            else:
                script_path = "sudo /etc/openvpn/easy-rsa/./auto_uservpn.sh " + str(hotel_name_certification)
                os.system(script_path)
                time = date.today()
                time = time.strftime("%d/%m/%Y")
                hotel.hotel_date_of_creation_certificate = time
                hotel.save()
                data = {"result": True,
                        "date": time}
                data = json.dumps(data)
                return data
        except Exception as error:
            logging.warning(error)
            data = {"result": False}
            data = json.dumps(data)
            return data

    '''check certificate on server and callback true or false'''
    def ckeck_status_cerificate(self, hotel_name_certification):
        path = store_cert_path +hotel_name_certification + '/' + hotel_name_certification + '.conf'
        if os.path.isfile(path):
            return False
        else:
            return True

    '''create ansible file and sent do remote host'''
    def copy_cert_to_host(self, login, password, hotel_name_certification, ip, port):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(ip, port=int(port), timeout=10, username=login, password=password)
            except:
                return False
            scp = SCPClient(ssh.get_transport())

            scp.put(store_cert_path +hotel_name_certification + '/' + hotel_name_certification + '.conf', remote_path='/home/' + str(login))
            scp.close()
            return True
        except Exception as error:
            logging.warning(error)
            return False

    '''create json object from database'''
    def get_hotel_json(self):
        hotel_json = Hotel.objects.all()
        hotel_json = serializers.serialize("json", hotel_json)
        return hotel_json


