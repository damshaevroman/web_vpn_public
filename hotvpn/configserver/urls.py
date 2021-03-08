from django.urls import path, re_path
from configserver.views import configserver, createServer

urlpatterns = [
    # user pages urls
    path('main/', configserver),
    path('createServer/', createServer),



]
