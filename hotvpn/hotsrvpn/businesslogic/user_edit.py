import json, logging
import os
import re
import shutil
from datetime import date
from django.core import serializers
from hotvpn.settings import config_settings
from hotsrvpn.models import Hotel_User
from hotsrvpn.businesslogic.serializer import UserSerializer

store_cert_path = config_settings["Config"]["certificate_store_path"]

class User_edit():
    def __init__(self):
        pass

    '''request data from database Hotel_user table'''
    def get_database(self):
        user_database = Hotel_User.objects.all()
        user_database = serializers.serialize("json", user_database)
        return user_database

    ''' Create users and add to database Hotel_user table'''
    def write_user_to_database(self, hotelSerialize):
        try:
            hotelSerialize.save()
            user_json = self.get_user_json()
            return user_json
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

    '''render user edit page check download button which appear if find on server '''
    def edit_user_page(self, id):
        try:
            user = Hotel_User.objects.get(id=id)
            user_cert = user.user_cert
            path = store_cert_path + str(user_cert) + '/' + str(user_cert) + ".conf"
            check_certificate_status = os.path.isfile(path)
            return user, check_certificate_status
        except Exception as error:
            logging.warning(error)
            return error, False

    ''' save changing of user'''
    def save_change_user(self, organization, user_city, user_fio, user_cert):
        try:
            user = Hotel_User.objects.get(user_cert=user_cert)
            user.organisation = organization
            user.user_city = user_city
            user.user_fio = user_fio
            user.save()
            return "User changed and save"
        except Exception as error:
            logging.warning(error)
            return str(error)

    '''delete certificate from server and database'''
    def delete_user(self, user_cert):
        try:
            user = Hotel_User.objects.get(user_cert=user_cert)
            user.delete()
            shutil.rmtree('/etc/openvpn/client/' + str(user_cert))
            os.remove("/etc/openvpn/easy-rsa/keys/" + str(user_cert) + '.csr')
            os.remove("/etc/openvpn/easy-rsa/keys/" + str(user_cert) + '.crt')
            os.remove("/etc/openvpn/easy-rsa/keys/" + str(user_cert) + '.key')
            os.remove("/etc/openvpn/ccd/" + str(user_cert) + '.key')
            os.remove("/etc/openvpn/ccd/" + str(user_cert) + '.crt')
            return "User deleted"
        except Exception as error:
            logging.warning(error)
            return str(error)


    '''Create certification or check exist of file and get feedack'''
    def make_certificate(self, user_certification):
        try:
            user = Hotel_User.objects.get(user_cert=user_certification)
            path = store_cert_path + str(user_certification) + "/" + str(user_certification) + '.conf'
            if os.path.isfile(path):
                data = {"result": False}
                data = json.dumps(data)
                return data
            else:
                script_path = "sudo /etc/openvpn/easy-rsa/./auto_uservpn.sh " + str(user_certification)
                os.system(script_path)
                time = date.today()
                time = time.strftime("%Y-%m-%d")
                user.user_date_of_creation_certificate = time
                user.save()
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

    def ckeck_status_cerificate(self, user_certification):
        path = store_cert_path + str(user_certification) + "/" + str(user_certification) + '.conf'
        if os.path.isfile(path):
            return True
        else:
            return False

    '''create json object from database'''
    def get_user_json(self):
        user_json = Hotel_User.objects.all().order_by('user_fio')
        user_json = UserSerializer(user_json, many=True)
        return user_json
