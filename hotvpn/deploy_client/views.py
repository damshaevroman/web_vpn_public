# It is deploy_client
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import re
import time, json
from .forms import DataForm
from django.http import JsonResponse, HttpResponse
from deploy_client.businessLogic.deployclient import ConnectionDeployServer
from django.core import serializers


@login_required(login_url='/')
def deployView(request):
    form = DataForm()
    return render(request, 'deploy_clients/datahost.html', {"form": form})


'''This methon get data from form and make magic =)'''


def post_deploy(request):
    
    if request.is_ajax and request.method == "POST":
        form = DataForm(request.POST)
        if form.is_valid():
            server_deploy = ConnectionDeployServer()


            client_login = form.cleaned_data.get("client_login")
            client_ip = form.cleaned_data.get("client_ip")
            client_port = form.cleaned_data.get("client_port")
            client_password = form.cleaned_data.get("client_password")
            client_sudo_password = form.cleaned_data.get("client_sudo_password")
            install_packages = form.cleaned_data.get("install_packeges")
            git_checkbox = form.cleaned_data.get("git_checkbox")
            dhcp_checkbox = form.cleaned_data.get("dhcp_checkbox")
            hostname_checkbox = form.cleaned_data.get("hostname_checkbox")
            hotel_id = form.cleaned_data.get("hotel_id")

            packages = "Starting install"
            deploy_status_bar_count = 0
            server_deploy.erase_record_from_base(hotel_id)
            server_deploy.primary_record_to_base(hotel_id, deploy_status_bar_count, packages)

            '''create Ansible inventory file of host which will use for install playbook on client server'''
            temp_host = server_deploy.create_host_config(client_login, client_ip, client_port, client_password,
                                                         client_sudo_password)



            '''proccesing of install_packeges field which contain list of programm packeges for deploy on server '''
            install_packages = server_deploy.data_install_packeges_field(install_packages)


            deploy_status_bar_count = len(install_packages) + 5
            if dhcp_checkbox == "on":
                print("dhcp_checkbox ON")
                deploy_status_bar_count += 1
            if git_checkbox == "on":
                print("git_checkbox ON")
                deploy_status_bar_count += 1
            if hostname_checkbox == "on":
                print("hostname_checkbox ON")
                deploy_status_bar_count += 1
            deploy_status_bar_count = 100 // deploy_status_bar_count

            '''deploy dhcp and config if checkbox ON '''

            if dhcp_checkbox == "on":
                server_deploy.dhcp_deploy(request, temp_host, hotel_id, deploy_status_bar_count)

            ''' download from bitbucket, pmsdaemon if checkbox on'''

            if git_checkbox == "on":
                server_deploy.git_load(request, temp_host, hotel_id, deploy_status_bar_count)
                '''install config pmsdeamon'''
                server_deploy.pmsdaemon_deploy(request, temp_host, hotel_id, deploy_status_bar_count)

            if hostname_checkbox == "on":
                server_deploy.hostname_change(request, temp_host, hotel_id, deploy_status_bar_count)

            '''install packages'''
            server_deploy.deploy_packeges(temp_host, install_packages, hotel_id, deploy_status_bar_count)

            '''install rc.local conf'''
            server_deploy.rclocal_deploy(request, temp_host, hotel_id, deploy_status_bar_count)

            '''install nginx conf'''
            server_deploy.nginx_deploy(request, temp_host, hotel_id, deploy_status_bar_count)

            '''install crontab '''
            server_deploy.crontab_deploy(request, temp_host, hotel_id, deploy_status_bar_count)

            '''install config systemctl'''
            server_deploy.systemctl_deploy(temp_host, hotel_id, deploy_status_bar_count)

            packages = "Finish"
            deploy_status_bar_count = 0
            server_deploy.write_finish(hotel_id, deploy_status_bar_count, packages)
            time.sleep(10)
            server_deploy.erase_record_from_base(hotel_id)
            temp_host.close()


            return JsonResponse({"finish": "Done"}, status=200)
        else:
            error = {}
            key2 = ""
            for field in form.errors:
                error[field] = form.errors[field][0]
            for key in error.items():
                key2 = str(key2) + '\n' + str(key)
                key2 = re.sub(r"[()']", '', key2)
                key2 = key2.replace(",", " -")
            return JsonResponse({"error": key2}, status=430)
    result = "Connection ok"
    return JsonResponse({"finish": result}, status=200)
    # return JsonResponse({"error": "не могу покдлючится проверьте данные"}, status=450)


'''request to Database in table installed_packeges and send to front data'''


def get_status_installed_packages(request):
    if request.is_ajax and request.method == "POST":
        responseDBpackeges = ConnectionDeployServer()
        hotel = json.loads(request.body)
        install_list = responseDBpackeges.check_intalled_packeges(hotel)
        return JsonResponse({"install_list": install_list}, status=200)
    else:
        return JsonResponse("result", "fail", status=501)


def get_process_status(request):
    if request.is_ajax and request.method == "POST":
        hotel_id = json.loads(request.body)
        hotel_id = int(hotel_id["hotel_id"])
        status = ConnectionDeployServer()
        result = status.check_status_bar(hotel_id)
        return JsonResponse(result, safe=False, status=200)


def check_passwords(request):
    if request.is_ajax and request.method == "POST":
        data = json.loads(request.body)
        check_pass = ConnectionDeployServer()
        check_sudo = check_pass.check_sudo_pass(data)
        if check_sudo == "OK":
            result = "Connection ok"
            return JsonResponse({"finish": result}, status=200)
        else:
            result = "Check entered data:\n login, ip, port, password, sudo password and user sudo permission"
            return JsonResponse({"finish": result}, status=500)


