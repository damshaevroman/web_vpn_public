import subprocess
from hotsrvpn.models import Hotel, Hotel_User
import json, psutil, re, logging
from django.core import serializers
import cpuinfo
from dashboard.models import ServerHardware


class Dashboard():
    def __init__(self):
        pass

    '''this is method get data from hotel'''

    def vpnCounter(self):
        count_hotel = str(Hotel.objects.count())
        count_user = str(Hotel_User.objects.count())
        count_ping_active = str(Hotel.objects.filter(hotel_ping_status=True).count())
        count_ping_lost = str(Hotel.objects.filter(hotel_ping_status=False).count())
        count_context = {"count_hotel": count_hotel,
                         "count_user": count_user,
                         "count_ping_active": count_ping_active,
                         "count_ping_lost": count_ping_lost}
        return count_context

    def get_memory_information(self):
        """This method get memory information from server which use in status bar about load server"""
        memory = str(psutil.virtual_memory())
        memory = re.sub("^\s+|[()]|svmem|", '', memory)
        memory = memory.split()
        memory_availble = re.sub("^\s+|'|=|,|total|", '', memory[0])
        memory_percent = re.sub("^\s+|'|=|,|percent|", '', memory[2])
        memory_availble = float(memory_availble) // 1048576
        return memory_percent, memory_availble

    def server_info(self):
        serverData = ServerHardware.objects.filter(server_info="server_info")
        serverData = serializers.serialize('json', serverData)
        serverData = json.loads(serverData)
        for data in serverData:
            serverInfo = data["fields"]
        return serverInfo

    def write_server_infomation(self):
        """This method write information (model processor, memory and other) in database"""
        cpu = cpuinfo.get_cpu_info_json()
        cpu = json.loads(cpu)
        memory_percent, memory_availble = self.get_memory_information()
        try:
            ServerHardware.objects.all().delete()
            server_harw = ServerHardware()
            server_harw.arch = cpu["arch"]
            server_harw.brand_raw = cpu["brand_raw"]
            server_harw.hz_advertised_friendly = cpu["hz_advertised_friendly"]
            server_harw.l3_cache_size = cpu["l3_cache_size"]
            server_harw.ram_total = memory_availble
            server_harw.save()
        except Exception as error:
            logging.warning(error)

    def status_memory_cpu_utilization(self):
        """get data of server cpu and memory"""
        cpu2 = cpuinfo.get_cpu_info_json()
        cpu_utilization = psutil.cpu_percent()
        memory_percent, memory_availble = self.get_memory_information()
        server_status = {
            "cpu_utilization": cpu_utilization,
            "memory_availble": memory_availble,
            "memory_percent": memory_percent,
        }
        server_status = json.dumps(server_status)
        return server_status, cpu2

    '''this is method get data from table database Hotel, Records which do not have vpn address (default 0.0.0.0)  
    serialaze to json and send to front. Other address go to method fping there check via FPING availible status
    and add to the database in table Hotel'''

    def check_availble_hosts(self):
        ip_list = []
        try:
            hotel_database = Hotel.objects.values_list('hotel_vpn_ip_address')

        except:
            pass
        hotel_database = list(hotel_database)
        for ip in hotel_database:
            if '0.0.0.0' in ip[0]:
                pass
            else:
                ip_list.append(ip[0])
        for ip in ip_list:
            ip = ip.replace(' ', '')
            try:
                result = subprocess.Popen(["fping", ip], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
                result = result.communicate()
                result = str(result[0])
                print('THIS is RESULT ' + str(result))
            except Exception as error:
                logging.warning(error)
            if 'alive' in result:

                try:
                    success_data = Hotel.objects.get(hotel_vpn_ip_address=ip)
                    success_data.hotel_ping_status = True
                    success_data.save()
                except Exception as error:
                    logging.warning(error)
            else:
                try:
                    success_data = Hotel.objects.get(hotel_vpn_ip_address=ip)
                    success_data.hotel_ping_status = False
                    success_data.save()
                except Exception as error:
                    logging.warning(error)

    '''create list of hosts which dont have vpn address and sent to front'''
    def non_ip_host(self):
        try:
            count_context = Hotel.objects.filter(hotel_vpn_ip_address='0.0.0.0')
            count_context = serializers.serialize('json', count_context)
            list_unavailible_host = Hotel.objects.filter(hotel_ping_status='0').exclude(hotel_vpn_ip_address='0.0.0.0')
        except Exception as error:
            logging.warning(error)
        list_unavailible_host = serializers.serialize('json', list_unavailible_host)
        print(list_unavailible_host)
        return count_context, list_unavailible_host

""" Write to database """
Dashboard().write_server_infomation()
