from django.urls import path
from deploy_client.views import post_deploy, deployView, get_status_installed_packages, get_process_status, check_passwords
urlpatterns = [
     path('', deployView),
     path('post_deploy/', post_deploy, name="post_deploy"),
     path('get_status_installed_packages/', get_status_installed_packages, name="get_status_installed_packages"),
     path('get_process_status/', get_process_status, name="get_process_status"),
     path('check_passwords/', check_passwords, name="check_passwords"),

]
