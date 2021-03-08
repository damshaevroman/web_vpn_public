# It is deploy_client
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import time
from .forms import DataForm
from deploy_client.businessLogic.deployclient import ConnectionDeployServer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import HotelSerializer, DeployDataSerializer
from hotsrvpn.models import Hotel


@login_required(login_url='/')
def deployView(request):
    form = DataForm()
    return render(request, 'deploy_clients/datahost.html', {"form": form})


@api_view(['GET'])
def hotelList(request):
    hotel = Hotel.objects.all()
    hotel_serializers = HotelSerializer(hotel, many=True)
    return Response(hotel_serializers.data)

@api_view(['POST'])
def downloadGit(request):
    """ function for download from git"""
    git = request.data
    git = git.dict()
    server_deploy = ConnectionDeployServer()
    temp_host = server_deploy.create_host_config(git["client_login"], git["client_ip"], git["client_port"],
                                                 git["client_password"],
                                                 git["client_sudo_password"])
    result = server_deploy.git_load(temp_host, git)
    result = {'result': result}
    return Response(result, status=200)

@api_view(['POST'])
def post_deploy(request):
    """This function get data from form and make magic =)"""
    if request.is_ajax and request.method == "POST":
        dataSerializers = DeployDataSerializer(data=request.data)
        if dataSerializers.is_valid():
            server_deploy = ConnectionDeployServer()
            packages = "Starting install"
            data = request.data
            '''proccesing of install_packeges field which contain list of programm packeges for deploy on server '''
            install_packages = server_deploy.data_install_packeges_field(data["install_packeges"])
            deploy_status_bar_count = len(install_packages) + 4


            if 'dhcp_interface' in data:
                deploy_status_bar_count += 1
                print('DHCP')
            if "hostname" in data:
                deploy_status_bar_count += 1
                print('HOSTnAME')
            deploy_status_bar_count = 100 // deploy_status_bar_count

            # deploy_status_bar_count = 0
            server_deploy.erase_record_from_base(data["hotel_id"])
            server_deploy.primary_record_to_base(data["hotel_id"], deploy_status_bar_count, packages)

            '''create Ansible inventory file of host which will use for install playbook on client server'''
            temp_host = server_deploy.create_host_config(data["client_login"], data["client_ip"], data["client_port"], data["client_password"],
                                                         data["client_sudo_password"])
            """apt-get update remote server"""

            server_deploy.update_server(temp_host)
            """copy abd add backup_deploy script to remote server"""
            server_deploy.add_backrsync(temp_host, data, deploy_status_bar_count)

            '''install packages'''

            server_deploy.deploy_packeges(temp_host, install_packages, data["hotel_id"], deploy_status_bar_count)

            '''deploy dhcp and config if checkbox ON '''

            if 'dhcp_interface' in data:
                server_deploy.dhcp_deploy(request, temp_host, data["hotel_id"], deploy_status_bar_count)

            ''' download from bitbucket, pdaemondaemon if checkbox on'''

            if 'hostname' in data:
                print('HOSTNAME ACTIVE')
                server_deploy.hostname_change(temp_host, data, deploy_status_bar_count)

            '''install rc.local conf'''
            server_deploy.rclocal_deploy(request, temp_host, data["hotel_id"], data["uplink_interface"], deploy_status_bar_count)

            '''install nginx conf'''
            server_deploy.nginx_deploy(request, temp_host, data["hotel_id"], deploy_status_bar_count)

            '''install crontab '''
            server_deploy.crontab_deploy(request, temp_host, data["hotel_id"], deploy_status_bar_count)

            '''install config systemctl'''
            server_deploy.systemctl_deploy(temp_host, data["hotel_id"], deploy_status_bar_count)

            # packages = "Finish"
            # deploy_status_bar_count = 0
            server_deploy.write_finish(data["hotel_id"], deploy_status_bar_count, packages)
            time.sleep(10)
            server_deploy.erase_record_from_base(data["hotel_id"])
            temp_host.close()


            return Response({'result': 'ok'}, status=200)
        else:
            return Response(dataSerializers.errors, status=430)



@api_view(['POST'])
def get_process_status(request):
    data = request.data
    data = data.dict()
    status = ConnectionDeployServer()
    result = status.check_status_bar(data["hotel_id"])
    return Response(result.data, status=200)

@api_view(['POST'])
def get_status_installed_packages(request):
    responseDBpackeges = ConnectionDeployServer()
    data = request.data
    data = data.dict()
    install_list = responseDBpackeges.check_intalled_packeges(data["hotel_id"])

    return Response({"install_list": install_list}, status=200)

@api_view(['POST'])
def check_passwords(request):
    data = request.data
    data = data.dict()
    check_pass = ConnectionDeployServer()
    check_sudo, int_data = check_pass.check_sudo_pass(data)
    if check_sudo == "OK":
        result = int_data
        return Response({"finish": result}, status=200)
    else:
        result = "Check entered data:\n login, ip, port, password, sudo password and user sudo permission"
        return Response({"finish": result}, status=500)

@api_view(['GET'])
def erase_Task_and_Status(request):
    hotel = ConnectionDeployServer()
    result = hotel.erase_Task_and_Status()
    return Response({"result": result}, status=200)

