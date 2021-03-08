from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import render
from django.http import JsonResponse

from dashboard.busineslogic.dashboard import Dashboard


@login_required(login_url='/')
def dashboard(request):
    """render main dashboard"""
    dashboard = Dashboard()
    serverInfo = dashboard.server_info()
    return render(request, 'dashboard.html', {"serverInfo": serverInfo})


def counter_members_vpn_host(request):
    """ back to front number of creates certifications of hotels and users"""
    dashboard = Dashboard()
    count_context = dashboard.vpnCounter()
    return JsonResponse({"count_context": count_context}, status=200)


def server_status(request):
    """ back to front information abnout system resourse CPU and memory """
    dashboard = Dashboard()
    server_status, cpu2 = dashboard.status_memory_cpu_utilization()
    return JsonResponse({"server_status": server_status, "cpu2": cpu2}, status=200)


def ping_hosts(request):
    '''e nable method which check via fping host '''
    dashboard = Dashboard()
    count_context = dashboard.vpnCounter()
    return JsonResponse({"count_context": count_context}, status=200)

def check_non_ip_host(request):
    """This method get records from database Hotel which dont have vpn ip address and records which unavailible via vpn
     address (use fping for check availble) and send to front 2 arrays"""
    dashboard = Dashboard()
    count_context, list_unavailible_host = dashboard.non_ip_host()
    return JsonResponse({"count_context": count_context, "list_unavailible_host": list_unavailible_host}, status=200)
