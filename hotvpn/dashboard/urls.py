from django.urls import path
from .import views

urlpatterns = [
    path('main/', views.dashboard, name='main'),
    path('counter_members/', views.counter_members_vpn_host, name='counter_members'),
    path('server_status/', views.server_status, name='server_status'),
    path('ping_hosts/', views.ping_hosts, name='ping_hosts'),
    path('check_non_ip_host/', views.check_non_ip_host, name='check_non_ip_host'),

]