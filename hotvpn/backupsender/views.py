from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from backupsender.businesslogic.sender import get_report_from_base


@login_required(login_url='/')
def main_page(request):
    # Mysender = sender.ReportBackuper()
    # sender.send_server(backup_ip, backup_port, backup_login)
    # sender.get_reports(backup_ip, backup_port, backup_login)
    get_report = get_report_from_base()
    print('THIS REPORT')
    print(get_report)
    return render(request, 'main.html', {"get_report": get_report})


# def backupsend(request):
#     sender = ReportBackuper()
#     sender.get_reports(backup_ip, backup_port, backup_login)
#     return JsonResponse({"count_context": "done"}, status=200)

# Create your views here.
